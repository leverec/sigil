# ~/.sigil/src/info.py
# info version: 1.0
import sys
import os

def info(sigil_home):
    tools_dir = os.path.join(sigil_home, "tools")
    
    tools = [
        f[:-3] for f in os.listdir(tools_dir)
        if f.endswith(".py")
    ]
    
    tools_amount = len(tools)
    info_text = f"""
Tools           : sigil
Version         : 1.0.0 (001)
Author          : leverec
Release date    : 29/04/2026

Platform        : Termux (Android)
Compatibility   : Linux (may work), Windows (not tested)
Environment     : POSIX shell

Lang used       : python, shell
License         : Apache-2.0
Sigil directory : ~/.sigil
Tools loaded    : {tools_amount}

Description     : A tool to run scripts from a central directory without manually copying them.

Try             : sigil -h
Github          : https://github.com/leverec/sigil
    """
    print(info_text)

def list_tools(sigil_home):
    tools_dir = os.path.join(sigil_home, "tools")
    
    try:
        tools = [
            f[:-3] for f in os.listdir(tools_dir)
            if f.endswith(".py")
        ]
        # tools1 = [
        #     f for f in os.listdir(tools_dir)
        #     if f.endswith(".py")
        # ]
        
        # print(tools)
        # print(tools1)
        
        if not tools:
            print("\n\033[33m> info.py < -> No tools available\033[0m\n")
            return
        
        # print(tools)
        
        print("\n\033[1;34m>> Available Tools <<\033[0m")
        for tool in tools:
            print(f" - \033[32m{tool}\033[0m")
        print()
    
    except Exception as e:
        print(f"\n\033[31m> info.py < -> Failed to list tools: {e}\033[0m\n")