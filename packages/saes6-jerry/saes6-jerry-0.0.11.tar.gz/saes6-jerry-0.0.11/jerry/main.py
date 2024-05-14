import argparse

def simulate_attack(target, duration):
    print(f"Simulation d'attaque sur la cible {target} pendant {duration} secondes...")
    print("Simulation terminée.")

def main():
    parser = argparse.ArgumentParser(description="Simulateur d'attaques cyber")
    parser.add_argument("cible", help="Cible de l'attaque")
    parser.add_argument("-d", "--duree", type=int, default=60, help="Durée de la simulation en secondes (par défaut : 60)")

    args = parser.parse_args()
    simulate_attack(args.cible, args.duree)