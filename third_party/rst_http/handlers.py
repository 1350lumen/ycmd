import contextlib
import logging
import json
import bottle
from bottle import response, request, Bottle

try:
  import httplib
except ImportError:
  from http import client as httplib

# num bytes for the request body buffer; request.json only works if the request
# size is less than this
bottle.Request.MEMFILE_MAX = 1000 * 1024

logger = logging.getLogger( __name__ )
app = Bottle( __name__ )

@app.post( '/healthy' )
def healthy():
  logger.debug( 'received /healthy request' )
  return _JsonResponse( True )


@app.post( '/ready' )
def ready():
  logger.debug( 'received /ready request' )
  return _JsonResponse( True )


@app.post( '/completions' )
def completions():
  logger.debug( 'received /completions request' )
  request_json = request.json
  completions = []
  response = _FormatCompletions(completions)
  return _JsonResponse( response )


@app.post( '/gotodefinition' )
def gotodefinition():
  logger.debug( 'received /gotodefinition request' )
  definitions = []
  response = _FormatDefinitions( definitions )
  return _JsonResponse( response )


def _FormatCompletions( completions ):
  return {
     'completions': [ {
          'module_path': 'path',
          'name':        'name',
          'type':        'type',
          'line':        request_data[ 'line' ],
          'column':      request_data[ 'col' ],
          'docstring':   'docstring',
          'description': 'description',
      }]
  }

  #return {
  #    'completions': [ {
  #        'module_path': completion.module_path,
  #        'name':        completion.name,
  #        'type':        completion.type,
  #        'line':        completion.line,
  #        'column':      completion.column,
  #        'docstring':   completion.docstring(),
  #        'description': completion.description,
  #    } for completion in completions ]
  #}


def _FormatDefinitions( definitions ):
  return {
      'definitions': [ {
          'module_path':       definition.module_path,
          'name':              definition.name,
          'type':              definition.type,
          'in_builtin_module': definition.in_builtin_module(),
          'line':              definition.line,
          'column':            definition.column,
          'docstring':         definition.docstring(),
          'description':       definition.description,
          'full_name':         definition.full_name,
          'is_keyword':        definition.is_keyword
      } for definition in definitions ]
  }


@app.error( httplib.INTERNAL_SERVER_ERROR )
def ErrorHandler( httperror ):
  body = _JsonResponse( {
    'exception': httperror.exception,
    'message': str( httperror.exception ),
    'traceback': httperror.traceback
  } )
  return body


def _JsonResponse( data ):
  response.content_type = 'application/json'
  return json.dumps( data, default = _Serializer )


def _Serializer( obj ):
  try:
    serialized = obj.__dict__.copy()
    serialized[ 'TYPE' ] = type( obj ).__name__
    return serialized
  except AttributeError:
    return str( obj )
