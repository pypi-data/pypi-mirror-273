from typing import Callable,  Optional
import os

import pathlib


def modificar_e_gravar_arquivo(arquivo_origem : str, arquivo_destino : str , 
                               pairs : list[tuple[str,str]], fedit : Optional[Callable[[str],str]] = None  ) -> None:
    try:
        # Abrir o arquivo de origem para leitura
        with open(arquivo_origem, 'r', encoding='utf-8') as origem:
            conteudo = origem.read()

        for busca, substituicao in pairs:
            conteudo = conteudo.replace(busca, substituicao)     

        if fedit:
            conteudo = fedit(conteudo)
            #lambda x : f'export const JS_CODE = `\n{x}\n`'   
            #conteudo = f'export const JS_CODE = `\n{conteudo}\n`'   

        with open(arquivo_destino, 'w', encoding='utf-8') as destino:
            destino.write(conteudo)
        
    except Exception as e:
        print(f"Ocorreu um erro: {e}")

class path:

    @staticmethod
    def upto(up_folder:str, from_folder : Optional[str] = None ) -> str:
        if from_folder is None:
            from_folder = os.getcwd()

        #print(from_folder, up_folder)

        for parent in pathlib.Path(from_folder).parents:
            if parent.name == up_folder:
                return str(parent)
        
        #lt = from_folder.split(os.sep)
        #n = len(lt)
        #try:
        #    while lt[n-1] != up_folder:
        #        n-=1
        #    return os.sep.join(lt[0:n])
        raise RuntimeError(f'Pasta não encntrada {up_folder} acima de {from_folder} ')


    @staticmethod
    def relative_to(from_folder:str, to_folder:str) ->str:
        return str(pathlib.Path(to_folder).relative_to(pathlib.Path(from_folder)))



'''

do jupyter notebook - ver local do arquivo que roda o script
get_ipython().starting_dir

'''