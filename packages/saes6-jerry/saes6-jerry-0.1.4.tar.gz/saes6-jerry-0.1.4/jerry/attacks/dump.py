import subprocess

def get_users(user, password, ipAddress, os):
    try:
        if os == "Windows":
            command = f"sshpass -p {password} ssh -tt {user}@{ipAddress} 'wmic useraccount get name,sid'"
        elif os == "Linux":
            command = f"sshpass -p {password} ssh -tt {user}@{ipAddress} 'echo {password} | sudo -S cat /etc/shadow'"
        else:
            print("Unsupported operating system")
            return

        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            users = result.stdout.splitlines()
            for user in users:
                print(user)
        else:
            print(f"Error retrieving users: {result.stderr}")

    except Exception as e:
        print(f"An error occurred: {e}")