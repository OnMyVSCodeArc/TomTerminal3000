from sympy import sympify

virtual_drive = {}
current_user = "shell"
user_list = ["shell"]

def create_file(args_string):
    parts = args_string.split(maxsplit=1)
    
    if len(parts) < 2:
        return "Error: Use 'create <filename> <content>'"
        
    filename = parts[0]
    content = parts[1]
    
    virtual_drive[filename] = content
    return f"Created file '{filename}' successfully."

def list_files():
    if not virtual_drive:
        return "[Isolated Zone is empty]"
    
    output = "--- Isolated Files ---\n"
    for filename in virtual_drive.keys():
        output += f"📄 {filename}\n"
    return output.strip()

def calculate(expression_string):
    try:
        return str(sympify(expression_string))
    except Exception:
        return "Error: Invalid math expression."

def delete_file(filename):
    if filename in virtual_drive:
        del virtual_drive[filename]
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
        "  list                 - List all files in the memory\n"
        "  expr <expression>    - Evaluate a math expression\n"
        "  delete <filename>    - Delete a file\n"
        "  account <name>       - Switch to a different account\n"
        "  me                   - Show currently logged in user\n"
        "  users                - List all accounts created\n"
        "  exit                 - Exit the terminal\n"
    )

def me():
    return f"Current user: {current_user}"