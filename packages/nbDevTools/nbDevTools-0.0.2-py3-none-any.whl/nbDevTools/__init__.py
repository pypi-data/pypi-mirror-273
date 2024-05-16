import sys
import importlib
from typing import Union, Any
#from nbTools.cmd_shell import SubShell

from nbDevTools.cmd_shell import SHELL

__version__ = "0.0.2"

def reload(module__name__ : Union[str, list[str]] ) -> Any:
    
    lt_names : list [str] = []
    if isinstance(module__name__,list):
        lt_names.extend(module__name__)
    else:
        lt_names.append(module__name__)
    
    ret = None
    lt_reload = []
    for k,v in sys.modules.items():
        for n in lt_names:
            if k.startswith(n):
                lt_reload.append((k,v))
                #print(k,'yes')
            
                
    for k,m in lt_reload:
        ri = importlib.reload(m)
        if k == module__name__:
            ret = ri

    return ret


def get_site_packages() -> dict[str,Any]:
    import site
    import sys
    import distutils.sysconfig

    #2023-07-18 passar stubs do binder para site-packages
    
    return { 
        'user-packages' : site.getusersitepackages(), #C:\Users\Christoph Cury\AppData\Roaming\Python\Python39\site-packages
        'root-packages' : distutils.sysconfig.get_python_lib(), #C:\ProgramData\Anaconda3\Lib\site-packages
            'packages' : [f for f in sys.path if f.endswith('packages')] 
    }


__all__ = ['reload','SHELL','get_site_packages']