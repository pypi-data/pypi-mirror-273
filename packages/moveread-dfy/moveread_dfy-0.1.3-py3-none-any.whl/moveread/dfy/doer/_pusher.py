import asyncio
from sqlalchemy import Engine
from sqlmodel import select, Session
from dslog import Logger
from haskellian import either as E, Left
from kv.api import KV
from q.api import ReadQueue
from moveread.core import CoreAPI
from moveread.pipelines.dfy import Result, output_one
from ..types import Game, PGN

def exact_game(tournId: str, group: str, round: str, board: str):
  return Game.tournId == tournId, Game.group == group, Game.round == round, Game.board == board

async def pusher(
  Qout: ReadQueue[Result], engine: Engine, *,
  tournId: str, output_core: CoreAPI, images: KV[bytes],
  logger = Logger.rich().prefix('[DFY PUSHER]')
):
  
  @E.do()
  async def push_one():
    id, result = (await Qout.read()).unsafe()
    (await output_one(output_core, id, result, tournId=tournId, images=images)).unsafe()
    gid = result.gameId
    logger(f'Pushing result for {gid}')
    try:
      with Session(engine) as ses:
        stmt = select(Game).where(*exact_game(tournId, **gid))
        game = ses.exec(stmt).first()
        if game is None:
          logger(f'Game not found: {gid}', level='ERROR')
          return

        game.pgn = PGN(moves=result.pgn, early=result.early)
        game.status = Game.Status.done
        ses.add(game)
        ses.commit()
    except Exception as e:
      Left(e).unsafe()

    (await Qout.pop(id)).unsafe()

  while True:
    r = await push_one()
    if r.tag == 'left':
      logger('Error whilst pushing', r.value, level='ERROR')
      await asyncio.sleep(5)