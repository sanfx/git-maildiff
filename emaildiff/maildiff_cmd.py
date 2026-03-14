
"""
Main command-line interface for git-maildiff.

This module provides the main entry point and command-line interface for the
git-maildiff tool. It handles parsing arguments, configuring the environment,
generating HTML diffs, and sending emails.
"""

import argparse
import getpass
import keyring
import logging
import re
import subprocess
import sys
import tempfile

from emaildiff.diff import generate as generate
from emaildiff.diff import validate as diff_validate
from emaildiff.mail import send as send
from emaildiff.mail import validate as mail_validate
from pathlib import Path


EPILOG = """	Utility to email the color diff and patches in email from shell.

	Examples:

	 \x1b[36mgit %s --subject <your subject here >   --compose\x1b[m
		compose message in default git editor to be sent prefixed with diff of changes.

	 \x1b[36mgit %s --compose\x1b[m
		compose message in default git editor to be sent prefixed with diff of changes.

	 \x1b[36mgit %s -u -to skysam@gmail.cam asksam@live.com\x1b[m
		if you have uncommited chanegs you can use this flag to send diff of uncommited
		changes compared to the last commit head. you can simultaneusly send to multiple
		recipients as in this case separated by space between skysam@gmail.cam asksam@live.com

	 \x1b[36mgit %s -to --compse\x1b[m
		email address to whom you want to send to, along with --compose flag to write
		content of email message.

	 \x1b[36mgit %s --compose --patches 4 -to skysam@gmail.cam\x1b[m
		first flag will cause text editor to open for you to compose message and then
		--patches will flag will take 4 number of last commit diffs to be attached and
		emailed to skysan@gmail.cam

	 \x1b[36mgit %s -d 'HEAD^ HEAD' -to skysam@gmail.cam\x1b[m
		if present pass arguments to it as you will do to git diff in inverted commas.
		"""

_log = logging.getLogger(__name__)


def main():
	"""
		This function parses the argumets passed from commandline.
		creates a logger and inject it to function.

	"""
	appName = Path(sys.argv[0]).name.split('-')[-1]
	parser = argparse.ArgumentParser(prog=appName,
		description=__doc__, epilog=EPILOG% tuple([appName] * EPILOG.count('%s')),
		formatter_class=argparse.RawDescriptionHelpFormatter)
	parser.add_argument('-v', '--verbose', action='store_true',
		help='if enabled will spit every command and its resulting data.')
	parser.add_argument("-s", "--subject", dest="subject", type=str, default="")
	parser.add_argument('-c', '--compose', action='store_true',
		help='compose message in default git editor to be sent prefixed with diff')
	parser.add_argument('-to', type=lambda a: mail_validate.validate_address(a).value, metavar='Email', nargs='+',
		help='A valid email you want to send to.')
	parser.add_argument('-p', '--patches', type=int, default=0, metavar='*.patch files',
		help='total number of pathces of last commits to email')
	parser.add_argument('-pwd', '--password', dest="password", action='store_true', default=False,
		help="Prompt for user's sender email password rather than using from keychain.")
	parser.add_argument('-d', '--diff', required=False, default='HEAD^ HEAD',
		metavar='HEAD^ HEAD', help='if present pass arguments to it as you \
		will do to git diff in inverted commas')
	parser.add_argument('-u', required=False, action='store_true', help='pass argument \
		to email diff of uncommited changes.')

	args = parser.parse_args()

	handler = logging.StreamHandler()
	DATE_FORMAT = '%H:%M'
	formatter = logging.Formatter(
		"%(name)s %(asctime)-2s %(message)s",
		datefmt=DATE_FORMAT,
		)
	handler.setFormatter(formatter)
	_log.addHandler(handler)
	_log.setLevel(logging.DEBUG)

	__pre_Check(args)

def __update_config(key, value):
	"""	Function to update the global config git file.
		:param key(string): key of the git command
		:param value(string): value of the key

		.. document private functions
		.. automethod:: _evaporate
	"""
	_exec_git_command('git config --global %s %s' % (key, value))


def config_db():
	"""
		Reads git global config file

		:returns config: git config settings
		:type config: dict
	"""
	configFile, _ = _exec_git_command('git config --list')
	config = {}
	for line in (_line for _line in configFile.split("\n") if _line):
		config[line.split("=")[0]] = line.split("=")[-1]

	return config

def launchEditor(editor: str):
	"""
		This function launches the default git editor
		set in git config for user to compose message
		to be sent along with git diff.

		:param editor: name or path of editor
		:type editor: str

		:returns msg: html formatted message
		:type msg: str
	"""

	with tempfile.NamedTemporaryFile(delete=False) as f:
		f.close()
		if "-" in editor and editor not in ['vi', 'vim', 'nano', 'emacs']:
			editor = re.sub(" -.*", "", editor)
			openToEdit = [editor, f.name]
			if re.search('Sublime', editor):
				openToEdit = [editor, '-w', f.name]
		else:
			openToEdit = [editor, f.name]

		if subprocess.call(openToEdit) != 0:
			raise IOError("%s exited with code." % (editor.split(" ")[0]))
		msg = ''
		with open(f.name) as temp_file:
			temp_file.seek(0)
			for line in temp_file.readlines():
				msg += line

			return "".join(msg).replace("\n", "<br>")

