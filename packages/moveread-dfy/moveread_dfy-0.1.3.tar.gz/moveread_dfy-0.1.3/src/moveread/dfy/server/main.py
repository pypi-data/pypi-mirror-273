import os
import uvicorn
from dslog import Logger
from kv.api import LocatableKV
from moveread.dfy import fastapi, DFY
from sqlalchemy import Engine

def run_api(
  images: LocatableKV[bytes],
  engine: Engine, *,
  images_path: str | None = None,
  port: int = 8000,
  host: str = '0.0.0.0',
  logger = Logger.click().prefix('[DFY API]')
):
  if images_path is not None:
    os.makedirs(images_path, exist_ok=True)
  sdk = DFY(images=images, engine=engine)
  app = fastapi(sdk, blobs=images, images_path=images_path, logger=logger)
  uvicorn.run(app, port=port, host=host)