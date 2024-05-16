import os
#from nbTools.cmd_shell import SubShell
from nbDevTools import reload as _reload
#from pyclosure.tool_shell import  SHELL
from nbDevTools import SHELL
from datetime import datetime

PACKAGE_NAME = __name__.split('.')[0]
REPOSITORY_NAME = 'pydev_tools'

reload = lambda : _reload(PACKAGE_NAME)

def code_project(code : bool = False, explorer: bool = False, start : bool = False) -> None:
    caminho_pasta = r'"..\"'
    if explorer: os.system(f'explorer "{caminho_pasta}"')
    if code: os.system(f'code "{caminho_pasta}"')
    if start: os.system(f'start "{caminho_pasta}"') # cmd prompt  


def mypy() -> None:

    s = SHELL()

    s.path_upto(REPOSITORY_NAME)    
    s.cmd(F'mypy src --strict') #file_name =  __file__.split(os.path.sep)[-1] #scripts\\{file_name}
    s.waiting_dots(lambda : str(datetime.now()) )

def stubgen() -> None:    
    s = SHELL()
    
    rd = 'rd /s /q'
    mv = 'move'
    if os.name == 'nt':...
    else: #linux
        rd = 'rm -rf'
        move = 'mv'

    s.path_upto(REPOSITORY_NAME)
    s.cmd(f'{rd} "src/{PACKAGE_NAME}-stubs"') #bindfiles
    s.cmd(f'stubgen src/{PACKAGE_NAME}')
    s.cmd(f'{mv} out/{PACKAGE_NAME} src/{PACKAGE_NAME}-stubs')
    s.cmd(f'{rd} "out"') 
    s.waiting_dots('')