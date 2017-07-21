import logging
import json
import os
import sys
from base64 import b64decode
from argparse import ArgumentParser
from waitress import serve


def ParseArgs():
  parser = ArgumentParser()
  parser.add_argument( '--host', type = str, default = '127.0.0.1',
                       help = 'server host' )
  parser.add_argument( '--port', type = int, default = 0,
                       help = 'server port' )
  parser.add_argument( '--log', type = str, default = 'info',
                       choices = [ 'debug', 'info', 'warning',
                                   'error', 'critical' ],
                       help = 'log level' )
  return parser.parse_args()


def SetUpLogging( log_level ):
  numeric_level = getattr( logging, log_level.upper(), None )
  if not isinstance( numeric_level, int ):
    raise ValueError( 'Invalid log level: {0}'.format( log_level ) )

  # Has to be called before any call to logging.getLogger().
  logging.basicConfig( format = '%(asctime)s - %(levelname)s - %(message)s',
                       level = numeric_level )


def Main():
  args = ParseArgs()

  SetUpLogging( args.log )

  serve( handlers.app,
         host = args.host,
         port = args.port )

if __name__ == "__main__":
  Main()
