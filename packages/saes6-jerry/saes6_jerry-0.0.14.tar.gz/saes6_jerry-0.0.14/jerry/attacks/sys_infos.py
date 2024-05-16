import platform
import socket

def getRemoteSystemInfo(ipAddress, startPort, endPort, ports):
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
        
        print(ipAddress + f": {sysInfo['System']}, 'Node Name': {sysInfo['Node Name']}, 'Release': {sysInfo['Release']}, 'Version': {sysInfo['Version']}, 'Machine': {sysInfo['Machine']}, 'Processor': {sysInfo['Processor']}")

    except socket.timeout:
        print("The connection timed out. Please check the IP address and ensure that the remote system is accessible.")
        return None

    except ConnectionRefusedError:
        print("The connection was refused. Please check that the SSH service is running on the remote system.")
        return None

    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    
    scanPorts(ipAddress, startPort, endPort, ports)

def scanPorts(ipAddress, startPort, endPort, ports):
    openPorts = []
    try:
        if ports:
            print("Scan ports : " + str(ports))
            for port in ports:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                result = sock.connect_ex((ipAddress, port))
                if result == 0:
                    openPorts.append(port)
                    print(f"Port {port} is open.")
                sock.close()
        else:        
            print("Scan ports : " + str(startPort) + " to " + str(endPort))
            for port in range(startPort, endPort + 1):
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)  # Set a timeout for the connection
                result = sock.connect_ex((ipAddress, port))  # Try to connect to the port
                if result == 0:
                    openPorts.append(port)
                    print(f"Port {port} is open.")
                sock.close()
    except KeyboardInterrupt:
        print("\nScan canceled.")
        exit()
    except socket.gaierror:
        print("Unable to resolve host. Please check the IP address.")
        exit()
    except socket.error:
        print("Impossible d'établir une connexion au serveur.")
        exit()

    if (len(openPorts) == 0):
        print("No port open.")