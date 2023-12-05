**git maildiff**

![maildiff.svg](http://img.shields.io/badge/pypi-3.7.0-green.svg?style=flat-square)
![Django.svg](https://img.shields.io/pypi/l/Django.svg)
![green.svg](https://img.shields.io/badge/issues-0_Open-green.svg?style=flat-square)

**maildiff** is a simple git command to email diff in color to reviewer/ co-worker.

Install
-------

Navigate to git-maildiff directory you cloned or downlaoded from terminal 

	pip install .

where . refers to your current working directory i.e. inside git-maildiff
and you are good to go.

Uninstall
---------

	pip  uninstall  maildiff

Setup Config
------------

	git config --global maildiff.mailto recipient@email.com	

	git config --global maildiff.smtpserver smtp.gmail.com	

	git config --global maildiff.smtpserverport 587	

	git config --global maildiff.mailFrom sender@email.com	

	git config --global maildiff.smtpencryption tls

e.g. Gmail uses tls encryption

if you forget to run the above setup the git maildiff command will prompts each 
one by one and update in .gitconfig the email password is stored in OS keychain.

Usage
-----

**git maildiff** - Email the diff of commited or uncommited changes in colored to multiple recipients and allows attaching patches.

**git maildiff -d 'HEAD^1'** - will email the diff.

when no -diff or -d flag is passed with value the default value is **git diff HEAD^ HEAD**

**git maildiff -to email@domain.com** - will email diff to this email address.

**git maildiff -v** - use the -v flag to enable verbosity and display what command is run and what is the result of executed command.

**type git maildiff -h** in shell for more help.

Note
----

If you are behind a proxy server, and you are having issues accessing git repository you can update gitconfig to add
proxy settings like 

	git config --global http.proxy http://mydomain\\myusername:mypassword@myproxyserver:8080

Dependencies
------------

- [argparse](https://docs.python.org/2.7/library/argparse.html)

- [keyring](https://pypi.python.org/pypi/keyring)

- [logging](https://docs.python.org/2/library/logging.html)

- [colorlog](https://pypi.python.org/pypi/colorlog/2.6.0)

- [colorama](https://pypi.python.org/pypi/colorama/0.3.3) (for windows only)


######Type **git maildiff -h** for help in command line/ terminal
 
## Contact

**Email:** <sansupercool@duck.com>

**Website:** [www.devilsan.com](http://devilsan.weebly.com "click to got to website")