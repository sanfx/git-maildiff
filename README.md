# Git ipush



> **ipush** is git command to push and email diff in color

###Setup Config

***git config --global ipush.mailto recipient@email.com***

***git config --global ipush.smtpserver smtp.gmail.com***

***git config --global ipush.smtpserverport 587***

***git config --global ipush.mailFrom sender@email.com***

***git config --global ipush.smtpencryption tls*** 
e.g. Gmail uses tls encryption


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