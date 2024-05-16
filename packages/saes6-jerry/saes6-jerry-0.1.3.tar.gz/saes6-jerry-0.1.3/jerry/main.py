import argparse
from .attacks.sys_infos import getRemoteSystemInfo
from .attacks.bruteforce.bruteforce import bruteforce, USERS_FILE_NAME, PASSWORDS_FILE_NAME, NUMBER_OF_THREADS

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
    parser.add_argument("attack", choices=["bruteforce","systemInfo",""], default="", const="", nargs="?", help="Type of attack")
    parser.add_argument("-ip", type=str, help="Target IP")
    parser.add_argument("-t", "--threads", type=int, default=1, help="Number of thread(s) (default : 1)")
    parser.add_argument("-p", "--ports", nargs="+", type=int, help="List ports")
    parser.add_argument("--start", type=int, default=1, help="start port")
    parser.add_argument("--end", type=int, default=65536, help="end port")
    parser.add_argument("--usersFileName", type=str, default=USERS_FILE_NAME, help=f"users file name (default : {USERS_FILE_NAME})")
    parser.add_argument("--passwordsFileName", type=str, default=PASSWORDS_FILE_NAME, help=f"passwords file name (default : {PASSWORDS_FILE_NAME})")

    args = parser.parse_args()

    if args.version:
        print(f"Version {__version__}")
        return

    match args.attack:
        case "bruteforce":
            bruteforce(args.ip, args.threads, args.usersFileName, args.passwordsFileName)
        case "systemInfo":
            getRemoteSystemInfo(args.ip, args.start, args.end, args.ports)
        case _:
            print("Attack not known !")