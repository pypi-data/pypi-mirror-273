from flask import Flask, send_from_directory, Response, request, Request
#from werkzeug.wrappers import Request
import requests
import threading
import os
import logging
from typing import Any, Optional, cast, Callable
import sys
import importlib
import re
import time
import inspect

from flask.logging import default_handler
#from flask import logging

#wz = logging.getLogger('werkzeug')
#print(wz)


from IPython.display import  display
from IPython.core.display import HTML
import IPython

from string import Template

from nbDevTools import nbCom as nbCom
UPDATE = '2023-10-01'



def reload() -> None:
    lt_reload = []
    for k,v in sys.modules.items():
        if k.startswith(__name__):
            lt_reload.append(v)           
        
    for m in lt_reload:
        importlib.reload(m)


class IPY_JS_STATUS:
    def __init__(self) -> None:
        self.status_pycode = ''
        self.status_resp_yes = ''
        self.text_on = ''
        self.text_off = ''
        self.wait_ms = 2000
        self.code_on = ''
        self.code_off = ''

    def html_code(self) ->str:
        
        if ('"' in  self.status_pycode) and ("'" in  self.status_pycode):
            raise RuntimeError('Usar apenas \' ou " ')
        self.status_pycode = self.status_pycode.replace('"',"'") # re.sub(r"['\"]", '`', self.status_pycode)

        #WORK_FUNCTION = 'ipyjs20231002'
        #KERNEL_RUN = 'ipykernel20231002'
        #'WORK_FUNCTION': WORK_FUNCTION, 'KERNEL_RUN': KERNEL_RUN,

        #HTML_FILE = r'C:\Users\Christoph Cury\source\2023\pydev_tools\src\nbCom\flask_button_off.html'
        #HTML = open(HTML_FILE,'r').read()
        
        JS_FILE = r'C:\Users\Christoph Cury\source\2023\pydev_tools\src\nbCom\flask_button_off.js'
        with open(JS_FILE, 'r') as file:
            lines = file.readlines()
            filtered_lines = [line for line in lines if not line.strip().startswith('import')]

        JS_CODE = ''.join(filtered_lines)

        #JS_CODE = (el)=>{console.log(el);}

        HTML = f'''
        <div><img src="data:image/gif;base64,R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw==" 
        style="display:none" 
        onload="({JS_CODE})(this)"
        data-scode="$status_pycode" 
        data-ry="$status_resp_yes" 
        data-ty="$text_on" 
        data-tn="$text_off" 
        data-con="$code_on" 
        data-cof="$code_off" 
        data-wms="$wait_ms">
        <button onclick="({JS_CODE})(this)">$text_on</button></div>
        '''



        
        #with open(r'C:\Users\Christoph Cury\source\2023\pydev_tools\src\nbCom\flask_button_off.html', "r") as file:
        template_js = Template(HTML)
        dic = {
                'text_on' : self.text_on, 'text_off': self.text_off , 
                'status_pycode': self.status_pycode, 'wait_ms':self.wait_ms,
                'code_on':self.code_on, 'code_off':self.code_off,
                'status_resp_yes':self.status_resp_yes }
        html_code = template_js.safe_substitute(dic)
        
        #template_html = Template(HTML)
        #dic['JS_CODE'] = html_code
        #html_code = template_html.safe_substitute(dic)
        #print(js_code)
        
        out_FILE = r'C:\Users\Christoph Cury\source\2023\pydev_tools\src\nbCom\flask_button_off_OUTPUT.html'
        open(out_FILE,'w').write(html_code)

        #html_code = '<h1>HELLOW WORLD</h1>'
        return html_code
    

class ListHandler(logging.Handler):
    def __init__(self, lt :list[str]):
        super().__init__()
        self._lt_log :list[str] = lt
        self.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        self.setLevel(logging.INFO)
        
        #https://stackoverflow.com/a/49020171/8234237
        logging.root.handlers = [self] #AQUI APLICA

    def emit(self, record : logging.LogRecord ) -> None: #uso isso? 2024-03-27
        self._lt_log.append(self.format(record))

FROUTE = Callable[[Request], Optional[Response]]

