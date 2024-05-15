def bruteforce(ip, duration):
    if not ip or not duration:
        raise ValueError("ip or duration nor provided")
    print(f"BruteForce d'attaque sur la cible {ip} pendant {duration} secondes...")
    print("BruteForce terminée.")