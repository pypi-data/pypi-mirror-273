import argparse
from .attacks.systemInfo import getRemoteSystemInfo
from .attacks.bruteforce.bruteforce import bruteforce, USERS_FILE_NAME, PASSWORDS_FILE_NAME
from .attacks.executeCommands import execute
from .attacks.scanNetwork import scan
from .attacks.dump import get_users
from jerry import __version__

def main():
    print('''
 ▄▄▄██▀▀▀▓█████  ██▀███   ██▀███ ▓██   ██▓
   ▒██   ▓█   ▀ ▓██ ▒ ██▒▓██ ▒ ██▒▒██  ██▒
   ░██   ▒███   ▓██ ░▄█ ▒▓██ ░▄█ ▒ ▒██ ██░
▓██▄██▓  ▒▓█  ▄ ▒██▀▀█▄  ▒██▀▀█▄   ░ ▐██▓░
 ▓███▒   ░▒████▒░██▓ ▒██▒░██▓ ▒██▒ ░ ██▒▓░
 ▒▓▒▒░   ░░ ▒░ ░░ ▒▓ ░▒▓░░ ▒▓ ░▒▓░  ██▒▒▒ 
 ▒ ░▒░    ░ ░  ░  ░▒ ░ ▒░  ░▒ ░ ▒░▓██ ░▒░ 
 ░ ░ ░      ░     ░░   ░   ░░   ░ ▒ ▒ ░░
 ░   ░      ░  ░   ░        ░     ░ ░
                                  ░ ░
          ''')
    parser = argparse.ArgumentParser(description="Simulateur d'attaques cyber")

    parser.add_argument("-v", "--version", action="store_true", help="Display version")
    parser.add_argument("attack", choices=["bruteforce","systemInfo","execute","scan","dump",""], default="", const="", nargs="?", help="Type of attack")
    parser.add_argument("-ip", type=str, help="Target IP")
    parser.add_argument("-t", "--threads", type=int, default=1, help="Number of thread(s) (default : 1)")
    parser.add_argument("-p", "--ports", nargs="+", type=int, help="List ports")
    parser.add_argument("--start", type=int, default=0, help="start port")
    parser.add_argument("--end", type=int, default=65535, help="end port")
    parser.add_argument("--usersFileName", type=str, default=USERS_FILE_NAME, help=f"users file name (default : {USERS_FILE_NAME})")
    parser.add_argument("--passwordsFileName", type=str, default=PASSWORDS_FILE_NAME, help=f"passwords file name (default : {PASSWORDS_FILE_NAME})")
    parser.add_argument("-U", "--user", type=str, help="username")
    parser.add_argument("-P", "--password", type=str, help="password")
    parser.add_argument("-cmd", "--commands", type=str, help="Path to the file containing the commands to execute")
    parser.add_argument("-i", "--info",  type=bool, default=False, help="Get system info")
    parser.add_argument("--os", type=str, help="Operating system of the remote system (Windows/Linux)")

    args = parser.parse_args()

    if args.version:
        print(f"Version {__version__}")
        return

    match args.attack:
        case "bruteforce":
            bruteforce(args.ip, args.threads, args.usersFileName, args.passwordsFileName)
        case "systemInfo":
            getRemoteSystemInfo(args.ip, args.start, args.end, args.ports)
        case "execute":
            execute(args.ip, args.user, args.password, args.commands)
        case "scan":
            scan(args.ip, args.info, args.start, args.end, args.ports, args.threads)
        case "dump":
            get_users(args.user, args.password, args.ip, args.os)
        case _:
            print("Attack not known !")