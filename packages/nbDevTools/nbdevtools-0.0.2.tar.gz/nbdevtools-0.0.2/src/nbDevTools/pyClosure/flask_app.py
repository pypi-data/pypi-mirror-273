UPDATE = '2023-08-16'

from flask import Flask, send_from_directory, Response
import threading
import os
import logging

from flask.logging import default_handler
#from flask import logging

#wz = logging.getLogger('werkzeug')
#print(wz)

from typing import Any

class ListHandler(logging.Handler):
    def __init__(self, lt :list[str]):
        super().__init__()
        self._lt_log :list[str] = lt
        self.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        self.setLevel(logging.INFO)
        
        #https://stackoverflow.com/a/49020171/8234237
        logging.root.handlers = [self] #AQUI APLICA

    def emit(self, record : Any) -> None:
        self._lt_log.append(self.format(record))

class FServer:
    def __init__(self, folder:str) -> None:

        self.lt_log :list[str] = []
        self.lt_error :list[str] = []

        self._handler = ListHandler(self.lt_log) 
        self._app = Flask(__name__)   

        @self._app.route('/<path:filename>') #files/
        def serve_file(filename:str) -> Any:
            try:
                if filename.endswith('.js'):
                    with open(os.path.join(folder,filename), 'r',encoding='utf-8') as f:
                        content = f.read()
                    return Response(content, content_type='application/javascript')
                return send_from_directory(folder, filename)
            except Exception as e:
                self.lt_error.append(f'{e} {filename} ')
            
        def run() -> None:
            self._app.run(port=5000, threaded=True)

        thread = threading.Thread(target=run)
        thread.start()

        