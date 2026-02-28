**git maildiff**

![Python Version](https://img.shields.io/badge/Python-3.7%2B-blue.svg)
![PyPI - License](https://img.shields.io/pypi/l/maildiff.svg)
![Issues - Open](https://img.shields.io/badge/issues-0_Open-green.svg?style=flat-square)

**maildiff** is a simple git command to send diff in color to reviewer/ co-worker through email.


Install
-------

Navigate to git-maildiff directory you cloned or downloaded from terminal 

	pip install .

Uninstall
---------

	pip uninstall maildiff

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

- [argparse](https://docs.python.org/3/library/argparse.html)

- [keyring](https://pypi.org/project/keyring/)

- [logging](https://docs.python.org/3/library/logging.html)


######
Type **git maildiff -h** for help in command line/ terminal
 
## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Contact

For any questions or issues, please open an issue on this GitHub repository or contact [Sanjeev Kumar](sanfx.github.io)

---

⭐️ Don't forget to star the repository if you find it useful!