class FServer:
    """
    EXEMPLO:
        import os;import nbFlask;nbFlask.reload()
        port, path = 5000, os.path.abspath(os.path.join(os.getcwd(),'../js_dev/src'))
        nbFlask.FServer(path,port, globals());

        http://127.0.0.1/  host é 127.0.0.1

    """  
    _VARROOT = 'fserv'
    
    def __init__(self, folder:str, port: int = 5000,
                 glob : dict[str,Any] = {}, 
                 route : Optional[FROUTE] = None, 
				 modulo : Optional[str] = None, #PARA CONFERIR SE ESTÁ ATIVO, VERIFICA DENTRO DO MÓDULO
				 host : Optional[str] = None,
                  #glob_debug : Optional[dict] = None 
                  ) -> None:
        
        '''
        SE TEM MODULO, O GLOB É O __dict__ do módulo. Cria varável com nome do port: self._VARNAME = f'{self._VARROOT}{port}'
        '''
        
        #self._html_shutdown_button()
        #return

        self.lt_log :list[str] = []
        self.lt_error :list[str] = []
        self.lt_route : list[FROUTE] = []
        if route:
            self.lt_route.append(route)
        self.modulo = modulo

        self.evento_atualizacao = threading.Event()

        if modulo:
            glob = sys.modules.get(modulo).__dict__

        self._VARNAME = f'{self._VARROOT}{port}'
        
        if self._VARNAME in glob:
            cast( FServer, glob[self._VARNAME]).shutdown() #desiga anterior
            
        glob[self._VARNAME] = self
        self.glob = glob
        #else:
        #    self._VARNAME = 'n/d'

        time.sleep(0.5)
        self._html_shutdown_button()


        self.port = port
        self._handler = ListHandler(self.lt_log) 
        self._app = Flask(__name__)   
        self._app.add_url_rule('/shutdown', view_func=self._shutdown_server)        
        self.host = host

        @self._app.route('/<path:filename>', methods=['GET', 'POST', 'DELETE', 'PATCH']) #files/ #'GET', 
        def serve_file(filename:str) -> Response:
            #fp = os.path.join(folder, filename)
            #return Response(f'{fp} exit = {os.path.exists(fp)}', mimetype='text/plain'  )
            try:
                for route in self.lt_route:
                    resp = route(request)
                    if resp is not None:
                        return resp                
                if filename.endswith('.js'):
                    with open(os.path.join(folder,filename), 'r',encoding='utf-8') as f:
                        content = f.read()
                    return Response(content, content_type='application/javascript')
                return send_from_directory(folder, filename)
            except Exception as e:
                self.lt_error.append(f'{e} {filename} ')
                return  Response(f'ERRO\n{e} {filename}', mimetype='text/plain')
            
        def run() -> None:
            self._app.run(port=port, threaded=True, host=host)

        thread = threading.Thread(target=run)
        thread.start()
    
        
    def _shutdown_server(self) -> Response:

        #deprecated - solução nova: https://stackoverflow.com/a/68886060/8234237 
        func = request.environ.get('werkzeug.server.shutdown')
        if func is None:
            raise RuntimeError('Not running with the Werkzeug Server')
        func()         #UserWarning: The 'environ['werkzeug.server.shutdown']' function is deprecated and will be removed in Werkzeug 2.1.

        try:
            del self.glob[self._VARNAME]
        except Exception: ...

        self.evento_atualizacao.set()
        return Response('SERVIDOR DESLIGADO', mimetype='text/plain')

    def __repr__(self) -> str:
        return str(self.__dict__)
    
    def shutdown(self) -> None:
        
        threading.Thread(target= lambda: requests.get(f'http://127.0.0.1:{self.port}/shutdown')).start()
        self.evento_atualizacao.wait()

        #self.glob_debug['sd'] = {'n': self._n}
        #try:
        #    requests.get(f'http://127.0.0.1:{self.port}/shutdown')
        #    del self.glob[self._VARNAME]
        #except Exception as e: 
        #    self.lt_error.append(e)
        #    self.glob_debug['sd']['e'] = e

    
    def _html_shutdown_button(self) -> None:

        js= IPY_JS_STATUS()
        
        if self.modulo is None:
            js.status_pycode = f'1 if "{self._VARNAME}" in globals() else 0'
            js.code_on = f'{self._VARNAME}.shutdown();del {self._VARNAME};200'
        else:
            def flask_shutdown() -> int:
                import sys
                try:
                    glob = sys.modules.get('$MODULE').__dict__
                    glob['$VARNAME'].shutdown()
                    del glob['$VARNAME']
                except: pass
                return 200
    
            def flask_check() -> int:
                import sys
                try:
                    if f'$VARNAME' in sys.modules.get('$MODULE').__dict__:
                        return 1
                except: pass
                return 0

            dic = { 'VARNAME':self._VARNAME, 'MODULE':self.modulo }
            #js.status_pycode = Template(inspect.getsource(flask_check)).safe_substitute(dic) + ";flask_check()"
            js.status_pycode = nbCom.extrair_corpo_funcao(flask_check ,dic=dic) + f'\n{flask_check.__name__}()'
            js.code_on = nbCom.extrair_corpo_funcao(flask_shutdown ,dic=dic) + f'\n{flask_shutdown.__name__}()'
            #js.code_on = Template(inspect.getsource(flask_shutdown)).safe_substitute(dic) + ";flask_shutdown()"

            #js.status_pycode = f'''import sys;1 if "{self._VARNAME}" in sys.modules.get("{self.modulo}").__dict__.keys()  else 0'''
            #js.code_on = f"    def run():\n        import sys\n        try:\n            glob = sys.modules.get('ploft').__dict__\n            glob['{self._VARNAME}'].shutdown()\n            del glob['{self._VARNAME}']\n        except: pass\n        return 200\n"
            #js.code_on = f'''import sys;glob = sys.modules.get('ploft').__dict__; glob['{self._VARNAME}'].shutdown(); del glob['{self._VARNAME}'];200'''
        ''' 200 no final de js.code_on é para retornar alguma coisa.
            Se não retornar vai para o timeout na lógica que fiz em javascript, não completa
            existe possibilidade de usar como indicador o status idle, mas teria que mudar lógica
        '''
        
        js.status_resp_yes = '1'
        js.code_off = ''
        js.text_on = 'Desligar Servidor'
        js.text_off = 'Servidor Desligado'

        html = js.html_code()

        display(HTML(html))
        #display(HTML('<span></span>'))
        #print('123')




def fserv(folder:str, port: int = 5000, 
        glob : dict[str,Any] = {}, 
        route : Optional[FROUTE] = None,
        modulo : Optional[str] = None, #PARA CONFERIR SE ESTÁ ATIVO, VERIFICA DENTRO DO MÓDULO
		host : Optional[str] = None, 
        #glob_debug : Optional[dict] = None
        ) -> tuple[str,FServer]:
    x = FServer(folder,port,glob, route=route, modulo=modulo, host=host)
    return (x._VARNAME,x)
