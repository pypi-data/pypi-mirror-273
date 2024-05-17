import asyncio
from datetime import timedelta
from sqlmodel import SQLModel
from sqlalchemy import Engine
from dslog import Logger
from haskellian import promise as P
from kv.api import KV
from q.api import ReadQueue, WriteQueue
from scoresheet_models import ModelID
from moveread.core import CoreAPI
from moveread.pipelines.dfy import Input, Result
from ._puller import puller
from ._pusher import pusher

@P.run
async def run_connect(
  Qin: WriteQueue[Input], Qout: ReadQueue[Result], *,
  engine: Engine, tournId: str, model: ModelID,
  output_core: CoreAPI,
  local_images: KV[bytes], online_images: KV[bytes],
  logger = Logger.rich().prefix('[DFY]'),
  polling_interval = timedelta(seconds=30)
):
  
  SQLModel.metadata.create_all(engine)

  tasks = (
    puller(
      Qin, engine, tournId=tournId, polling_interval=polling_interval,
      model=model, logger=logger.prefix('[PULLER]'),
      online_images=online_images, local_images=local_images
    ),
    pusher(Qout, engine, output_core=output_core, images=local_images, tournId=tournId, logger=logger.prefix('[PUSHER]'))
  )
  await asyncio.gather(*tasks)