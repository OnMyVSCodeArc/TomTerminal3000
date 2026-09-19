import os
from datetime import datetime
from sympy import sympify

current_user = "shell"
user_list = ["shell"]

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
        "  account <name>       - Switch to a different account\n"
        "  me                   - Show currently logged in user\n"
        "  users                - List all accounts created\n"
        "  exit                 - Exit the terminal\n"
    )

def me():
    return f"Current user: {current_user}"