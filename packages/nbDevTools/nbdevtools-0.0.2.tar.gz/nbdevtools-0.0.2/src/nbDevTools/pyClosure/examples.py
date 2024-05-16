#from pyclosure.tools import  SHELL
import os
import re
from nbDevTools.cmd_shell import SHELL



def ploft_block_build() -> SHELL:

    root = '2023/ploft/js_dev'    
    
    #FILE_ENTRY = f'{root}/pyproj/src/js_inspect/page/entry.js' 
    FILE_ENTRY = f'{root}/scripts/pyclosure/entry/__entry__block_build_.js'
    FILE_EXTERN = f'{root}/scripts/pyclosure/entry/__extern_html__.js'

    #C:\Users\Christoph Cury\source\2023\pywebspy\pyproj\src\js_inspect\js_dev\__extern__.js
    
    FILE_OUTPUT = f'{root}/scripts/pyclosure/output/__output__block_build_.js'
    MODE ='ADVANCED' #SIMPLE


    #C:\Users\Christoph Cury\source\2023\pywebspy\pyproj\src\js_inspect\page\html_computed.js
    FILE = [ 
        f'--js {root}/js_dev/*.js',
        f'--js {root}/js_dev/**/*.js',
        #f'--js {root}/svg_editor/src/**/*.js',
        #f'--js {root}/html_tools/src/*.js',
        f'--js {FILE_ENTRY}'
        ]
    
    DEP_ARG = '--dependency_mode PRUNE'
    FORMATING = '--formatting PRETTY_PRINT'

    GC = ['npx google-closure-compiler',
        ' '.join(FILE),
        f'--entry_point {FILE_ENTRY}',
        f'--externs {FILE_EXTERN}',
        '--js node/node_modules/google-closure-library/closure/goog/base.js',
        '--language_in ECMASCRIPT_NEXT',
        DEP_ARG,
        f'--js_output_file {FILE_OUTPUT}',
        '--jscomp_error checkTypes',
        FORMATING,
        '--warning_level VERBOSE',
        '--hide_warnings_for goog',
        '--isolation_mode IIFE',
        f'--compilation_level {MODE}',
        '--jscomp_error=*', #--jscomp_error * gera erro por conta de pasta 2020
        '--jscomp_off extraRequire',
        '--jscomp_off unusedLocalVariables',
        '--jscomp_off uselessCode',
        '--chunk_output_type=ES_MODULES', #por conta de import.meta.url
    ]
    
    COMPILE = ' '.join(GC)
    #print(COMPILE);return
    
    s = SHELL()
    s.path_upto('source')    
    s.cmd(COMPILE)
    s.waiting_dots('COMPILED!')
    return s





def get_computed() -> SHELL:

    root = '2023/pywebspy'    
    
    #FILE_ENTRY = f'{root}/pyproj/src/js_inspect/page/entry.js' 
    FILE_ENTRY = f'{root}/pyproj/src/js_inspect/js_dev/__entry__.js'
    #FILE_ENTRY =r'2023/pywebspy/pyproj/src/js_inspect/page/entry.js'
    FILE_EXTERN = f'{root}/pyproj/src/js_inspect/js_dev/__extern__.js'

    #C:\Users\Christoph Cury\source\2023\pywebspy\pyproj\src\js_inspect\js_dev\__extern__.js
    
    FILE_OUTPUT = f'{root}/scripts/pyclosure/output/js_inspect_compiled.js' 
    MODE ='ADVANCED' #SIMPLE


    #C:\Users\Christoph Cury\source\2023\pywebspy\pyproj\src\js_inspect\page\html_computed.js
    FILE = [ 
        f'--js {root}/pyproj/src/js_inspect/js_dev/app_capture.js',
        f'--js {root}/pyproj/src/js_inspect/js_dev/**/*.js',
        #f'--js {root}/svg_editor/src/**/*.js',
        #f'--js {root}/html_tools/src/*.js',
        f'--js {FILE_ENTRY}'
        ]
    
    DEP_ARG = '--dependency_mode PRUNE'
    FORMATING = '--formatting PRETTY_PRINT'

    GC = ['npx google-closure-compiler',
        ' '.join(FILE),
        f'--entry_point {FILE_ENTRY}',
        f'--externs {FILE_EXTERN}',
        '--js node/node_modules/google-closure-library/closure/goog/base.js',
        '--language_in ECMASCRIPT_NEXT',
        DEP_ARG,
        f'--js_output_file {FILE_OUTPUT}',
        '--jscomp_error checkTypes',
        FORMATING,
        '--warning_level VERBOSE',
        '--hide_warnings_for goog',
        '--isolation_mode IIFE',
        f'--compilation_level {MODE}',
        '--jscomp_error=*', #--jscomp_error * gera erro por conta de pasta 2020
        '--jscomp_off extraRequire',
        '--jscomp_off unusedLocalVariables',
        '--jscomp_off uselessCode',
        '--chunk_output_type=ES_MODULES', #por conta de import.meta.url
    ]
    
    COMPILE = ' '.join(GC)
    #print(COMPILE);return
    
    s = SHELL()
    s.path_upto('source')    
    s.cmd(COMPILE)
    s.waiting_dots('COMPILED!')
    return s
    



