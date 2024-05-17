from scoresheet_models import MODEL_IDS
from argparse import ArgumentParser

def main():
  parser = ArgumentParser()
  parser.add_argument('-i', '--input', required=True)
  parser.add_argument('-o', '--output', required=True)
  parser.add_argument('-b', '--base-path', required=True)
  parser.add_argument('-d', '--db', required=True, help='Database URL')
  parser.add_argument('-t', '--tournament', required=True, help='Tournament ID')
  parser.add_argument('-m', '--model', required=True, choices=MODEL_IDS, help='Model ID')
  parser.add_argument('--protocol', default='sqlite', required=False, choices=['sqlite', 'fs'], help='Protocol used in queues')
  parser.add_argument('--images', type=str, help='Local path to images')
  parser.add_argument('--blobs', type=str, help='Azure Blob connection string')
  parser.add_argument('--core', type=str, help='Path to output core')

  args = parser.parse_args()


  import os
  from dslog import Logger
  input_path = os.path.join(os.getcwd(), args.input)
  output_path = os.path.join(os.getcwd(), args.output)
  base_path = os.path.join(os.getcwd(), args.base_path)
  proto = args.protocol
  db_url = args.db
  tournId = args.tournament
  images_path = os.path.join(os.getcwd(), args.images)
  core_path = os.path.join(os.getcwd(), args.core)
  
  logger = Logger.click().prefix('[DFY]')
  logger(f'Running...')
  logger(f'- Tournament ID: "{tournId}"')
  logger(f'- Database URL: "{db_url}"')
  logger(f'- Images path: "{images_path}"')
  logger(f'- Output core path: "{core_path}"')

  
  logger(f'- Queues protocol: "{proto}"')
  logger(f'- Input path: "{input_path}"')
  logger(f'- Internal path: "{base_path}"')
  logger(f'- Output path: "{output_path}"')
  

  if args.blobs.startswith('.'):
    from kv.fs import FilesystemKV
    blobs = os.path.join(os.getcwd(), args.blobs)
    online_images = FilesystemKV[bytes](blobs)
    logger(f'- Local blobs: {blobs}')
  
  else:
    from kv.azure.blob import BlobKV
    online_images = BlobKV[bytes].from_conn_str(args.blobs)
    logger(f'- Azure Blob account: {online_images.client.account_name}')
  
  from sqlmodel import create_engine
  from kv.fs import FilesystemKV
  from moveread.dfy import run_connect
  from moveread.pipelines.dfy import run_local, input_queue, output_queue
  from multiprocessing import Process
  from moveread.core import CoreAPI
  local_images = FilesystemKV[bytes](images_path)
  core = CoreAPI.at(core_path)

  Qin = input_queue(input_path, protocol=proto)
  Qout = output_queue(output_path, protocol=proto)
  engine = create_engine(db_url)
  ps = (
    Process(
      target=run_connect, args=(Qin, Qout), kwargs=dict(
        engine=engine, tournId=tournId, logger=logger.prefix('[I/O]'), model=args.model,
        local_images=local_images, online_images=online_images, output_core=core
      )
    ),
    Process(
      target=run_local, args=(Qin, Qout), kwargs=dict(
        base_path=base_path, images=local_images,
        images_path=images_path, logger=logger
      )
    ),
  )
  for p in ps:
    p.start()
  for p in ps:
    p.join()

if __name__ == '__main__':
  import sys
  import os
  from dotenv import load_dotenv
  path = '/home/m4rs/mr-github/modes/moveread-dfy/infra/doer/local'
  os.makedirs(path, exist_ok=True)
  os.chdir(path)
  load_dotenv()

  SQL_CONN_STR = os.environ['SQL_CONN_STR']
  # SQL_CONN_STR = 'sqlite:////home/m4rs/mr-github/modes/moveread-dfy/local-db/db.sqlite'
  BLOB_CONN_STR = os.environ['BLOB_CONN_STR']
  # BLOB_CONN_STR = '../../../local-db/images'
  blobs = ''
  args = f'-i queues/in -o queues/out -b queues/internal \
      -t llobregat23 -m llobregat23 \
      --db {SQL_CONN_STR} \
      --blobs {BLOB_CONN_STR} \
      --core core \
      --images images'.replace('\n', '').split(' ')
  args = [arg for arg in args if arg]
  sys.argv.extend(args)
  main()