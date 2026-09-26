import os
import shutil
import json
import hashlib
from datetime import datetime
from sympy import sympify

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STORAGE_DIR = os.path.join(PROJECT_ROOT, "TomFolder3000")
CACHE_FILENAME = ".terminal_cache.json"
CACHE_FILE = os.path.join(STORAGE_DIR, CACHE_FILENAME)
ACCOUNTS_DIRNAME = "accounts"
RESERVED_NAMES = (CACHE_FILENAME, ACCOUNTS_DIRNAME)

SHELL_USER = "shell"

current_user = SHELL_USER
accounts = {}
user_list = []
command_history = []

def _active_dir():
    if current_user == SHELL_USER:
        return STORAGE_DIR
    return os.path.join(STORAGE_DIR, ACCOUNTS_DIRNAME, current_user)

def _hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def load_cache():
    global current_user, accounts, user_list
    os.makedirs(STORAGE_DIR, exist_ok=True)

    if os.path.isfile(CACHE_FILE):
        try:
            with open(CACHE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            current_user = data.get("current_user", SHELL_USER)
            accounts = data.get("accounts", {})
            accounts.pop(SHELL_USER, None)
            user_list = list(accounts.keys())
            return
        except (json.JSONDecodeError, OSError):
            pass

    save_cache()

def save_cache():
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump({"current_user": current_user, "accounts": accounts}, f, indent=2)

load_cache()

def create_file(args_string):
    parts = args_string.split(maxsplit=1)

    if len(parts) < 2:
        return "Error: Use 'create <filename> <content>'"

    filename = parts[0]
    content = parts[1]

    if filename in RESERVED_NAMES:
        return f"Error: '{filename}' is a reserved filename."

    active_dir = _active_dir()
    os.makedirs(active_dir, exist_ok=True)
    filepath = os.path.join(active_dir, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    return f"Created file '{filename}' successfully in '{active_dir}'."

def _visible_files():
    active_dir = _active_dir()
    if not os.path.isdir(active_dir):
        return []
    return [f for f in os.listdir(active_dir) if f not in RESERVED_NAMES]

def list_files():
    files = _visible_files()
    label = "TomFolder3000's Files" if current_user == SHELL_USER else f"{current_user}'s Private Files"

    if not files:
        return f"{label}:\n(empty)"

    output = f"{label}:\n"
    active_dir = _active_dir()
    for filename in files:
        filepath = os.path.join(active_dir, filename)
        created = datetime.fromtimestamp(os.path.getctime(filepath)).strftime("%Y-%m-%d %H:%M:%S")
        output += f"{filename} ({created})\n"
    return output.strip()

def view_file(filename):
    filepath = os.path.join(_active_dir(), filename)

    if filename in RESERVED_NAMES or not os.path.isfile(filepath):
        return f"Error: File '{filename}' not found."

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    except UnicodeDecodeError:
        return f"Error: Cannot view '{filename}' as text (it may be an image, video, or other binary file)."

def read_for_edit(filename):
    if filename in RESERVED_NAMES:
        return None, f"Error: '{filename}' is a reserved filename."

    filepath = os.path.join(_active_dir(), filename)
    if not os.path.isfile(filepath):
        return [], None

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read().splitlines(), None
    except UnicodeDecodeError:
        return None, f"Error: Cannot edit '{filename}' as text (it may be an image, video, or other binary file)."

def save_edit(filename, lines):
    active_dir = _active_dir()
    os.makedirs(active_dir, exist_ok=True)
    filepath = os.path.join(active_dir, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    return f"Saved '{filename}' successfully."

def calculate(expression_string):
    try:
        return str(sympify(expression_string))
    except Exception:
        return "Error: Invalid math expression."

def delete_file(filename):
    filepath = os.path.join(_active_dir(), filename)
    if filename not in RESERVED_NAMES and os.path.isfile(filepath):
        os.remove(filepath)
        return f"Deleted file '{filename}' successfully."
    else:
        return f"Error: File '{filename}' not found."

def get_date():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def record_history(entry):
    command_history.append(entry)

def get_history():
    if not command_history:
        return "No commands entered yet."

    output = "--- Command History ---\n"
    for i, entry in enumerate(command_history, start=1):
        output += f"{i}. {entry}\n"
    return output.strip()

def get_path():
    return _active_dir()

def open_file(filename):
    filepath = os.path.join(_active_dir(), filename)

    if filename in RESERVED_NAMES or not os.path.isfile(filepath):
        return f"Error: File '{filename}' not found."

    try:
        os.startfile(filepath)
        return f"Opening '{filename}'..."
    except OSError as e:
        return f"Error: Could not open '{filename}' ({e})."

def copy_file(args_string):
    parts = args_string.split(maxsplit=1)

    if len(parts) < 2:
        return "Error: Use 'copy <src> <dest>'"

    active_dir = _active_dir()
    src, dest = parts[0], parts[1]
    src_path = os.path.join(active_dir, src)
    dest_path = os.path.join(active_dir, dest)

    if src in RESERVED_NAMES or not os.path.isfile(src_path):
        return f"Error: File '{src}' not found."
    if dest in RESERVED_NAMES:
        return f"Error: '{dest}' is a reserved filename."

    shutil.copy(src_path, dest_path)
    return f"Copied '{src}' to '{dest}'."

def publish_file(filename):
    if current_user == SHELL_USER:
        return "Error: You're already on the public 'shell' session."
    if filename in RESERVED_NAMES:
        return f"Error: '{filename}' is a reserved filename."

    src_path = os.path.join(_active_dir(), filename)
    if not os.path.isfile(src_path):
        return f"Error: File '{filename}' not found."

    os.makedirs(STORAGE_DIR, exist_ok=True)
    shutil.copy(src_path, os.path.join(STORAGE_DIR, filename))
    return f"Published '{filename}' to the public TomFolder3000 (kept your private copy too)."

def privatize_file(filename):
    if current_user == SHELL_USER:
        return "Error: Switch to (or create) an account first to have private storage."
    if filename in RESERVED_NAMES:
        return f"Error: '{filename}' is a reserved filename."

    src_path = os.path.join(STORAGE_DIR, filename)
    if not os.path.isfile(src_path):
        return f"Error: File '{filename}' not found."

    private_dir = _active_dir()
    os.makedirs(private_dir, exist_ok=True)
    shutil.copy(src_path, os.path.join(private_dir, filename))
    return f"Copied '{filename}' to your private storage (kept the public copy too)."

def rename_file(args_string):
    parts = args_string.split(maxsplit=1)

    if len(parts) < 2:
        return "Error: Use 'rename <old> <new>'"

    active_dir = _active_dir()
    old, new = parts[0], parts[1]
    old_path = os.path.join(active_dir, old)
    new_path = os.path.join(active_dir, new)

    if old in RESERVED_NAMES or not os.path.isfile(old_path):
        return f"Error: File '{old}' not found."
    if new in RESERVED_NAMES:
        return f"Error: '{new}' is a reserved filename."
    if os.path.exists(new_path):
        return f"Error: File '{new}' already exists."

    os.rename(old_path, new_path)
    return f"Renamed '{old}' to '{new}'."

def get_size(filename):
    filepath = os.path.join(_active_dir(), filename)

    if filename in RESERVED_NAMES or not os.path.isfile(filepath):
        return f"Error: File '{filename}' not found."

    size_bytes = os.path.getsize(filepath)
    if size_bytes < 1024:
        return f"{filename}: {size_bytes} bytes"
    return f"{filename}: {size_bytes / 1024:.2f} KB"

def search_files(keyword):
    files = _visible_files()
    if not files:
        return "No files to search."

    active_dir = _active_dir()
    matches = []
    for filename in files:
        filepath = os.path.join(active_dir, filename)
        if keyword.lower() in filename.lower():
            matches.append(filename)
            continue
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                if keyword.lower() in f.read().lower():
                    matches.append(filename)
        except (UnicodeDecodeError, IsADirectoryError):
            continue

    if not matches:
        return f"No files matching '{keyword}' found."

    output = f"--- Matches for '{keyword}' ---\n"
    for filename in matches:
        output += f"{filename}\n"
    return output.strip()

def account_exists(username):
    return username in accounts

def account_has_password(username):
    return accounts.get(username) is not None

def verify_password(username, password):
    stored_hash = accounts.get(username)
    if stored_hash is None:
        return True
    return _hash_password(password) == stored_hash

def account(newaccount):
    global current_user
    current_user = newaccount
    if newaccount != SHELL_USER and newaccount not in accounts:
        accounts[newaccount] = None
        user_list.append(newaccount)
    save_cache()
    return f"Switched to account '{newaccount}'"

def sign_out():
    account(SHELL_USER)
    return "Signed out. You are now on the temporary 'shell' session."

def set_password(old_password, new_password):
    username = current_user

    if username == SHELL_USER:
        return "Error: 'shell' is a temporary session, not an account. Use 'account <name>' to create one first."

    stored_hash = accounts.get(username)

    if stored_hash is None:
        if old_password != "":
            return "Error: Incorrect old password."
    elif _hash_password(old_password) != stored_hash:
        return "Error: Incorrect old password."

    if not new_password:
        return "Error: New password cannot be empty."

    accounts[username] = _hash_password(new_password)
    save_cache()
    return f"Password updated for account '{username}'."

def help():
    return (
        "Available commands:\n"
        "  show <text>          - Print the text\n"
        "  create <filename> <content> - Create a file with content\n"
        "  list                 - List your files (public in 'shell', private per account)\n"
        "  view <filename>      - Show the contents of a file\n"
        "  edit <filename>      - Open a full-screen text editor for a file\n"
        "                         (arrows/Home/End to move, Backspace/Del to remove,\n"
        "                         Ctrl+O to save, Ctrl+X to save and exit)\n"
        "  expr <expression>    - Evaluate a math expression\n"
        "  delete <filename>    - Delete a file\n"
        "  copy <src> <dest>    - Copy a file\n"
        "  public <filename>    - Copy a private file to the public TomFolder3000\n"
        "  private <filename>   - Copy a public file to your private storage\n"
        "  rename <old> <new>   - Rename a file\n"
        "  size <filename>      - Show a file's size\n"
        "  search <keyword>     - Search filenames and contents for a keyword\n"
        "  open <filename>      - Open a file with the default app\n"
        "  path                 - Show the TomFolder3000 storage path\n"
        "  date                 - Show the current date and time\n"
        "  history              - Show previously entered commands\n"
        "  clear                - Clear the terminal screen\n"
        "  account <name>       - Switch to (or create) an account\n"
        "  signout              - Sign out to the temporary 'shell' session\n"
        "  password             - Change the current account's password (interactive prompts)\n"
        "  me                   - Print the current username (whoami)\n"
        "  users                - List all accounts created\n"
        "  exit                 - Exit the terminal\n"
    )

def me():
    return current_user