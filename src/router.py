# ~/.sigil/src/router.py
# router.py version: 1.0

import importlib.util

import sys
import os

# sigil -t gentrees --ignore .git @ origin keep
# |        |        |               |      |
# |        |        |               +------+-- TAIL (Sigil modifiers)
# |        |        +-- SCRIPT ARGS (python3 gentrees.py [SCR_ARGV])
# +--------+-- HEAD (Target & Action)

# head list command : { -t, -l, -h, -v, -s }
# tail list command : { keep, origin }
    
def router(data: dict):
    # {
    #     'COMMANDS': '-t',
    #     'SCR_ARGV': '--ignore __pycache__',
    #     'TAIL': ['keep', 'origin'],
    #     'TARGET': 'gentrees',
    #     'TOKENS': ['-t', 'gentrees', '--ignore', '__pycache__', '@', 'keep', 'origin']
    # }
    # print(">>>>>>>>>>>> ROUTER <<<<<<<<<<<<\n")
    command    = data['COMMANDS']
    target     = data['TARGET']
    scr_argv   = data['SCR_ARGV']
    sigil_home = os.environ.get('SIGIL_HOME')
    
    # print(f"[ROUTER] -> DATE : {data}")
    # print(f"[ROUTER] -> SIGIL-HOME : {sigil_home}")
    
    if command == '-h':
        # load src/help.py dynamically
        help_module_path = os.path.join(sigil_home, "src", "help.py")
        # print(f"[ROUTER] -> help dynamic import:\n-> {help_dir=}\n-> {help_module_path=}\n")
        
        # if help_dir not in sys.path:
            # print(f"[ROUTER] -> sys.path: {sys.path}\n")
            # sys.path.insert(0, help_dir)
        spec = importlib.util.spec_from_file_location("help", help_module_path)
        # print(f"[ROUTER] -> {spec=}")
        help_env = importlib.util.module_from_spec(spec)
        # print(f"[ROUTER] -> {help_env=}")
        spec.loader.exec_module(help_env)
        if not target:
            help_env.sigil_help(sigil_home)
        else:
            help_env.tools_help(target, sigil_home)
    elif command == '-v' or command == '-l':
        # idk im just copying shit
        info_module_path = os.path.join(sigil_home, "src", "info.py")
        spec             = importlib.util.spec_from_file_location("info", info_module_path)
        info_path        = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(info_path)
        if command == '-v':
            info_path.info(sigil_home)
        else:
            info_path.list_tools(sigil_home)
    elif command == '-t':
        script_module_path = os.path.join(sigil_home, "src", "script.py")
        spec               = importlib.util.spec_from_file_location("script", script_module_path)
        script_path        = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(script_path)
        script_path.script(data, sigil_home)
    elif command == '-s':
        setup_module_path = os.path.join(sigil_home, "src", "setup.py")
        spec              = importlib.util.spec_from_file_location("setup", setup_module_path)
        setup_path        = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(setup_path)
        setup_path.setup(data, sigil_home)
    else:
        print("\nTry: sigil -h\n")