Mac和Linux下已实践该方案可行

**pull.py**
```python
#! /usr/bin/env python3

import git
import os
from getpass import getpass

project_dir = os.path.dirname(os.path.abspath(__file__))
os.environ['GIT_ASKPASS'] = os.path.join(project_dir, 'askpass.py')
os.environ['GIT_USERNAME'] = username
os.environ['GIT_PASSWORD'] = getpass()
g = git.cmd.Git('/path/to/some/local/repo')
g.pull()
```
**askpass.py** (similar to this one)
This is in the same directory as pull.py and is not limited to Github only.
```python
#!/usr/bin/env python3
#
# Short & sweet script for use with git clone and fetch credentials.
# Requires GIT_USERNAME and GIT_PASSWORD environment variables,
# intended to be called by Git via GIT_ASKPASS.
#

from sys import argv
from os import environ

if 'username' in argv[1].lower():
    print(environ['GIT_USERNAME'])
    exit()

if 'password' in argv[1].lower():
    print(environ['GIT_PASSWORD'])
    exit()

exit(1)
```




Refrence:
[gitpython git authentication using user and password](https://stackoverflow.com/questions/44784828/gitpython-git-authentication-using-user-and-password)