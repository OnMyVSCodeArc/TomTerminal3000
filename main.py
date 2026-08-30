import commands

while True:
    user_input = input(commands.current_user + " >> ").strip()
    
    if not user_input:
        continue
        
    tokens = user_input.split(maxsplit=1)
    cmd = tokens[0]
    args = tokens[1] if len(tokens) > 1 else ""

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
    else:
        print(f"Unknown command: '{cmd}'")