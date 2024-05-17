from typing import Sequence, Literal, TypeAlias, Unpack, Any
from functools import partial
import asyncio
from sqlalchemy import Engine
from sqlmodel import Session, select
from uuid import uuid4
from haskellian import either as E, Left
import pure_cv as vc
from kv.api import KV, InexistentItem, ReadError
from .pgns import export_all
from ..types import Game, Token, GameId, RoundId, Group, Image, Tournament, FrontendPGN

ImgExtension: TypeAlias = Literal['.jpg', '.png', '.webp']
MimeType: TypeAlias = str

def stringify(tournId: str, group: str, round: str, board: str) -> str:
  return f'{tournId}/{group}/{round}/{board}'

def exact_game(tournId: str, group: str, round: str, board: str):
  return Game.tournId == tournId, Game.group == group, Game.round == round, Game.board == board

def select_game(**gameId: Unpack[GameId]):
  return select(Game).where(*exact_game(**gameId))

def round_games(tournId: str, group: str, round: str):
  return Game.tournId == tournId, Game.group == group, Game.round == round

def select_tnmt(tournId: str):
  return select(Tournament).where(Tournament.tournId == tournId)

class DFY:

  def __init__(self, images: KV[bytes], engine: Engine):
    self._images = images
    self._engine = engine

  def authorize(self, token: str, tournId: str) -> bool:
    with Session(self._engine) as ses:
      results = ses.exec(select(Token).where(Token.token == token, Token.tournId == tournId))
      return results.first() is not None

  def tournaments(self) -> Sequence[Tournament]:
    with Session(self._engine) as ses:
      return ses.exec(select(Tournament)).all()

  def tournament(self, tournId: str) -> Tournament | None:
    with Session(self._engine) as ses:
      return ses.exec(select_tnmt(tournId)).first()
    
  def group(self, tournId: str, group: str) -> Group | None:
    with Session(self._engine) as ses:
      return ses.exec(select(Group).where(Group.tournId == tournId, Group.name == group)).first()
  
  def round(self, **roundId: Unpack[RoundId]) -> Sequence[Game]:
    with Session(self._engine) as ses:
      order: Any = Game.index # order_by's typing is messed up
      stmt = select(Game).where(*round_games(**roundId)).order_by(order)
      return ses.exec(stmt).all()
    
  def round_pgn(self, **roundId: Unpack[RoundId]) -> str:
    with Session(self._engine) as ses:
      order: Any = Game.index
      stmt = select(Game).where(*round_games(**roundId)).order_by(order)
      games = ses.exec(stmt).all()
      tnmt = ses.exec(select_tnmt(roundId['tournId'])).first()
      return export_all(games, tnmt)

  def game_pgn(self, **gameId: Unpack[GameId]) -> FrontendPGN | None:
    with Session(self._engine) as ses:
      game = ses.exec(select_game(**gameId)).first()
      if game and game.pgn:
        return game.pgn
      
  def images(self, **gameId: Unpack[GameId]) -> Sequence[str] | None:
    with Session(self._engine) as ses:
      game = ses.exec(select_game(**gameId)).first()
      if game:
        return [img.descaled_url for img in game.imgs]
      
  @E.do[ReadError]()
  async def post_game(
    self, images: Sequence[bytes],
    descaled_height: int = 768,
    **gameId: Unpack[GameId]
  ):
    if images == []:
      return Left('No images provided')

    id = f'{stringify(**gameId)}_{uuid4()}'

    uploads = []
    imgs = []
    for i, img in enumerate(images):
      mat = vc.decode(img)
      url = f'{id}/{i}.jpg'
      descaled_url = f'{id}/{i}-{descaled_height}.jpg'
      descaled = vc.encode(vc.descale_h(mat, descaled_height), format='.jpg')
      encoded = vc.encode(mat, format='.jpg')
      uploads.extend([
        self._images.insert(url, encoded),
        self._images.insert(descaled_url, descaled)
      ])
      imgs.append(Image(url=url, descaled_url=descaled_url))
    
    E.sequence(await asyncio.gather(*uploads)).unsafe()

    deletions = []
    with Session(self._engine) as ses:
      game = ses.exec(select_game(**gameId)).first()
      if game is None:
        return Left(InexistentItem(detail=f'Game {gameId} not found in DB'))
      for img in game.imgs:
        (await self._images.delete(img.url)).unsafe()
        ses.delete(img)
        deletions.extend([
          self._images.delete(img.url),
          self._images.delete(img.descaled_url)
        ])

      game.imgs = imgs
      game.status = Game.Status.uploaded
      ses.add(game)
      ses.commit()

    E.sequence(await asyncio.gather(*deletions)) # if they don't get deleted, who cares