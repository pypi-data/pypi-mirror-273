from typing import Callable, Optional, Any
import inspect
from string import Template


def extrair_corpo_funcao( func : Callable[[],Any], inside : bool = False , dic : Optional[dict[str,str]] = None ) -> str:
    
    source_code = inspect.getsource(func)
    lines = source_code.splitlines()
    if inside:
        lines = lines[1:]
    min_indent = min(len(line) - len(line.lstrip(' ')) for line in lines if line.strip())
    stripped_lines = [line[min_indent:] for line in lines]
    cleaned_source_code = "\n".join(stripped_lines)

    if dic:
        cleaned_source_code = Template(cleaned_source_code).safe_substitute(dic)
    
    return cleaned_source_code