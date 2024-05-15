import argparse
from .attacks.bruteforce import bruteforce

def main():
    parser = argparse.ArgumentParser(description="Simulateur d'attaques cyber")
    parser.add_argument("attack", choices=["bruteforce"], help="Type of attack")
    parser.add_argument("-d", "--duration", type=int, default=60, help="Duration of the attack in seconds (default : 60)")
    parser.add_argument("-ip", type=str, help="target IP")

    args = parser.parse_args()

    match args.attack:
        case "bruteforce":
            bruteforce(args.ip, args.duration)
        case _:
            print("Attack not known !")