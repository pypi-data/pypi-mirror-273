import requests
import platform
import socket
import paramiko

""" Get file content from local or remote file. """
def getFileContent(filePath):
    if filePath.startswith('http://') or filePath.startswith('https://'):  # Remote file
        response = requests.get(filePath)
        response.raise_for_status()
        return response.text.splitlines()
    else:  # Local file
        with open(filePath, 'r') as f:
            return f.readlines()

""" Get basic system infos by socket connection """
def getBasicSystemInfo(ipAddress):
    try:
        # Create a socket to establish a connection with the specified IP address
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)  # Set a timeout for the connection
        sock.connect((ipAddress, 22))  # Attempt to connect to SSH port (22)
        
        # Get information about the remote system
        sysInfo = {
            "System": platform.system(),
            "Node Name": platform.node(),
            "Release": platform.release(),
            "Version": platform.version(),
            "Machine": platform.machine(),
            "Processor": platform.processor()
        }
        
        return sysInfo
    except socket.timeout:
        strToReturn = "The connection timed out. Please check the IP address and ensure that the remote system is accessible."
        print(strToReturn)
        return strToReturn

    except ConnectionRefusedError:
        strToReturn = "The connection was refused. Please check that the SSH service is running on the remote system."
        print(strToReturn)
        return strToReturn

    except Exception as e:
        strToReturn = f"An error occurred: {e}"
        print(strToReturn)
        return strToReturn



""" Execute commands using SSH """
def executeCommands(ip, user, password, commands):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(ip, username=user.strip(), password=password.strip())   # Connect to the target
        print(f"[✓] Successfully connected with {user.strip()}:{password.strip()}")
        print(f"[INFO] Trying to run commands...")

        for command in commands:
            print(f"[INFO] Trying command {command}")
            stdin, stdout, stderr = ssh.exec_command(command)
            print(stdout.read().decode())

        ssh.close()
    except paramiko.AuthenticationException:
        print(f"[X] Authentication Failure (Wrong user or password) - {user.strip()}:{password.strip()}")
    except paramiko.SSHException as e:
        print(f"[X] SSH connection failed - {user.strip()}:{password.strip()} : {e}")
    except Exception as e:
        print(f"[X] Failed to connect - {user.strip()}:{password.strip()} : {e}")
