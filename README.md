# Git maildiff



> **maildiff** is a simple git command to email diff in color to reviewer/ co-worker.

###Install
Navigate to git-maildiff directory you cloned/ downlaoded
from terminal 

run ***$ python setup.py install***

and you are good to go.

###Setup Config

***git config --global maildiff.mailto recipient@email.com***

***git config --global maildiff.smtpserver smtp.gmail.com***

***git config --global maildiff.smtpserverport 587***

***git config --global maildiff.mailFrom sender@email.com***

***git config --global maildiff.smtpencryption tls*** 
e.g. Gmail uses tls encryption

if you forget to run the above setup the git maildiff command will prompts each 
one by one and update in .gitconfig the email password is stored in OS keychain.

###Usage

**git maildiff** - will push the last commit and email the colored diff.

**git maildiff -d 'HEAD^1'** - will email the diff but not push as we are requesting to do diff of uncommited tree.

###Dependencies

**argparse**
**keyring**
**logging**
**colorlog**
**colorama** (for windows only)

######Note
when no -diff or -d flag is passed with value the default value is **git diff HEAD^ HEAD**


**git maildiff -to email@domain.com** - will push the last commit and email diff to this email address.

 **git maildiff -v** - use the -v flag to enable verbosity and display what command is run and what is the result of executed command.

######Type **git maildiff -h** for help in command line/ terminal
 
## Contact

**Email:** <skysan@gmail.com>

**Website:** [www.devilsan.com](http://www.devilsan.com "click to got to website")

[![Licence]( http://i.creativecommons.org/l/by-nc-sa/4.0/80x15.png )](https://raw.github.com/sanfx/git-maildiff/master/LICENSE)