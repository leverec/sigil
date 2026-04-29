# ~/.sigil/src/parser.py
# parser.py version : 1.0
import sys

# constant
SEPARATOR_CHAR = '@'
HEAD_COMMANDS  = { '-t', '-h', '-v', '-l', '-s' }

# sigil -t gentrees --ignore .git @ origin keep
# |        |        |               |      |
# |        |        |               +------+-- TAIL (Sigil modifiers)
# |        |        +-- SCRIPT ARGS (python3 gentrees.py [SCR_ARGV])
# +--------+-- HEAD (Target & Action)

# head list cmd : { -t, -l, -h, -v, -s }
# tail list cmd : { keep, origin }

# def tokenizer(argv: str):
#     if not isinstance(argv, str):
#         return []
#     return argv.strip().split()[1:]
#     [1:] for removing the first sys.argv which is the file itself

def section(tokens: list, mode=1):
    # 1 = head tail section
    # 2 or anything else = script args section
    if mode == 1:
        if SEPARATOR_CHAR not in tokens: return tokens, []
        idx  = tokens.index(SEPARATOR_CHAR)
        # every object before separator_char
        head = tokens[:idx]
        # every object after separator_char
        tail = tokens[idx+1:]
        # return tuple(before separator_char, after SEPARATOR_CHAR)
        return head, tail
        # every tokens has 3, 2 or 1 section
    else:
        # soo, head token will always be like
        # ['-t', 'gentrees', '--ignore', '.git']
        # my logic is, just remove the first 2 index and insert the remaining into script argv
        # first i'm gonna check if the commands is -t or -h
        # and the length is more than 2
        if not '-t' in tokens and not len(tokens) > 2: return []
        script_argv = tokens[2:]
        return script_argv
        # and also, i need to make sure that 'sigil' is not an arguments

def classify_head_commands(tokens: list):
    if not tokens: return "HINTS"
    cmd = tokens[0]
    if cmd in HEAD_COMMANDS: return cmd
    else                   : return 'HINTS'

def parser(argv):
    # print(">>>>>>>>>>>> PARSER <<<<<<<<<<<<\n")
    # tokens: list = tokenizer(argv)
    tokens = argv[1:]
    cmd = classify_head_commands(tokens)
    head, tail = section(tokens)
    
    # print(f"[PARSER] -> head: {head}")
    # print(f"[PARSER] -> tail: {tail}")
    # print(f"[PARSER] -> tokens: {tokens}")
    
    scripts_argv = []
    if '-t' in head and len(head) > 2:
        scripts_argv = section(head, 2)
        
    if SEPARATOR_CHAR not in tokens:
        # print(f"[PARSER] -> scripts_argv: {scripts_argv}\n")
        return {
            "COMMANDS" : cmd,
            "TARGET"   : head[1] if len(head) > 1 and (cmd == '-t' or cmd == '-h')else [],
            "SCR_ARGV" : scripts_argv if scripts_argv else [],
            "TAIL"     : [],
            "TOKENS"   : tokens
        }
    else:
        # print(f"[PARSER] -> scripts_argv: {scripts_argv}\n")
        return {
            "COMMANDS" : cmd,
            "TARGET"   : head[1],
            "SCR_ARGV" : scripts_argv,
            "TAIL"     : tail,
            "TOKENS"   : tokens
        }