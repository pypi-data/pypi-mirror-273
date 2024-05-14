from typing import Sequence, TypedDict
from enum import StrEnum
from datetime import date
from pydantic import RootModel, Field as PydanticField
from sqlmodel import Field, SQLModel, Relationship
from sqltypes import SpaceDelimitedList, PydanticModel
from chess_pairings import Paired, Unpaired

class Pairing(RootModel):
  root: Paired | Unpaired = PydanticField(discriminator='tag')

class Tournament(SQLModel, table=True):
  tournId: str = Field(primary_key=True)
  name: str
  site: str | None = None
  start_date: date | None = None
  end_date: date | None = None
  groups: Sequence[str] = Field(sa_type=SpaceDelimitedList)

class Group(SQLModel, table=True):
  tournId: str = Field(primary_key=True, foreign_key='tournament.tournId')
  name: str = Field(primary_key=True)
  rounds: Sequence[str] = Field(sa_type=SpaceDelimitedList)
  
class Image(SQLModel, table=True):
  id: int | None = Field(default=None, primary_key=True)
  url: str
  descaled_url: str
  gameId: int = Field(default=None, foreign_key='game.id')

class FrontendPGN(SQLModel):
  moves: Sequence[str] = Field(sa_type=SpaceDelimitedList)
  early: bool | None = None

class PGN(FrontendPGN, table=True):
  gameId: int = Field(default=None, primary_key=True, foreign_key='game.id')

class FrontendGame(SQLModel):
  board: str
  pairing: Pairing = Field(sa_type=PydanticModel(Pairing))
  status: 'Game.Status | None' = None

class Game(FrontendGame, table=True):
  class Status(StrEnum):
    uploaded = 'uploaded'
    doing = 'doing'
    done = 'done'

  id: int | None = Field(default=None, primary_key=True)
  tournId: str
  group: str
  round: str
  index: int
  """Boards may have out of whack names (e.g. in team tournaments "1.3"). This is the order you'd see in chess-results"""
  imgs: list[Image] = Relationship()
  pgn: PGN | None = Relationship()
  
class GroupId(TypedDict):
  tournId: str
  group: str

class RoundId(GroupId):
  round: str

class GameId(RoundId):
  board: str

def gameId(tournId: str, group: str, round: str, board: str) -> GameId:
  return GameId(tournId=tournId, group=group, round=round, board=board)

def roundId(tournId: str, group: str, round: str) -> RoundId:
  return RoundId(tournId=tournId, group=group, round=round)
  
class Token(SQLModel, table=True):
  id: int | None = Field(default=None, primary_key=True)
  token: str
  tournId: str
  
__all__ = [
  'Game', 'GameId', 'Image', 'Tournament', 'PGN', 'Pairing', 'Token'
]