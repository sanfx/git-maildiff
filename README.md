# Git ipush



> **ipush** is git command to push and email diff in color


###Usage

**git ipush** - will push the last commit and email the colored diff.

**git ipush -d 'HEAD^1'** - will email the diff but not push as we are requesting to do diff of uncommited tree.

######Note
when no -diff or -d flag is passed with value the default value is **git diff HEAD^ HEAD**


**git ipush -to email@domain.com** - will push the last commit and email diff to this email address.

 **git ipush -v** - use the -v flag to enable verbosity and display what command is run and what is the result of executed command.
 
 
## Contact

**Email:** <skysan@gmail.com>

**Website:** [www.devilsan.com](http://www.devilsan.com "click to got to website")

**iPush Page** [hhttp://goo.gl/3NEHvn](http://goo.gl/3NEHvn "Click to read story behind how it came up!!!")