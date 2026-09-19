# TomTerminal3000
> **Status:** In development (indev). Commands and storage format may still change between releases.

## Requirements

- Python 3.10+
- [sympy](https://www.sympy.org/) (used by the `expr` command)

Install the dependency:

```bash
pip install sympy
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

## Storage

Files created with `create` are written to a real folder on disk:

```
Documents/TomFolder3000/
```

The folder is created automatically the first time you run `create`. Commands like `list`, `view`, `copy`, `rename`, `size`, `search`, `open`, and `delete` all operate on files in this folder.

## Accounts

- You start out on a temporary `shell` session — it's not a real account and never shows up in `users`.
- `account <name>` switches to (or creates) an account. If that account has a password set, you'll be prompted for it.
- `signout` drops you back to the temporary `shell` session.
- `password` interactively changes the password on your **current** account (prompts for old password, new password, and confirmation). Hidden input is used when running in an interactive terminal.
- Account state (current user, accounts, and password hashes) is cached in a hidden file inside `TomFolder3000` so it persists across runs.

## Commands

| Command | Description |
|---|---|
| `show <text>` | Print the given text |
| `create <filename> <content>` | Create a file with content |
| `list` | List all files in TomFolder3000 |
| `view <filename>` | Show the contents of a file |
| `expr <expression>` | Evaluate a math expression |
| `delete <filename>` | Delete a file |
| `copy <src> <dest>` | Copy a file |
| `rename <old> <new>` | Rename a file |
| `size <filename>` | Show a file's size |
| `search <keyword>` | Search filenames and contents for a keyword |
| `open <filename>` | Open a file with the OS default app |
| `path` | Show the TomFolder3000 storage path |
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
