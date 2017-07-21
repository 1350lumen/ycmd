from webtest import TestApp
from rst_http import handlers
import bottle

bottle.debug( True )

def test_healthy():
  app = TestApp( handlers.app )
  assert app.post( '/healthy' ).status_int == 200
