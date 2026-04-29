# ~/.sigil/src/help.py
# help.py version: 1.0
import importlib.util

import os

def sigil_help(sigil_home):
    help_path = os.path.join(sigil_home, 'docs', 'help.txt')
    # help_path = 'help.txt'

    try:
        with open(help_path, 'r') as f:
            content = f.read()
        print(content)
        
    except FileNotFoundError:
        print(f"\033[31m> help.py < -> Help file not found at: {help_path}\033[0m")
    except Exception as e:
        print(f"\033[31m> help.py < -> Could not display help: {e}\033[0m")

def tools_help(target: str, sigil_home):
    if not target:
        print("\033[31m> help.py < -> Target can't be empty\033[0m")
        return
    
    target_path = os.path.join(sigil_home, "tools", f"{target}.py")
    
    if not os.path.exists(target_path):
        print(f"\033[31m> help.py < -> Tool '{target}' not found\033[0m")
        return
    
    try:
        spec = importlib.util.spec_from_file_location(f"help_{target}", target_path)
        # print(f"[HELP] -> {spec=}")
        module = importlib.util.module_from_spec(spec)
        # print(f"[HELP] -> {module=}")
        spec.loader.exec_module(module)
        
        if hasattr(module, "sghelp"):
            module.sghelp()
        else:
            print(f"\033[33m> help.py < -> '{target}' has no sghelp() function\033[0m")
    
    except Exception as e:
        print(f"\033[31m> help.py < -> Failed to load '{target}': {e}\033[0m")

# if __name__ == "__main__":
#     sigil_help()