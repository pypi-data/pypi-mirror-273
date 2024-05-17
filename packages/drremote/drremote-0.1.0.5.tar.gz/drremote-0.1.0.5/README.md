# DRRemote

DRRemote is a python modul which offers access to Davinci Resolve Studio.
At the time the functionality is very basic. DRRemote is used in conjunction with [LRDavinci](https://github.com/sto3014/LRDavinci).
LRDavinci is a Lightroom plug-in for Davinci Resolve Studio

## Features
* Changes the current timeline
* Retrieves the attributes for the current timeline 
  * name, type and ipaddress of database
  * name of project
  * name of timeline

## Requirements
* Python 3.6 (not more, not less due to Davinci Resolve restrictions)  
* Davinci Resolve Studio (license is needed for Davinci Resolve's Python API).

## Installation
1. [Python](https://www.python.org/downloads/)  
    You need to install version 3.6.x.
2. PIP 
   * Windows
        * python -m pip install --upgrade pip
   * macOS
        * curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py  
        * python get-pip.py
3. DRRemote
   * pip install drremote
4. Davinci Resolve scripting environment  
   See readme file:  
  macOS  
  ```/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting/README.txt```  
  Windows  
    ```%PROGRAMDATA%\Blackmagic Design\DaVinci Resolve\Support\Developer\Scripting\README.txt```
## Usage
You must execute __DRRemote__ in a command prompt (Windows) or terminal (macOS).  
Remarks for Windows:  
After you installed drremote with PIP, an executable is created as well: 
```
%APPDATA%\Programs\Python\Python36\Scripts\drremote.exe.
```
To execute drremote.exe you must use the full path or extend your PATH variable.

A simple example:
* Start Davinci Resolve Studio, open a project and select a timeline
* Open a Command Prompt/Terminal and type:
```
drremote -m gettimeline -o out.txt
```
If successful you find the gathered information in file out.txt in your current directory:
```
Success
project=Snippets
timeline=2021-12-10-First Snow
database=2021:Disk
```
If you get an error, you may find some more information in the log logfile:
* MacOS  
  * $TMPDIR/drremote.log
* Windows  
  * %TEMP%/drremote.log


For the commandline arguments see ```drremote --help```:
```
usage: drremote [-h] -m {settimeline,gettimeline} [-p PROJECT [PROJECT ...]]
                [-t TIMELINE [TIMELINE ...]] [-d DATABASE [DATABASE ...]] -o
                OUTPUT_PATH [OUTPUT_PATH ...] [-w WAIT]

optional arguments:
  -h, --help            show this help message and exit
  -m {settimeline,gettimeline}, --mode {settimeline,gettimeline}
                        The operating mode.
  -p PROJECT [PROJECT ...], --project PROJECT [PROJECT ...]
                        The name of a project
  -t TIMELINE [TIMELINE ...], --timeline TIMELINE [TIMELINE ...]
                        The name of a timeline
  -d DATABASE [DATABASE ...], --database DATABASE [DATABASE ...]
                        The database. The format is: DbName:DbType for disk
                        driven databases and DbName:DbType:IpAddress for
                        PostgreSQL databases
  -o OUTPUT_PATH [OUTPUT_PATH ...], --output-path OUTPUT_PATH [OUTPUT_PATH ...]
                        The name and path of the output file. This file holds
                        the result like timeline attributes or error messages.
  -w WAIT, --wait WAIT  Amounts of seconds to wait between the first and
                        second connection attempt
```

###Examples  
#### Set the current timeline in Davinci resolve   
```
drremote -m settimeline -t "2021-12-10-First Snow" -p Snippets -d 2021:disk -o out.txt
```  

#### Get the current timeline IDs  
```
drremote -m gettimeline -o out.txt
```
The result is written into __out.txt__:
```
Success
project=Snippets
timeline=2021-12-10-First Snow
database=2021:Disk
```
