import socket
from ..utils import getBasicSystemInfo

def scanSinglePort(ip, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((ip, port))
        sock.close()
        return result;
    except KeyboardInterrupt:
        strToReturn = "Scan canceled."
        print(strToReturn)
        return strToReturn
    except socket.gaierror:
        strToReturn = "Unable to resolve host. Please check the IP address."
        print(strToReturn)
        return strToReturn
    except socket.error:
        strToReturn = "Failed to connect to the server."
        print(strToReturn)
        return strToReturn

def scanPorts(ip, startPort, endPort, ports):
    openPorts = []
    if ports:
        print("Scan ports : " + str(ports))
        for port in ports:
            if scanSinglePort(ip, port) == 0:
                openPorts.append(port)
                print(f"Port {port} is open.")
    else:        
        print("Scan ports : " + str(startPort) + " to " + str(endPort))
        for port in range(startPort, endPort):
            if scanSinglePort(ip, port) == 0:
                openPorts.append(port)
                print(f"Port {port} is open.")
    if (len(openPorts) == 0):
        print("No port open.")

def getRemoteSystemInfo(ipAddress, startPort, endPort, ports):
    infos = getBasicSystemInfo(ipAddress)
    print(f"{ipAddress} : {infos}")
    scanPorts(ipAddress, startPort, endPort, ports)