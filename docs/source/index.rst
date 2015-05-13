.. maildiff command for git documentation master file, created by
   sphinx-quickstart on Tue May 12 22:03:45 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to maildiff git command documentation!
==============================================

Git command to email the color diff and patches in email from shell to single or multiple users.

User Notes:
===========

**git maildiff** - Email the diff of commited or uncommited changes in colored to multiple recipients and allows attaching patches.

**git maildiff -d 'HEAD^1'** - will email the diff.

when no -diff or -d flag is passed with value the default value is **git diff HEAD^ HEAD**

**git maildiff -to email@domain.com** - will email diff to this email address.

**git maildiff -v** - use the -v flag to enable verbosity and display what command is run and what is the result of executed command.

**type git maildiff -h** in shell for more help.
.. toctree::
   :maxdepth: 2
   send
   maildiff

Requirements:
=============
**Python 2.7 or above**

Install Notes
=============

Navigate to git-maildiff directory you cloned/ downlaoded
from terminal 

run **$ python setup.py install**

and you are good to go.

Dependencies
=============

**argparse**

**keyring**

**logging**

**colorlog**

**colorama** (for windows only)


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

