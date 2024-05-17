from .sys_infos import getRemoteSystemInfo
import subprocess
import ipaddress
import platform
import threading
import subprocess

def ping(host):
    #define param if os is linux or windows
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    command = ['ping', param, '1', host]
    
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()
    
    return process.returncode == 0

def scan(ip, info, startPort, endPort, ports, threads):
    print("[INFO] Start scan")
    
    def scanSingle(threadNumber, ip):
        if ping(ip):
            print(f"[✓] [Thread {threadNumber}] {ip} is reachable")
            if info:
                getRemoteSystemInfo(ip, startPort, endPort, ports)
        else:
            print(f"[X] [Thread {threadNumber}] {ip} is not reachable")
    ipList = list(ipaddress.IPv4Network(ip).hosts())
    threadsList = []
    for i in range(0, len(ipList) + 1, threads):
        for j in range(threads):    # create all the threads
            thread = threading.Thread(target=scanSingle, args=(j+1, str(ipList[i+j]),))
            thread.start()
            threadsList.append(thread)
        for thread in threadsList:
            thread.join()
        print('end')

    print("[INFO] End scan")