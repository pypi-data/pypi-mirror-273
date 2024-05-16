<h1 align="center"><img src="./docs/jerry.png" alt="API Platform" width="350" height="250"></h1>

# SAES6 : Jerry

[![Stable Version](https://img.shields.io/pypi/v/saes6-jerry?color=blue)](https://pypi.org/project/saes6-jerry/)
[![Downloads](https://img.shields.io/pypi/dm/saes6-jerry)](https://pypistats.org/packages/saes6-jerry)

Table of Contents
---------------
- [Description](#description)
- [Installation](#installation)
- [Features](#features)
- [Developers](#developers)

## Description <a name="description"></a>
This tool is a command-line pentesting simulator designed to test the robustness of a system. It offers a variety of features to simulate attacks and identify potential vulnerabilities.

## Installation <a name="description"></a>
Insttal the following package :
```cmd
pip install saes6-jerry
```

## Features <a name="features"></a>
When installed, you can see the help with the folowing command :
```python
saes6-jerry --help
```

Our tool has the following features :
- [SSH Bruteforce](#ssh_bruteforce)
- [Get informations about a system](#system_infos)
- [Scan a specific network](#scan_network)


## Usage <a name="features"></a>
### SSH BruteForce <a name="ssh_bruteforce"></a>
```python
saes6-jerry bruteforce -ip <ip> [-t <numberOfThreads> --usersFileName <usersFileName> --passwordsFileName <passwordsFileName>]
```
**Exemple :**
```python
saes6-jerry bruteforce -ip 127.0.0.1 -t 3 --usersFileName ./users.txt --passwordsFileName ./passwords.txt
```

### Get informations about a system <a name="system_infos"></a>
```python
saes6-jerry systemInfo -ip <ip> [-p <listOfPorts> --start <startPort> --end <endPort>]
```
**Exemples :**

⚠️ You have to choose between the -p option and --start --end options

Scan the ports 20, 21 and 23.
```python
saes6-jerry systemInfo -ip 127.0.0.1 -p 20 21 23
```
Scan the ports between 1 and 65 included.
```python
saes6-jerry systemInfo -ip 127.0.0.1 --start 1 --end 65
```
⚠️ If -p, --start and --end are not specified, it will scan all ports

### Scan a specific network <a name="scan_network"></a>


## Developers <a name="developers"></a>
- GONZALES Lenny <img align="left" src="https://avatars.githubusercontent.com/u/91269114?s=64&v=4" alt="profile" width="20" height="20"/>
- SAADI Nils <img align="left" src="https://avatars.githubusercontent.com/u/91779594?v=4" alt="profile" width="20" height="20"/>
- SAUVA Mathieu <img align="left" src="https://avatars.githubusercontent.com/u/91150750?s=64&v=4" alt="profile" width="20" height="20"/>