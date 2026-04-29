# ~/.sigil/src/script.py
# script.py version: 1.0
from pathlib import Path
from uuid import uuid4

import subprocess
import shutil
import os

def new_filename_gen(file, origin_modifier=False):
    if not origin_modifier:
        files_id = str(uuid4())[:8].upper()
        new_filename = f"{Path(file).stem.upper()}-{files_id}-SIGIL.py"
    else:
        new_filename = Path(file).name
    return new_filename
    # print(new_filename)
    # print(files_id)
    # print(len(files_id))
    # print(files_id[24:])

def tools_mover(source_path, destination_path):
    # print("SRC :", os.path.abspath(source_path))
    # print("DST :", os.path.abspath(destination_path))
    try:
        shutil.copy(source_path, destination_path)
    except Exception as e:
        print(f"\n\033[31m> script.py < -> Copy failed: {e}\033[0m\n")
        return False
    return True

def script(data: dict, sigil_home):
    _cmd      = data['COMMANDS']
    target    = data['TARGET']
    scr_argv  = data['SCR_ARGV']
    tail_cmd  = data['TAIL']
    tools_dir = os.path.join(sigil_home, "tools")
    tools     = [
        f[:-3] for f in os.listdir(tools_dir)
        if f.endswith(".py")
    ]
    if not tools:
        print("\n\033[33m> script.py < -> No tools available\033[0m\n")
        return
    
    target_path = os.path.join(sigil_home, "tools", f"{target}.py")
    
    if not os.path.exists(target_path):
        print(f"\n\033[31m> script.py < -> Tool '{target}' not found\033[0m\n")
        return
    
    keep   = 'keep'   in tail_cmd # True / False
    origin = 'origin' in tail_cmd # True / False
    
    # print('CHECKPOINT HERE')
    
    new_filename     = new_filename_gen(target_path, origin)
    destination_path = os.path.join(os.getcwd(), new_filename)
    
    if not tools_mover(target_path, destination_path): return
    
    print(f"\n\033[3;32m> script.py < -> Running python3 '{new_filename}'\033[0m\n")
    
    try:
        columns, _lines = os.get_terminal_size()
        print("—" * columns + "\n")
        subprocess.run(["python3", destination_path] + scr_argv)
        print("\n" + "—" * columns)
    
    except Exception as e:
        print(f"\n\033[31m> script.py < -> Execution failed: {e}\033[0m\n")
    
    finally:
        if not keep:
            try:
                os.remove(destination_path)
                print(f"\n\033[2;3m> script.py < -> Cleaned up '{new_filename}'\033[0m\n")
            except Exception as e:
                print(f"\n\033[31m> script.py < -> Cleanup failed: {e}\033[0m\n")
        else:
            print(f"\n\033[33m> script.py < -> File kept: '{new_filename}'\033[0m\n")