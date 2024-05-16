from nbDevTools.cmd_shell import SHELL
from nbDevTools.pyClosure.flask_app import FServer
from nbDevTools.pyClosure.tools import modificar_e_gravar_arquivo , path

from nbDevTools import reload as _reload
reload = lambda : _reload(__name__)

#from pyclosure.examples import *

__all__ = ["SHELL", "reload", "modificar_e_gravar_arquivo" , 'path' ]

