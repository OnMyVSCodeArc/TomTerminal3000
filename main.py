import sys
import getpass
import curses
from core import commands, editor

def prompt_password(prompt):
    if sys.stdin.isatty():
        return getpass.getpass(prompt)
    return input(prompt)

while True:
    user_input = input(commands.current_user + " >> ").strip()
    
    if not user_input:
        continue
        
    tokens = user_input.split(maxsplit=1)
    cmd = tokens[0]
    args = tokens[1] if len(tokens) > 1 else ""

    if cmd != "history":
        commands.record_history(user_input)

    if cmd == "show":
        if not args:
            print("Error: Nothing to show.")
        else:
            print(args)
            
    elif cmd == "create":
        if not args:
            print("Error: Missing filename and content.")
        else:
            response = commands.create_file(args)
            print(response)
            
    elif cmd == "list":
        response = commands.list_files()
        print(response)

    elif cmd == "view":
        if not args:
            print("Error: Missing filename.")
        else:
            response = commands.view_file(args)
            print(response)

    elif cmd == "edit":
        if not args:
            print("Error: Missing filename.")
        else:
            filename = args
            lines, error = commands.read_for_edit(filename)
            if error:
                print(error)
            else:
                def do_save(current_lines):
                    return commands.save_edit(filename, current_lines)

                curses.wrapper(editor.run_editor, filename, lines, do_save)
                print(commands.save_edit(filename, lines))
        
    elif cmd == "expr":
        if not args:
            print("Error: Missing math expression.")
        else:
            response = commands.calculate(args)
            print(response)
            
    elif cmd == "delete":
        if not args:
            print("Error: Missing filename.")
        else:
            response = commands.delete_file(args)
            print(response)

    elif cmd == "help":
        print(commands.help())
    
    elif cmd == "account":
        if not args:
            print("Error: Missing account name.")
        elif commands.account_exists(args) and commands.account_has_password(args):
            entered_password = prompt_password("Password: ")
            if commands.verify_password(args, entered_password):
                print(commands.account(args))
            else:
                print("Error: Incorrect password.")
        else:
            response = commands.account(args)
            print(response)

    elif cmd == "exit":
        print("Exiting terminal. Press Enter to close.")
        input()
        break

    elif cmd == "me":
        response = commands.me()
        print(response)
    
    elif cmd == "users":
        print("Available users:")
        for user in commands.user_list:
            print(f"  - {user}")

    elif cmd == "date":
        print(commands.get_date())

    elif cmd == "clear":
        commands.clear_screen()

    elif cmd == "history":
        print(commands.get_history())

    elif cmd == "path":
        print(commands.get_path())

    elif cmd == "open":
        if not args:
            print("Error: Missing filename.")
        else:
            response = commands.open_file(args)
            print(response)

    elif cmd == "copy":
        if not args:
            print("Error: Missing source and destination filenames.")
        else:
            response = commands.copy_file(args)
            print(response)

    elif cmd == "public":
        if not args:
            print("Error: Missing filename.")
        else:
            print(commands.publish_file(args))

    elif cmd == "private":
        if not args:
            print("Error: Missing filename.")
        else:
            print(commands.privatize_file(args))

    elif cmd == "rename":
        if not args:
            print("Error: Missing old and new filenames.")
        else:
            response = commands.rename_file(args)
            print(response)

    elif cmd == "size":
        if not args:
            print("Error: Missing filename.")
        else:
            response = commands.get_size(args)
            print(response)

    elif cmd == "search":
        if not args:
            print("Error: Missing search keyword.")
        else:
            response = commands.search_files(args)
            print(response)

    elif cmd == "signout":
        print(commands.sign_out())

    elif cmd == "password":
        old_password = prompt_password("Enter your old password: ")
        new_password = prompt_password("Enter your new password: ")
        confirm_password = prompt_password("Confirm your new password: ")
        if new_password != confirm_password:
            print("Error: New passwords do not match.")
        else:
            response = commands.set_password(old_password, new_password)
            print(response)

    else:
        print(f"Unknown command: '{cmd}'")