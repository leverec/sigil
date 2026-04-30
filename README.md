# Sigil

> *A tools that make your life easier*

[![Python](https://img.shields.io/badge/Python%203.13+-3670a0?logo=python&logoColor=ffdd54)](https://www.python.org/downloads/)
[![Shell](https://img.shields.io/badge/GNU--Bash-4eaa25?logo=gnubash&logoColor=fff)](#)
[![!Termux](https://img.shields.io/badge/Android-Termux-black?logo=android&labelColor=brightgreen&logoColor=fff)](#)
[![License: Apache-2.0](https://img.shields.io/badge/License-Apache--2.0%20License-yellow?)](https://opensource.org/license/Apache-2.0)

**Seriously.**

Do you ever find it kind of a hassle to use a different app between termux and your file manager just to copy and run a small python script?
well, that's the reason why i make this

Sigil is a python tools that can **run** a single file **anywhere** you want,
**Automatically delete** the file that has been moved to the Current Directory
so it'd not make any trash file, And **adding your own tools!**

## Features

- **Remove tools after being used:** After copying and running the file in the current directory, sigil will remove the file from that directory unless you're using a modifiers
- **Modified file name:** Before copying it to your current directory, sigil will rename the file in this format `[ORIGINAL_FILENAME]-[CUSTOM_UUID]-SIGIL.py` unless you're using a modifiers, it's intention is to avoid an unexpected overwrite
- **Easy to setup new tools:** by using `sigil -s \?set [filename]` you've added your own tools

## Installation

### Prerequisites
- Python 3.6 or higher
- Bash/Zsh (for shell components)

### The easy way
Run this single script in your terminal and everything got setup:

```bash
curl -sL https://raw.githubusercontent.com/leverec/sigil/main/installer.sh | bash
```

```text
+ very easy to setup
- no tests/ folder
```

### The hard way
1.Clone thi repository
```bash
git clone https://github.com/leverec/sigil.git
```
2.Rename and move the folder to ~
```bash
mv sigil ~/.sigil
```
3.Move the bin/sigil.sh to $PREFIX
```bash
cd .sigil/bin
cp sigil.sh $PREFIX/bin/sigil
```
4.Add execute permission
```bash
chmod +x $PREFIX/bin/sigil
```

```text
+ has every folder in it
- not easy to setup
```

### The wise way
if you want every file, doesnt wanna lose anything, and also don't want to bother with those step, try this

<details>
<summary></summary>
😂 just merge the hard way together lol
</details>

```bash
git clone https://github.com/leverec/sigil.git && mv sigil ~/.sigil && cp ~/.sigil/bin/sigil.sh $PREFIX/bin/sigil && chmod +x $PREFIX/bin/sigil
```

---

After all of that, you're basically done.try `sigil -h`

## Usage

Try `sigil -h` for help

### Head Commands
| Commands                      | Description                                                                                       |
|-------------------------------|---------------------------------------------------------------------------------------------------|
| `-l`                          | List all available tools                                                                          |
| `-v`                          | Show sigil information                                                                            |
| `-h [Tools]`                  | Show sigil help. If tools is filled, it'd run `sghelp()` from that tools (if the function exists) |
| `-t <Tools>`                  | Run tools from you current directory                                                              |
| `-s <setup_command> <target>` | Setup command : `?set ?rm ?lh`, set a new tools or remove an existing tools                           |

### Tail Commands

Tail commands separator : `@`

example: `sigil -t <TOOLS> @ <TAIL>`

| Commands | Description                                                                       |
|----------|-----------------------------------------------------------------------------------|
| `keep`   | Kept the file in your current directory instead of removing it                    |
| `origin` | Kept the file's original name when moving it (might overwrite the same file name) |

### Setup Commands

A commands after `sigil -s <This_Setup_Commands>`

> [!TIP]
> Use `\` an escape characters before the `?` example: `?rm` -> `\?rm`

| Commands            | Description                                             |
|---------------------|---------------------------------------------------------|
| `?set <YOUR_FILES>` | Set a new tools (has to be a single and python files)   |
| `?rm <TOOLS>`       | Remove an existing tools                                |
| `?lh`               | List for every setup commands (idk why i made this tbh) |

### Structure Commands
```text
sigil -t gentrees --ignore .git @ origin keep
       |  |        |            |  |      |
       |  |        |            |  +------+-- TAIL COMMANDS (Modifiers)
       |  |        |            +------ TAIL SEPARATOR
       |  |        +-- SCRIPT ARGS (python3 gentrees.py [SCR_ARGV])
       |  +--------- TARGET
       +------- HEAD COMMANDS
```

> [!NOTE]
> Script Args = an argv that get putted back to `python3 {TARGET} {SCR_ARGV}` as an argument

## Project Structure

```text
sigil/
  ├── bin/
  │   └── sigil.sh
  ├── docs/
  │   └── (any documentation)
  ├── src/
  │   └── (src code)
  ├── tests/
  │   └── (test unit)
  ├── tools/
  │   └── (your tools)
  └── installer.sh
```

## Testing

install `pip install pytest` if you don't have pytest

Run the test suite using `pytest`:

```bash
pytest test/
```

personally, i recommend using `python3 -m pytest -v`

## Contributing

Contributions are welcome. Please read [CONTRIBUTING.md](./CONTRIBUTING.md) for guidelines on reporting bugs, suggesting features, code style, writing tests, and submitting pull requests.

## License

Distributed under the Apache-2.0 License. See [LICENSE](LICENSE) for more information.

Project Link: [https://github.com/leverec/sigil](https://github.com/leverec/sigil)
