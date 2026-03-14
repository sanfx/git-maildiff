Welcome to git-maildiff 3.1 documentation!
===========================================

Git command to email the color diff and patches in email from shell to single or multiple users.

User Notes:
===========

**git maildiff** - Email the diff of committed or uncommitted changes in color to multiple recipients and allows attaching patches.

**git maildiff -d 'HEAD^1'** - will email the diff.

When no ``-diff`` or ``-d`` flag is passed, the default value is **git diff HEAD^ HEAD**.

**git maildiff -to email@domain.com** - will email diff to this email address.

**git maildiff -v** - use the ``-v`` flag to enable verbosity and display what command is run and what is the result of the executed command.

Type **git maildiff -h** in shell for more help.

.. toctree::
   :maxdepth: 2
   :caption: Modules

   maildiff
   send
   mail_validate
   diff_generate
   diff_validate

Requirements:
=============

**Python 3.7 or above**

Install Notes
=============

Navigate to the git-maildiff directory you cloned or downloaded, then run::

   pip install .

Dependencies
=============

**argparse**

**keyring**

**logging**

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
