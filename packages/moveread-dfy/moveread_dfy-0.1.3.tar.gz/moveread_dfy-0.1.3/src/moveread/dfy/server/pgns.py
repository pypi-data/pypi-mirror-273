from typing import Iterable
from chess_utils import PGNHeaders, export_pgn
from ..types import Game, Tournament

def export(game: Game, tnmt: Tournament | None = None) -> str | None:
  pair = game.pairing.root
  if game.pgn is None or pair.tag == 'unpaired':
    return None
  site = tnmt and tnmt.site
  event = tnmt and tnmt.name
  headers = PGNHeaders(
    Event=event, Site=site, White=pair.white, Black=pair.black,
    Round=f'{game.round}.{game.board}', Result=pair.result,
  )
  comment = '[...]' if game.pgn.early else None
  return export_pgn(game.pgn.moves, headers, comment)

def export_all(games: Iterable[Game], tnmt: Tournament | None = None) -> str:
  return '\n\n'.join(pgn for game in games if (pgn := export(game, tnmt)) is not None)