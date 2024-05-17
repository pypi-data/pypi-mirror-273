import os
from argparse import ArgumentParser

def main():
  parser = ArgumentParser()
  group = parser.add_mutually_exclusive_group()
  group.add_argument('--images', type=str, help='Local path to images')
  group.add_argument('--blobs', type=str, help='Azure Blob connection string')

  parser.add_argument('--db', required=True, type=str, help='DB URL')

  parser.add_argument('-p', '--port', default=8000, type=int)
  parser.add_argument('--host', default='0.0.0.0', type=str)


  args = parser.parse_args()
  db = args.db

  from dslog import Logger, formatters
  logger = Logger.stderr().format(formatters.click)

  logger(f'Running API...')
  logger(f'- DB URL: "{db}"')

  if args.images:
    images_path = os.path.join(os.getcwd(), args.images)
    logger(f'- Images path: "{images_path}"')
    from kv.fs import FilesystemKV
    images = FilesystemKV[bytes](images_path)
  else:
    images_path = None
    from kv.azure.blob import BlobKV
    images = BlobKV[bytes].from_conn_str(args.blobs)
    logger(f'- Azure Blob account: {images.client.account_name}')

  from sqlalchemy import create_engine
  from moveread.dfy import run_api
  engine = create_engine(db)
  run_api(images, engine, images_path=images_path, port=args.port, host=args.host, logger=logger)

if __name__ == '__main__':
  import sys
  from dotenv import load_dotenv
  load_dotenv()
  SQL_CONN_STR = os.environ['SQL_CONN_STR']
  BLOB_CONN_STR = os.environ['BLOB_CONN_STR']
  sys.argv.extend(f'--blobs {BLOB_CONN_STR} --db {SQL_CONN_STR}'.split(' '))
  main()