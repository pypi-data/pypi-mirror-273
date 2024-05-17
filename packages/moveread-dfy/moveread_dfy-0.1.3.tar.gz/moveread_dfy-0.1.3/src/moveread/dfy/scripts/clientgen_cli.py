import os
from argparse import ArgumentParser
from openapi_ts import generate_client
from moveread.dfy import fastapi

def main():

  parser = ArgumentParser()
  parser.add_argument('-p', '--package-path', help="Path to the typescript package's base folder", required=True)
  args = parser.parse_args()

  app = fastapi({}, blobs={}) # type: ignore
  spec = app.openapi()
  path = os.path.abspath(args.package_path)
  generate_client(spec, path)

if __name__ == '__main__':
  main()