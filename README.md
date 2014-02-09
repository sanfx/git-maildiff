# Git ipush



> **ipush** is git command to push and email diff in color

###Install
1. Copy the downloaded git-ipush and send.py in the path where your environment variable PATH can access.
2. make the git-ipush command executable. e.g.
	chmod +x git-ipush
3. Now you are ready to setup your config from from command line/terminal.


###Setup Config

***git config --global ipush.mailto recipient@email.com***

***git config --global ipush.smtpserver smtp.gmail.com***

***git config --global ipush.smtpserverport 587***

***git config --global ipush.mailFrom sender@email.com***

***git config --global ipush.smtpencryption tls*** 
e.g. Gmail uses tls encryption

if you forget to run the above setup the git ipush command will prompts each 
one by one and update in .gitconfig the email password is stored in OS keychain.

###Usage

**git ipush** - will push the last commit and email the colored diff.

**git ipush -d 'HEAD^1'** - will email the diff but not push as we are requesting to do diff of uncommited tree.

######Note
when no -diff or -d flag is passed with value the default value is **git diff HEAD^ HEAD**


**git ipush -to email@domain.com** - will push the last commit and email diff to this email address.

 **git ipush -v** - use the -v flag to enable verbosity and display what command is run and what is the result of executed command.

######Type **git ipush -h** for help in command line/ terminal
 
## Contact

**Email:** <skysan@gmail.com>

**Website:** [www.devilsan.com](http://www.devilsan.com "click to got to website")