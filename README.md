# TomTerminal3000
> **Status:** In development (indev). Commands and storage format may still change between releases.

## Requirements

- Python 3.10+
- [sympy](https://www.sympy.org/) (used by the `expr` command)
- [windows-curses](https://pypi.org/project/windows-curses/) (used by the `edit` command; only needed on Windows — curses ships with Python on Linux/macOS)

Install dependencies:

```bash
pip install -r requirements.txt
```

## Running it

```bash
python main.py
```

You'll land on a prompt like:

```
shell >>
```

Type `help` at any time to see the full command list.

## Project layout

```
main.py       - entry point / command loop
core/         - implementation modules (commands, editor, ...)
```

Only `main.py` sits at the top level; everything else lives in `core/` so new modules can be dropped in there later without touching the entry point.

## Storage

Files created with `create` are written to a real folder on disk:

```
Documents/TomFolder3000/
```

The folder is created automatically the first time you run `create`. Commands like `list`, `view`, `edit`, `copy`, `rename`, `size`, `search`, `open`, and `delete` all operate on files in this folder — **which one depends on who you're signed in as**:

- On the temporary `shell` session, files are **public** and live directly in `TomFolder3000/`.
- On a real account, files are **private** and live in `TomFolder3000/accounts/<name>/` — invisible and inaccessible from `shell` or any other account.

Since switching into a password-protected account requires that password, private files are effectively password-gated: nobody can `list`, `view`, or otherwise touch them without signing in first.

## Accounts

- You start out on a temporary `shell` session — it's not a real account, never shows up in `users`, and its files are public.
- `account <name>` switches to (or creates) an account. If that account has a password set, you'll be prompted for it. Its files are private to it.
- `signout` drops you back to the temporary `shell` session.
- `password` interactively changes the password on your **current** account (prompts for old password, new password, and confirmation). Hidden input is used when running in an interactive terminal.
- Account state (current user, accounts, and password hashes) is cached in a hidden file inside `TomFolder3000` so it persists across runs.

## Commands

| Command | Description |
|---|---|
| `show <text>` | Print the given text |
| `create <filename> <content>` | Create a file with content |
| `list` | List your files (public in `shell`, private per account) |
| `view <filename>` | Show the contents of a file |
| `edit <filename>` | Open a full-screen text editor for a file (arrows/Home/End to move, Backspace/Del to remove, Ctrl+O save, Ctrl+X save & exit) |
| `expr <expression>` | Evaluate a math expression |
| `delete <filename>` | Delete a file |
| `copy <src> <dest>` | Copy a file |
| `public <filename>` | Copy a private file to the public TomFolder3000 (keeps the private copy too) |
| `private <filename>` | Copy a public file to your private storage (keeps the public copy too) |
| `rename <old> <new>` | Rename a file |
| `size <filename>` | Show a file's size |
| `search <keyword>` | Search filenames and contents for a keyword |
| `open <filename>` | Open a file with the OS default app |
| `path` | Show your current (public or private) storage path |
| `date` | Show the current date and time |
| `history` | Show previously entered commands |
| `clear` | Clear the terminal screen |
| `account <name>` | Switch to (or create) an account |
| `signout` | Sign out to the temporary `shell` session |
| `password` | Change the current account's password |
| `me` | Print the current username |
| `users` | List all accounts created |
| `help` | Show the command list |
| `exit` | Exit the terminal |

## Notes

- `view` will refuse to print binary files (images, video, etc.) as text.
- Passwords are stored as SHA-256 hashes, never in plain text.
