from typing import Sequence, Literal, Annotated
import os
from fastapi import FastAPI, Response, File, Request, status
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from dslog import Logger
from dslog.uvicorn import setup_loggers_lifespan, DEFAULT_FORMATTER, ACCESS_FORMATTER
from kv.api import LocatableKV
from ..types import FrontendGame, gameId, roundId, Tournament, Group, FrontendPGN
from .sdk import DFY

def fastapi(
  sdk: DFY, *, images_path: str | None = None,
  blobs: LocatableKV[bytes],
  logger = Logger.click().prefix('[DFY API]')
):
  
  app = FastAPI(
  generate_unique_id_function=lambda route: route.name,
    lifespan=setup_loggers_lifespan(
      access=logger.format(ACCESS_FORMATTER),
      uvicorn=logger.format(DEFAULT_FORMATTER),
    )
  )
  
  app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
  )

  if images_path is not None:
    app.mount('/images', StaticFiles(directory=images_path))

  @app.get('/authorize/{tournId}', responses={ 401: {}, 200: {} })
  def authorize(token: str, tournId: str):
    authed = sdk.authorize(token, tournId)
    return Response(status_code=200 if authed else status.HTTP_401_UNAUTHORIZED)

  @app.get('/')
  def tournaments() -> Sequence[Tournament]:
    return sdk.tournaments()

  @app.get('/{tournId}', responses={ 404: {}, 200: { 'model': Tournament }})
  def tournament(tournId: str, r: Response) -> Tournament | None:
    tnmt = sdk.tournament(tournId)
    if tnmt is None:
      r.status_code = status.HTTP_404_NOT_FOUND
    return tnmt
  
  @app.get('/{tournId}/{group}', responses={ 404: {}, 200: { 'model': Group }})
  def group(tournId: str, group: str, r: Response) -> Group | None:
    grp = sdk.group(tournId, group)
    if grp is None:
      r.status_code = status.HTTP_404_NOT_FOUND
    return grp

  @app.get('/{tournId}/{group}/{round}.pgn', response_model=str)
  def round_pgn(tournId: str, group: str, round: str):
    pgn = sdk.round_pgn(**roundId(tournId, group, round))
    return Response(content=pgn, media_type='application/x-chess-pgn', headers={
      'Content-Disposition': f'attachment; filename={tournId}_{group}_{round}.pgn'
    })
  
  @app.get('/{tournId}/{group}/{round}')
  def round(tournId: str, group: str, round: str) -> Sequence[FrontendGame]:
    return sdk.round(**roundId(tournId, group, round))
  

  @app.get('/{tournId}/{group}/{round}/{board}/pgn', responses={ 404: {}, 200: { 'model': FrontendPGN }})
  def game_pgn(tournId: str, group: str, round: str, board: str, r: Response) -> FrontendPGN | None:
    pgn = sdk.game_pgn(**gameId(tournId, group, round, board))
    if pgn is None:
      r.status_code = status.HTTP_404_NOT_FOUND
    return pgn
  
  @app.get('/{tournId}/{group}/{round}/{board}/images', responses={ 404: {}, 200: { 'model': Sequence[str] }})
  def images(tournId: str, group: str, round: str, board: str, req: Request, res: Response) -> Sequence[str] | None:
    urls = sdk.images(**gameId(tournId, group, round, board))
    if urls is None or len(urls) == 0:
      res.status_code = status.HTTP_404_NOT_FOUND
      return None
    
    if images_path is not None:
      path = os.path.join(str(req.base_url), 'images')
      return [os.path.join(path, url) for url in urls]
    else:
      return [blobs.url(url) for url in urls]
  
  @app.post('/{tournId}/{group}/{round}/{board}', responses={
    401: dict(model=Literal['UNAUTHORIZED']),
    200: dict(model=Literal['OK']),
    500: dict(model=Literal['ERROR'])
  })
  async def post_game(
    tournId: str, group: str, round: str, board: str, token: str,
    images: Annotated[list[bytes], File()], r: Response, 
  ) -> Literal['OK', 'UNAUTHORIZED', 'ERROR']:
  
    if not sdk.authorize(token, tournId):
      r.status_code = status.HTTP_401_UNAUTHORIZED
      return 'UNAUTHORIZED'
    
    gid = gameId(tournId, group, round, board)
    res = await sdk.post_game(images, **gid)
    if res.tag == 'left':
      logger(f'Error posting game {gid}:', res.value, level='ERROR')
      r.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
      return 'ERROR'
    
    return 'OK'  
  
  return app