def _setUp_maildiff(config):
	"""	Prompts the user to enter email settings
		for this git maildiff command to store in .gitconfig
		while password is stored in os keychain.

		Args:
			config(dict): existing config from .gitconfig
	"""
	if 'maildiff.mailfrom' not in config:
		_log.info("\x1b[32mFirst time email setup.\x1b[m")
		sender_email = config['user.email']
		ret = input(f"Do you want to use your git email '{sender_email}' to send diffs or any other email address ?\n\t[YES]")
		if ret.lower() in ['yes', 'y']:
			ret = sender_email
			__update_config('maildiff.mailfrom', ret)
		else:
			ret = mail_validate.validate_address(ret).value
			_exec_git_command('git maildiff.mailfrom %s' % ret)
		__update_config('maildiff.mailfrom', ret)
		_log.info("Please enter password for the email: %s", ret)
		emailPwd = getpass.getpass(prompt=" Password: ")
		keyring.set_password('maildiff', ret, emailPwd)
	if 'maildiff.smtpserver' not in config:
		_log.info("Add SMTP details for '%s'.", ret)
		smtpServer = input(" SMTP Server: ")
		__update_config('maildiff.smtpserver', smtpServer)
		smtpServerPort = input(" SMTP Server Port: ")
		__update_config('maildiff.smtpserverport', smtpServerPort)
		smtpEncryption = input(" Server Encryption: ")
		__update_config('maildiff.smtpencryption', smtpEncryption)
	return True


def __get_context(args):
	"""Loads git config and derives editor, diff command, and email subject.

	Returns:
		tuple: (config, editor, diffCmd, subject) or None if not in a git repo.
	"""
	config = config_db()
	editor = config.get('core.editor', 'vi')
	diffCmd = 'git diff' if args.u else 'git diff %s' % args.diff

	branchName, _ = _exec_git_command('git rev-parse --abbrev-ref HEAD')
	if not branchName:
		return None

	branchName = branchName.split("\n")[0]
	commitComment, _ = _exec_git_command('git log -1 --pretty=%B')
	subject = args.subject or "%s: %s" % (branchName, commitComment)

	return config, editor, diffCmd, subject


def __build_message(args, editor, diffData):
	"""Composes and returns the HTML email body from the diff data.

	Returns:
		str: HTML-formatted email message.
	"""
	message = ""
	if args.compose:
		message = launchEditor(editor)

	htmlDiff = generate.get_Html(diffData.split("\n"))
	remotePath, _ = _exec_git_command('git config --get remote.origin.url')
	return "%s<br>git clone %s<br><br>%s" % (message, remotePath, htmlDiff)


def __send_emails(args, config, subject, message, patches):
	"""Ensures maildiff is configured then sends the email to each recipient."""
	updateComplete = _setUp_maildiff(config)
	if updateComplete:
		config = config_db()

	mailtos = args.to if args.to else [input("Who do you want to send to?")]
	for mailto in mailtos:
		_log.info("Trying to send to %s", mailto)
		pas = getpass.getpass(prompt=f" Password for {config['maildiff.mailfrom']}: ") if args.password else None
		__email_diff(subject, mailto, message, patches, password=pas)


def __pre_Check(args):
	"""Pre-checks repository state and orchestrates the diff email workflow."""
	context = __get_context(args)
	if not context:
		return

	config, editor, diffCmd, subject = context

	result = diff_validate.validate_diff(diffCmd, args, args.verbose, _exec_git_command)
	if not result:
		return

	diffData, patches = result
	if not diffData:
		return

	message = __build_message(args, editor, diffData)
	__send_emails(args, config, subject, message, patches)

def _exec_git_command(command, verbose=False):
	"""	Function used to get data out of git commads
		and errors in case of failure.

		Args:
			command(string): string of a git command
			verbose(bool): whether to display every command
			and its resulting data.
		Returns:
			(tuple): string of Data and error if present
	"""
	command = re.sub(' +',' ',command)
	pr = subprocess.Popen(command, shell=True,
		stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
	msg = pr.stdout.read()
	err = pr.stderr.read()
	if err:
		_log.error(err)
		if 'Could not resolve host' in err:
			return
	if verbose and msg:
		_log.info("Executing '%s' %s", command, msg)
	return msg, err


def __email_diff(subject, emailTo, htmlDiff, attachment, password=None):
	""" This function send color diff via email

		Args:
			subject(string): name of the branch with commit message
			htmlDiff(string): html formatted string
			attachment(list): list of file names to be attached
	"""
	htmlDiff = """%s<br><br>
	Sent using git maildiff<br>
	git clone https://github.com/sanfx/git-maildiff.git""" % htmlDiff
	emailInfo = config_db()
	pwd = password or str(keyring.get_password('maildiff', emailInfo['maildiff.mailfrom']))
	mail = send.EMail(
						mailfrom=emailInfo['maildiff.mailfrom'],
						server=emailInfo['maildiff.smtpserver'],
						usrname=emailInfo['maildiff.mailfrom'],
						password=pwd,
						logger=_log,
						debug=False
					)
	try:
		emailTo = mail_validate.validate_address(emailTo).value
	except argparse.ArgumentTypeError as er:
		_log.error("%s. Message not sent.", er)
	else:
		isSent = mail.sendMessage(subject, htmlDiff, attachment, emailTo)
		if isSent:
			msg = ' Diff of branch, %s sent to email: %s .' % (subject, emailTo)
			_log.info(msg)
