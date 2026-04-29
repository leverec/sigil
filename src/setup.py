# ~/.sigil/src/setup.py
# setup.py version: 1.0
import os
import sys
import shutil

from pathlib import Path

def confirmation(message):
    try:
        choice = input(f"\n\033[33m{message}\033[0m [y/N] -> ").strip().lower()
    except (KeyboardInterrupt, EOFError):
        return False
    return choice in ('y', 'yes')

def force_yes(argument):
    if '-y' in argument or '--yes' in argument: return True
    else                                      : return False

def rmcmd(target, tools_dir):
    file      = target + '.py'
    rm_target = Path(tools_dir) / Path(file)
    # print(rm_target)
    try:
        os.remove(rm_target)
        print(f"\n\033[32m> removed {rm_target}\033[0m")
        print(f"\033[32m> setup.py < -> Success deleting '{target}' tools from sigil\033[0m\n")
    except Exception as e:
        print(f"\n\033[31m> setup.py < -> Deleting attempt failed: {e}\033[0m\n")

def setcmd(file, dest):
    try:
        shutil.copy(str(file), str(dest))
        print(f"\033\n[32m> added {dest}\033[0m")
        print(f"\033[32m> setup.py < -> Success added new tools '{Path(file).stem}' try run \033[2msigil -t {Path(file).stem}\033[0m\n")
    except Exception as e:
        print(f"\n\033[31m> setup.py < -> Adding attempt failed: {e}\033[0m\n")
# sigil -s /rm [tools name without .py]
def setup(data, sigil_home):
    arg       = data['TOKENS'][1] if len(data['TOKENS']) > 1 else '?lh'
    path      = data['TOKENS'][2] if len(data['TOKENS']) > 2 else []
    tools_dir = os.path.join(sigil_home, "tools")
    force_y   = force_yes(data['TOKENS'][2:]) if len(data['TOKENS']) > 2 else False
    
    if arg not in ('?set', '?rm', '?lh'):
        print('\nTry: sigil -s \\?lh\n')
        return
    if not path and arg != '?lh' :
        print(f"\n\033[31m> setup.py < -> Target can't be empty\033[0m\n")
        return
    if path:
        target = Path(path)
    
    # print(">>>>>>>>>>>> SETUP <<<<<<<<<<<<\n")
    # print(f"[SETUP] -> force yes : {force_y}")
    # print(f"[SETUP] -> arg       : {arg}\n")
    
    # print(target)
    
    if arg   == '?set':
        if not target.exists():
            print(f"\n\033[31m> setup.py < -> File '{target.name}' not found\033[0m\n")
            return
        if not target.name.endswith('.py'):
            print(f"\n\033[31m> setup.py < -> File '{target.name}' has to be python files\033[0m\n")
            return
        
        file = target.name
        dest = Path(tools_dir) / file
        if dest.exists() and not force_y:
            choice = confirmation(f"Are you sure you want to overwrite\n'{dest}'")
            if not choice: print(' ' * 5, '\033[31;1;2mAborted.\033[0m\n')
            else:
                setcmd(target, dest)
                return
        else:
            setcmd(target, dest)
            return
            
    elif arg == '?rm':
        # print('I HATE WHEN I HAD TO DO THIS BECAUSE SOMETHING ISNT RIGHT')
        if str(target).endswith('.py'): rm_target = str(Path(target).stem)
        else                          : rm_target = str(target)
        tools = [
            f[:-3] for f in os.listdir(tools_dir)
            if f.endswith(".py")
        ]
        # print(rm_target)
        # print(tools)
        if not rm_target in tools:
            print(f"\n\033[31m> setup.py < -> Tool '{rm_target}' not found\033[0m")
            print(f"\033[36m> setup.py < -> TIP: try \033[2msigil -l\033[0m\n")
            return
        
        if not force_y:
            choice = confirmation(f"Are you sure you want to delete '{rm_target}'")
            if not choice: print(' ' * 5, '\033[31;1;2mAborted.\033[0m\n')
            else:
                rmcmd(rm_target, tools_dir)
                return
        else:
            rmcmd(rm_target, tools_dir)
            return
        
    elif arg == '?lh':
        print('\nsigil -s \\?set ... # add new tools')
        print('sigil -s \\?rm  ... # remove tools')
        print('sigil -s \\?lh      # show this help and exit\n')
        return
    
    else:
        print('\nTry: sigil -s \\?lh\n')