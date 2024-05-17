from ..utils import getBasicSystemInfo, getFileContent, executeCommands

""" Get Default commands depends on the os """
def getDefaultCommands(ip, user):
    systemInfo = getBasicSystemInfo(ip)
    systemName = systemInfo.get('System').lower()

    securityText = "Security Test"
    COMMANDS_WINDOWS = [
        f'echo "{securityText}"> C:\\Windows\Temp\\test.txt',
        'fsutil file createnew C:\\Users\Public\\test.txt 0',
        'fsutil file createnew C:\\ProgramData\\test.txt 0',
        'fsutil file createnew C:\\Windows\System32\\test.txt 0'
    ]
    COMMANDS_LINUX = [
        f'echo {securityText} > /var/log/test.txt',
        f'touch /home/{user}/test.txt',
        f'echo {securityText} >> /root/test.txt',
        f'echo {securityText} >> /tmp/test.txt'
    ]

    return COMMANDS_LINUX if systemName == 'darwin' or systemName == 'linux'  else COMMANDS_WINDOWS


""" Get and execute commands using SSH """
def execute(ip, user, password, commandsFileName):
    if not commandsFileName:
        commands = getDefaultCommands(ip, user)
    else:
        commands = getFileContent(commandsFileName)
    executeCommands(ip, user, password, commands)