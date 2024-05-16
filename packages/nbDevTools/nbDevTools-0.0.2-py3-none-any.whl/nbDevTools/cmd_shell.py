
from __future__ import annotations
import os
import re
from datetime import datetime,timedelta
from IPython.display import display, clear_output
#import source_swe as swe
from typing import Callable,Any, Union, TextIO, cast, Optional, Literal, Tuple #, TypeVar, ForwardRef,Protocol, runtime_checkable
import ipywidgets as widgets # type: ignore

import sys

import subprocess
import threading
import io
import re
import time
from queue import Queue

TIME_ERROR_LINE = tuple[datetime,bool,str]
TEL_CALL = Callable[[list[TIME_ERROR_LINE]],None]

class TEL_COL():
    DT : int = 0
    ERROR : int = 1
    TEXT : int = 2

class SHELL:   
    
    # Q = cast(queue.Queue[ WT_TUPLE ],None)

    def __init__(self) -> None:
        
        self._bAlive = True
        self._waiting_dots = True
        self._task_completed = threading.Event()
        self._task_completed.set()

        self._wmsg : Union[str,Callable[[],str],None] = None

        self._qcmd : Queue[tuple[str,TEL_CALL]] = Queue()        
        self._curr_cmd : Optional[tuple[str,TEL_CALL]] = None

        self._lt_trheads : list[threading.Thread] = []

        #LEGADO 2024-05-15 - MANTER?
        self._lt : list[TIME_ERROR_LINE] = []        
        self._cmd_lt :list[TIME_ERROR_LINE]  = []

        self.output = widgets.Output()
        display(self.output) 

        self._process : subprocess.Popen[Any]
        self._init_process()

    def __del__(self) -> None:
        self.end()

    def end(self) -> None:
        self._bAlive = False
        self._process.terminate()
        self._qcmd.put_nowait(('',SHELL._log_print))
        for t in self._lt_trheads:
            t.join()
        self._lt_trheads[:] = []
        self.clear_output()
        
    def clear_output(self) -> None:
        with self.output:
            clear_output(wait=False)

    def _init_process(self) -> None:

        bash = 'cmd.exe'
        if os.name == 'nt':...
        else: #linux
            bash = 'bash'

        self._process = subprocess.Popen(bash, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8', errors='replace')

        # Iniciar thread para ler a saída
        t0 = threading.Thread(target= self._loop_cmd )
        t0.start()  
        
        t1 = threading.Thread(target= self._loop_pipe, args=( self._process.stdout,False))
        t1.start()

        t2 = threading.Thread(target= self._loop_pipe, args=( self._process.stderr,True))
        t2.start()        
        self._lt_trheads[:] = [t0,t1,t2]
    
    def _loop_pipe(self, pipe : io.TextIOWrapper, error:bool) -> None:
        while self._bAlive:
            line = pipe.readline()

            if line:
                rm = re.match('(\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}\.\d{6})([i|f])',line)                    
                if rm:
                    if rm[2] == 'i':
                        self._cmd_lt = []
                        if self._waiting_dots:
                            self._waiting_dots_func()         
                    
                    elif rm[2] == 'f':
                        
                        if self._curr_cmd:
                            self._log_exe(self._cmd_lt, self._curr_cmd[1])

                        else:...

                        if self._qcmd.qsize() == 0:
                            msg = self._wmsg
                            if isinstance(msg, str):
                                print(f'\r{msg}')
                            elif callable(msg):
                                tmsg = msg()
                                print(f'\r{tmsg}')
                            self._wmsg = None

                        self._task_completed.set()
                else:
                    self._cmd_lt.append( (datetime.now(),error,line))

                self._lt.append( (datetime.now(),error,line))
            else:
                break

    def _loop_cmd(self) -> None:
        while True:
            self._task_completed.wait()
            tuple_cmd = self._qcmd.get()
            if not self._bAlive:
                break            

            self._curr_cmd = tuple_cmd
            
            self._task_completed.clear()
            tnow = f'{datetime.now()}'
                
            if self._process.stdin is not None: 
                self._process.stdin.write(f'echo {tnow}i & {tuple_cmd[0]} & echo {tnow}f\n') 
                self._process.stdin.flush()    

    @staticmethod
    def _log_print( log:list[TIME_ERROR_LINE] ) -> None:
        first_line = True
        for i in log:
            if i[TEL_COL.ERROR]:
                #\x1b[30m: Preto, 31m: Vermelho, 32m: Verde, 33m: Amarelo, 34m: Azul, 35m: Magenta (ou Roxo), 36m: Ciano (ou Azul-água), 37m: Branco
                print(f"\x1b[35m{i[TEL_COL.TEXT]}\x1b[0m",end='')
            else:
                if first_line:
                    sys.stdout.write('\r' + ' ' * 100)
                    sys.stdout.write('\r')
                    first_line = False
                print(f'{i[TEL_COL.TEXT]}',end='')    

    def _log_exe(self, log:list[TIME_ERROR_LINE] , fun : TEL_CALL) -> None:
        with self.output:
            fun(log)

    def cmd(self, txt:str, func : Optional[TEL_CALL] = None) -> None: #, show:bool = True, f : Optional[Callable[[SHELL, list[TIME_ERROR_LINE]],None]] = None
        if func is None:
            func = SHELL._log_print
        self._qcmd.put_nowait((txt,func))
    
        
    def path_set(self,folder:str) -> None:
        folder = os.path.normpath(folder)
        self.cmd(f'cd\\ & cd {folder}')

    def path_upto(self,folder:str) -> None:
        #COM BASE EM os.gecwd

        cwd = os.getcwd()
        lt = cwd.split(os.sep)
        n = len(lt)
        while n> 0 and lt[n-1] != folder:
            n-=1
        lt = lt[0:n]
        p = os.sep.join(lt)
        self.cmd(f'cd\\ & cd {p}') 
    
    def getcwd_cback(self, cback : Callable[[str],None]) -> None:
        #CONSULTOANDO O PROMPT
        def ret(log: list[TIME_ERROR_LINE]) -> None:
            cback('\n'.join([ i[TEL_COL.TEXT] for i in log ]))  # type: ignore      
        self.cmd('cd',ret)

    def path_upto_cback(self,folder:str, *, link : Optional[Callable[[SHELL],None]] = None) -> None:
        #COM BASE EM CONSULTA AO PROMPT INTERNO
        def set_dir(cwd : str) -> None:
            lt = cwd.split(os.sep)
            n = len(lt)
            while n> 0 and lt[n-1] != folder:
                n-=1
            lt = lt[0:n]
            p = os.sep.join(lt)
            self.cmd(f'cd\\ & cd {p}')
            if link:
                link(self)
        self.getcwd_cback( set_dir )

    def waiting_dots(self, msg: Union[str,Callable[[],str],None] = None) -> None:
        self._waiting_dots = True
        self._wmsg = msg

    def _waiting_dots_func(self) -> None:

        def capsula_dots() -> None:
            i = 0 
            with self.output:
                while self._bAlive and (not self._task_completed.is_set()): #self._bAlive and not event.is_set():
                    sys.stdout.write('\r' + '.' * i + '   ')  # The extra spaces are to clear any remaining dots
                    sys.stdout.flush()
                    #time.sleep(0.2)
                    self._task_completed.wait(0.2)
                    i=i+1
                    if i > 3:
                        i=0
        threading.Thread(target= capsula_dots).start()




# import os
# import subprocess
# import threading
# import queue
# import time

# import ipywidgets as widgets # type: ignore
# from IPython.display import display

# # Definir uma fila para comunicação entre threads e um evento para parar a execução

# class SubShell:

#     def __init__(self) -> None:
#         self.output_queue : queue.Queue[str] = queue.Queue()
#         self.commands_queue : queue.Queue[str] = queue.Queue()
#         self.stop_event = threading.Event()
#         self.original_directory = os.getcwd()
        
#         self.exec_thread = threading.Thread(target=self._loop_commands)
#         self.print_thread = threading.Thread(target=self._loop_print)
#         self.output = widgets.Output()
#         display(self.output)

#         #time.sleep(0.5)
#         self.exec_thread.start()
#         #time.sleep(0.5)
#         self.print_thread.start() 
#         #time.sleep(0.5)
        

        

#     def __del__(self) -> None:
#         self.stop_execution()

#     def run_commands(self, commands: list[str]) -> None:
#         for c in commands:
#             self.commands_queue.put(c) # put ou put_nowait ?? 

#     def run_command(self, command: str) -> None:
#         self.commands_queue.put(command) # put ou put_nowait ?? 

#     def stop_execution(self) -> None:
#         self.stop_event.set()

#     def path_upto(self, folder: str ) -> None:
#         cwd = self.original_directory #.lower() #os.getcwd()
#         #folder = folder.lower()
#         lt = cwd.split(os.sep)
#         if folder not in lt:
#             self.output_queue.put(f"A pasta '{folder}' não existe no caminho atual. {cwd}\n")
#             return        
#         n = len(lt)
#         while n> 0 and lt[n-1] != folder:
#             n-=1
#         lt = lt[0:n]
#         p = os.sep.join(lt)
#         os.chdir(p)

#     def _loop_print(self) -> None:
#         with self.output:
#             while True: #not self.stop_event.is_set():  #.exec_thread.is_alive():
#                 try:
#                     message = self.output_queue.get_nowait()
#                     print('\r' + message, end='', flush=True)
#                 except queue.Empty:
#                     continue
#                 if self.stop_event.is_set():
#                     print('saindo comando')
                    
#                 time.sleep(0.1) 
#             print('fim loop')
    
#     def _animate_dots(self, stop_event : threading.Event) -> None:
#         """Animação de três pontos enquanto espera"""
#         while not stop_event.is_set() and not self.stop_event.is_set():
#             for dots in ['.   ', '.. ', '...  ']:
#                 self.output_queue.put(f'\r{dots}')
#                 if stop_event.wait(5.5): #retorna True se for sinalizado
#                     break
#         #self.output_queue.put('\rComando concluído.   ', flush=True)
    
#     def _loop_commands(self) -> None:

#         while True: #not self.stop_event.is_set()  #self.exec_thread.is_alive():
#             try:
#                 command = self.commands_queue.get_nowait()
#                 #if self.stop_event.is_set():
#                 #    self.output_queue.put("Execução interrompida pelo usuário.\n")
#                 #    break

#                 self.output_queue.put(f"\nExecutando: {command}\n")
#                 animation_stop_event = threading.Event()
                
#                 animation_thread = threading.Thread(target= SubShell._animate_dots, args=(self, animation_stop_event,))
#                 animation_thread.start()
                
                
#                 result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
#                 animation_stop_event.set()
#                 if result.returncode != 0:
#                     self.output_queue.put(f"Erro ao executar o comando: {command}\n")
#                     #self.output_queue.put(f"stderr: {result.stderr}\n")
#                     #raise subprocess.CalledProcessError(result.returncode, command)
#                 self.output_queue.put(f"stdout: {result.stdout}\n")
#                 self.output_queue.put(f"stderr: {result.stderr}\n")
            
#                 animation_stop_event.set()
#                 animation_thread.join()
#             except queue.Empty: ...               
                            
#             time.sleep(0.1)                   
        

