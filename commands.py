import os
import shutil
from datetime import datetime
from sympy import sympify

current_user = "shell"
user_list = ["shell"]
command_history = []

STORAGE_DIR = os.path.join(os.path.expanduser("~"), "Documents", "TomFolder3000")

def create_file(args_string):
    parts = args_string.split(maxsplit=1)

    if len(parts) < 2:
        return "Error: Use 'create <filename> <content>'"

    filename = parts[0]
    content = parts[1]

    os.makedirs(STORAGE_DIR, exist_ok=True)
    filepath = os.path.join(STORAGE_DIR, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    return f"Created file '{filename}' successfully in '{STORAGE_DIR}'."

def list_files():
    if not os.path.isdir(STORAGE_DIR) or not os.listdir(STORAGE_DIR):
        return "TomFolder3000's Files:\n(empty)"

    output = "TomFolder3000's Files:\n"
    for filename in os.listdir(STORAGE_DIR):
        filepath = os.path.join(STORAGE_DIR, filename)
        created = datetime.fromtimestamp(os.path.getctime(filepath)).strftime("%Y-%m-%d %H:%M:%S")
        output += f"{filename} ({created})\n"
    return output.strip()

def view_file(filename):
    filepath = os.path.join(STORAGE_DIR, filename)

    if not os.path.isfile(filepath):
        return f"Error: File '{filename}' not found."

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    except UnicodeDecodeError:
        return f"Error: Cannot view '{filename}' as text (it may be an image, video, or other binary file)."

def calculate(expression_string):
    try:
        return str(sympify(expression_string))
    except Exception:
        return "Error: Invalid math expression."

def delete_file(filename):
    filepath = os.path.join(STORAGE_DIR, filename)
    if os.path.isfile(filepath):
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
    return STORAGE_DIR

def open_file(filename):
    filepath = os.path.join(STORAGE_DIR, filename)

    if not os.path.isfile(filepath):
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

    src, dest = parts[0], parts[1]
    src_path = os.path.join(STORAGE_DIR, src)
    dest_path = os.path.join(STORAGE_DIR, dest)

    if not os.path.isfile(src_path):
        return f"Error: File '{src}' not found."

    shutil.copy(src_path, dest_path)
    return f"Copied '{src}' to '{dest}'."

def rename_file(args_string):
    parts = args_string.split(maxsplit=1)

    if len(parts) < 2:
        return "Error: Use 'rename <old> <new>'"

    old, new = parts[0], parts[1]
    old_path = os.path.join(STORAGE_DIR, old)
    new_path = os.path.join(STORAGE_DIR, new)

    if not os.path.isfile(old_path):
        return f"Error: File '{old}' not found."
    if os.path.exists(new_path):
        return f"Error: File '{new}' already exists."

    os.rename(old_path, new_path)
    return f"Renamed '{old}' to '{new}'."

def get_size(filename):
    filepath = os.path.join(STORAGE_DIR, filename)

    if not os.path.isfile(filepath):
        return f"Error: File '{filename}' not found."

    size_bytes = os.path.getsize(filepath)
    if size_bytes < 1024:
        return f"{filename}: {size_bytes} bytes"
    return f"{filename}: {size_bytes / 1024:.2f} KB"

def search_files(keyword):
    if not os.path.isdir(STORAGE_DIR) or not os.listdir(STORAGE_DIR):
        return "No files to search."

    matches = []
    for filename in os.listdir(STORAGE_DIR):
        filepath = os.path.join(STORAGE_DIR, filename)
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

def account(newaccount):
    global current_user
    current_user = newaccount
    if newaccount not in user_list:
        user_list.append(newaccount)
    return f"Switched to account '{newaccount}'"

def help():
    return (
        "Available commands:\n"
        "  show <text>          - Print the text\n"
        "  create <filename> <content> - Create a file with content\n"
        "  list                 - List all files in TomFolder3000\n"
        "  view <filename>      - Show the contents of a file\n"
        "  expr <expression>    - Evaluate a math expression\n"
        "  delete <filename>    - Delete a file\n"
        "  copy <src> <dest>    - Copy a file\n"
        "  rename <old> <new>   - Rename a file\n"
        "  size <filename>      - Show a file's size\n"
        "  search <keyword>     - Search filenames and contents for a keyword\n"
        "  open <filename>      - Open a file with the default app\n"
        "  path                 - Show the TomFolder3000 storage path\n"
        "  date                 - Show the current date and time\n"
        "  history              - Show previously entered commands\n"
        "  clear                - Clear the terminal screen\n"
        "  account <name>       - Switch to a different account\n"
        "  me                   - Print the current username (whoami)\n"
        "  users                - List all accounts created\n"
        "  exit                 - Exit the terminal\n"
    )

def me():
    return current_user