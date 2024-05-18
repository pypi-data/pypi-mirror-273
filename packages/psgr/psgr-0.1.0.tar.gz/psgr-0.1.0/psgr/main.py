import json
import sys
import time
import base64
import os.path
import getpass
from tabulate import tabulate
import json
import rsa
from InquirerPy import inquirer
import signal



def main():

    def generateKeys():
        (pubkey, privkey) = rsa.newkeys(512)
        keyData = {
            "public_key": pubkey.save_pkcs1().decode(),
            "private_key": privkey.save_pkcs1().decode()
        }

        with open("keys.json", 'w') as f:
            json.dump(keyData, f)


    def fetchKeys():
        while True:
            try:
                with open("keys.json", "r") as f:
                    keyData = json.load(f)
                    pubkey = rsa.PublicKey.load_pkcs1(keyData['public_key'].encode())
                    privkey = rsa.PrivateKey.load_pkcs1(keyData['private_key'].encode())
                    return pubkey, privkey
            except FileNotFoundError:
                print("No Keys Found. Generating Keys. Please wait...")
                generateKeys()
            
        
    (pubkey, privkey) = fetchKeys()

    def encrypt(data, pubkey):
        return rsa.encrypt(data, pubkey)

    def decrypt(data, privkey):
        try: 
            return rsa.decrypt(data, privkey)
        except rsa.pkcs1.DecryptionError:
            print("Decryption Error. Did you change the keys?")
            return


    def refreshkeys():
        tempAccounts = {}
        (pubkey, privkey) = fetchKeys()
        for k,v in accounts.items():
            account, password = k, decrypt(base64.b64decode(v), privkey).decode("utf-8")
            tempAccounts[account] = password

        generateKeys()
        (pubkey, privkey) = fetchKeys()

        try:
            for account, password in tempAccounts.items():
                encyrptedPW = encrypt(password.encode("utf-8"), pubkey)
                tempAccounts[account] = base64.b64encode(encyrptedPW).decode("utf-8")

            with open("accountinfo.json", "w") as f:
                json.dump(tempAccounts, f)
        except Exception as e:
            print("An error occurred while writing to the file:", e)
            

    def assign_task(command, additional="", additional2="", additonal3=""):
        if command == "help":
            help()
        elif command == "add":
            add(additional, additional2)
        elif command == "show":
            show(additional)
            refreshkeys()
        elif command == "remove":
            remove(additional)
        elif command == "refresh":
            refreshkeys()
        elif command == "keys":
            (pub, priv) = fetchKeys()
            print(pub, priv)

        return

    def add(accountName="", password=""):
        (pubkey, privkey) = fetchKeys()
        if not accountName:
            accountName = input("Enter The Account Name: ")

        if accounts.get(accountName) is not None:
            message = input("Password for this account is already entered. Overrite? This cannot be undone. [Y]/[N]? ")
            if message.upper() == "N":
                return
            
        if not password:        
            password = getpass.getpass(f"Enter Password for {accountName}: ").encode("utf-8")
        else:
            password = password.encode("utf-8")

        encyrptedPW = encrypt(password, pubkey)
        accounts[accountName] = base64.b64encode(encyrptedPW).decode("utf-8")
        try:
            with open("accountinfo.json", "w") as f:
                json.dump(accounts, f)
        except Exception as e:
            print("An error occurred while writing to the file:", e)
        # print(accounts)
        return

    def show(name=""):
        (pubkey, privkey) = fetchKeys()
        showAccounts = {}
        for k,v in accounts.items():
            try:
                account, password = k, decrypt(base64.b64decode(v), privkey).decode("utf-8")
                showAccounts[account] = password
            except Exception as e:
                print("An error occured. Error:", e, "Have you changed the keys?")
                return
        
        if name == "all":
            # pprint.pprint(showAccounts)
            table_data = [(key, value) for key, value in showAccounts.items()]
            table = tabulate(table_data, headers=["Account", "Password"], tablefmt="github")
            print(table)
            print(" ")
        elif name == "accounts":
            print("Accounts: ")
            for key, _ in showAccounts.items():
                print(key)
            print(" ")

        else:
            if not name:
                chooseIt = []
                for k, v in accounts.items():
                    chooseIt.append(k)
                accountName = inquirer.select(
                    message = "Choose the account:",
                    choices = chooseIt
                ).execute()
            else:
                accountName = name

            if accountName not in showAccounts:
                message = input("Account not found. Add a new account with that name? [Y]/[N]? ")
                if message.upper() == "Y":
                    add(name)
                return
            else:
                table_data = [(accountName, showAccounts[accountName])]
                table = tabulate(table_data, headers=["Account", "Password"], tablefmt="github")
                print(table)
                print(" ")

        def ignore_ctrl_c(signum, frame):
            print("Ctrl+C is disabled.", end="\r")
        original_handler = signal.getsignal(signal.SIGINT)
        signal.signal(signal.SIGINT, ignore_ctrl_c)
        for i in range(5, 0, -1):
            print(f"clearing screen in {i} seconds.", end="\r")
            time.sleep(1)
        signal.signal(signal.SIGINT, original_handler)
        if os.name == 'nt':
            _ = os.system('cls')
        # For UNIX-like systems (Linux, macOS)
        else:
            _ = os.system('clear')
        return

    def help():
        help_message = """
    Passman - Password Manager

    Usage:
        passman command

    Commands:
        add          Add a new account
        show         Show account information
        refresh      Refresh account information
        help         Show this help message

    Examples:
        passman add Google                # Add a new account named "Google"
        passman add Facebook password     # Add a new account named "Facebook" with password "password"
        passman show all                       # Show all accounts
        passman show Google               # Show account information for "Google"
        passman refresh                     # Refresh account information

    For more information, visit: https://github.com/nareshkarthigeyan/passwordManager

    Note:
        - Passwords are encrypted at all times.
        - Passwords will disappear from the screen after 5 seconds.
    """
        print(help_message)
        return

    def remove(alll=""):
        message = inquirer.select(
                    message = "Choose Account:",
                    choices = ['Y', 'N']
                ).execute()
        if message.upper() == "Y":
            if alll == "all":
                with open("accountinfo.json", 'w') as json_file:
                    # Write an empty JSON object to the file
                    json.dump({}, json_file)
            else:
                chooseIt = []
                for k, v in accounts.items():
                    chooseIt.append(k)
                alll = inquirer.select(
                    message = "Choose Account:",
                    choices = chooseIt
                ).execute()

            if alll in accounts:
                accounts.pop(alll)
                with open("accountinfo.json", "w") as f:
                    json.dump(accounts, f)            
        return


    n = len(sys.argv)

    arguments = ("help", "add", "show", "remove", "keys", "refresh")

    if os.path.isfile("accountinfo.json"):
        with open("accountinfo.json", "r") as f:
            accounts = json.load(f)
    else:
        accounts = {}

    appname = "passman"

    if n < 2:
        print(f"Usage: {appname} command. Use {appname} help for more info.")
    elif sys.argv[1] not in arguments:
        print("No use for the command {", sys.argv[1], "} found. Try using appname.py help.")

    if n == 2:
        assign_task(sys.argv[1])
    elif n == 3:
        assign_task(sys.argv[1], sys.argv[2])
    elif n == 4:
        assign_task(sys.argv[1], sys.argv[2], sys.argv[3]) 


main()