from ycmd.completers.rst.rst_completer import RstCompleter

def GetCompleter( user_options ):
  return RstCompleter( user_options )
