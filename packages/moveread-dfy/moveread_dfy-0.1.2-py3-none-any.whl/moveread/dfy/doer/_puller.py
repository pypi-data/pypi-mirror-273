from datetime import timedelta
import asyncio
from uuid import uuid4
from sqlalchemy import Engine
from sqlalchemy.exc import DatabaseError
from sqlmodel import select, Session
from haskellian import Left, either as E
from dslog import Logger
from kv.api import KV
from q.api import WriteQueue
from moveread.pipelines.dfy import Input
from moveread.pipelines.input_validation import GameId
from scoresheet_models import ModelID
from ..types import Game

def randomId(tournId: str, group: str, round: str, board: str) -> str:
  return f'{tournId}/{group}/{round}/{board}_{uuid4()}'

async def puller(
  Qin: WriteQueue[Input], engine: Engine, *,
  online_images: KV[bytes], local_images: KV[bytes],
  tournId: str, model: ModelID, polling_interval: timedelta = timedelta(seconds=30),
  logger = Logger.rich().prefix('[PULLER]')
):
  @E.do()
  async def pull_once():
    try:
      with Session(engine) as ses:
        stmt = select(Game).where(Game.tournId == tournId, Game.status == Game.Status.uploaded)
        games = ses.exec(stmt).all()
        for game in games:
          gameId = GameId(group=game.group, round=game.round, board=game.board)
          id = randomId(tournId, **gameId)
          urls = [img.url for img in game.imgs]
          task = Input(gameId=gameId, model=model, imgs=urls)
          tasks = [online_images.copy(url, local_images, url).run() for url in urls]
          results = await asyncio.gather(*tasks)
          E.sequence(results).unsafe()

          logger(f'Inputting new task for "{id}":', task)
          (await Qin.push(id, task)).unsafe()
          game.status = Game.Status.doing
          ses.add(game)
        ses.commit()


    except DatabaseError as e:
      Left(e).unsafe()


  while True:
    logger('Polling', level='DEBUG')
    r = await pull_once()
    logger('Polled', level='DEBUG')
    if r.tag == 'left':
      logger('Error while pulling', r.value, level='ERROR')
    
    await asyncio.sleep(polling_interval.total_seconds())