def svg_editor() -> None:

    root = '2023/cjs'    
    FILE_ENTRY = f'{root}/closure/sources/svg_editor/entry.js'
    FILE_OUTPUT = f'{root}/closure/output/svg_editor_compiled.js'
    MODE ='ADVANCED' #SIMPLE

    FILE = [ 
        f'--js {root}/svg_editor/src/*.js',
        f'--js {root}/svg_editor/src/**/*.js',
        f'--js {root}/html_tools/src/*.js',
        f'--js {root}/html_tools/src/**/*.js',
        f'--js {FILE_ENTRY}'
        ]
    
    DEP_ARG = '' #--dependency_mode PRUNE'
    FORMATING = '--formatting PRETTY_PRINT'

    GC = ['npx google-closure-compiler',
        ' '.join(FILE),
        '--js node/node_modules/google-closure-library/closure/goog/base.js',
        '--language_in ECMASCRIPT_NEXT',
        DEP_ARG,
        f'--js_output_file {FILE_OUTPUT}',
        '--jscomp_error checkTypes',
        FORMATING,
        '--warning_level VERBOSE',
        '--hide_warnings_for goog',
        '--isolation_mode IIFE',
        f'--compilation_level {MODE}',
        '--jscomp_error=*',
        '--jscomp_off extraRequire',
        '--jscomp_off unusedLocalVariables',
        '--jscomp_off uselessCode'
    ]
    
    COMPILE = ' '.join(GC)
    
    s = SHELL()
    s.path_upto('source')    
    s.cmd(COMPILE)
    s.waiting_dots()
    

def cs50_run(bprint:bool= False) -> None:

    # Visite: https://www.google.com/

    # file://C:/Users/Christoph%20Cury/source/2023/cjs/closure/sources/html_tools_cs50.js
    
    root = '2023/cjs'    
    FILE_ENTRY = f'{root}/closure/sources/html_tools_cs50.js'
    FILE_OUTPUT = f'{root}/closure/output/html_tools_cs50_compiled.js'
    FILE_SOURCEMAP = ''# f'{root}/closure/output/html_tools_cs50_source_map.map'
    MODE ='ADVANCED' #SIMPLE

    FILE = [ 
        f'--js {root}/html_tools/src/*.js',
        f'--js {root}/html_tools/src/**/*.js',
        f'--js {root}/html_tools/models/tests/cs50.js',
        f'--js {FILE_ENTRY}'
        ]
    
    DEP_ARG = '--dependency_mode PRUNE'
    FORMATING = '--formatting PRETTY_PRINT'

    GC = ['npx google-closure-compiler',
        ' '.join(FILE),
        '--js node/node_modules/google-closure-library/closure/goog/base.js',
        '--language_in ECMASCRIPT_NEXT',
        DEP_ARG,
        f'--entry_point={FILE_ENTRY}',
        f'--js_output_file {FILE_OUTPUT}',
        '--jscomp_error checkTypes',
        FORMATING,
        '--warning_level VERBOSE',
        '--hide_warnings_for goog',
        '--isolation_mode IIFE',
        f'--compilation_level {MODE}',
        '--jscomp_error=*',
        '--jscomp_off extraRequire',
        '--jscomp_off unusedLocalVariables',
        '--jscomp_off uselessCode',
        f'--create_source_map {FILE_SOURCEMAP}' if FILE_SOURCEMAP else ''
    ]
    
    
    COMPILE = re.sub('\s+',' ',' '.join(GC))
    
    if bprint:
        print(COMPILE)
    else:
        s = SHELL()
        s.path_upto('source')    
        s.cmd(COMPILE)
        s.waiting_dots()

