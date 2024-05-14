from argparse import ArgumentParser
from scoresheet_models import MODEL_IDS

def main():
  parser = ArgumentParser()
  parser.add_argument('-i', '--input', required=True)
  parser.add_argument('-o', '--output', required=True)
  parser.add_argument('-d', '--database', required=True, help='Database URL')
  parser.add_argument('-t', '--tournament', required=True, help='Tournament ID')
  parser.add_argument('-m', '--model', required=True, choices=MODEL_IDS, help='Model ID')
  parser.add_argument('--protocol', default='sqlite', required=False, choices=['sqlite', 'fs'], help='Protocol used in queues')

  args = parser.parse_args()


  import os
  from dslog import Logger
  input_path = os.path.join(os.getcwd(), args.input)
  output_path = os.path.join(os.getcwd(), args.output)
  proto = args.protocol
  db_url = args.database
  tournId = args.tournament

  logger = Logger.rich().prefix('[DFY CONNECTOR]')
  
  logger(f'Running...')
  logger(f'- Tournament ID: "{tournId}"')
  logger(f'- Database URL: "{db_url}"')
  logger(f'- Queues protocol: "{proto}"')
  logger(f'- Input path: "{input_path}"')
  logger(f'- Output path: "{output_path}"')
  
  from sqlmodel import create_engine
  from moveread.dfy import run_connect
  from moveread.pipelines.dfy import input_queue, output_queue
  
  Qin = input_queue(input_path, protocol=proto)
  Qout = output_queue(output_path, protocol=proto)
  engine = create_engine(db_url)
  run_connect(Qin, Qout, engine=engine, tournId=tournId, logger=logger, model=args.model)

if __name__ == '__main__':
  import sys
  import os
  os.chdir('/home/m4rs/mr-github/modes/dfy/moveread-dfy/')
  sys.argv.extend('-i queues/in -o queues/out -d sqlite:///db.sqlite -t llobregat -m llobregat23'.split(' '))
  main()