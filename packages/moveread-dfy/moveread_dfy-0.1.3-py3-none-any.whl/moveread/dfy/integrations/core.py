from typing import Callable
from uuid import uuid4
from sqlmodel import Session
from kv.api import KV
from dslog import Logger
from scoresheet_models import ModelID
from moveread.core import CoreAPI, Game as CoreGame
from ..types import Game, GameId, Image, Pairing, Paired

def gameIdFn(game: CoreGame, tournId: str) -> GameId:
  if game.meta is None or game.meta.tournament is None:
    return GameId(tournId=tournId, group='a', round='1', board='1')
  t = game.meta.tournament
  return GameId(tournId=tournId, group=t.group or 'a', round=t.round or '1', board=t.board or '1')

async def input_core(
  core: CoreAPI, session: Session,
  *, images: KV[bytes],
  gameId_fn: Callable[[CoreGame], GameId] | None = None,
  tournId: str = 'llobregat23',
  num_games: int | None = None, shuffle: bool = True,
  logger = Logger.rich().prefix('[CORE INPUT]')
):
  """Input all images from `core` into `Qin` tasks
  - Actually, only images with `version == 0`
  - `model_fn`: determines the scoresheet model of each task
  - `state_fn`: determines an arbitrary tuple of JSON-serializable data to attach to each task
  """
  gameId_fn = gameId_fn or (lambda game: gameIdFn(game, tournId))
  games = list((await core.games.keys()).unsafe())
  if shuffle:
    import random
    random.shuffle(games)
  for gameId in games[:num_games]:
    game = (await core.games.read(gameId)).unsafe()
    game.id = f'{tournId}/{game.id}'
    imgs = []
    for imgId, image in game.images:
      if imgId.version == 0:
        id = str(imgId)
        url = f'{id}/original_{uuid4()}.jpg'
        img = (await core.blobs.read(image.url)).unsafe()
        (await images.insert(url, img)).unsafe()
        imgs.append(url)

    gid = gameId_fn(game)
    g = Game(
      index=int(gid['board']), pairing=Pairing(Paired(white='Magnus', black='Anish', tag='paired')),
      imgs=[Image(url=img, descaled_url=img) for img in imgs], status=Game.Status.uploaded, **gid)
    session.add(g)
    logger(f'Inputted game "{gid}"')
  session.commit()