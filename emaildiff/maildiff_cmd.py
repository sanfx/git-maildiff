
import argparse
import getpass
import keyring
import logging
import re
import subprocess
import sys
import tempfile

from colorlog import ColoredFormatter
from emaildiff.mail import send as send
from os import path


EPILOG = """	Utility to email the color diff and patches in email from shell.

	Examples:

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

def __validate_address(address):
	"""	If address looks like a valid e-mail address, return it. Otherwise
		raise ArgumentTypeError.

		Args:
			address(string): email address to send to
		.. document private functions
		.. automethod:: _evaporate
	"""
	if re.match('^([^@\s]+)@((?:[-a-z0-9]+\.)+[a-z]{2,})$', address):
		return address
	raise argparse.ArgumentTypeError('Invalid e-mail address: %s' % address)

def main():
	"""	
		This function parses the argumets passed from commandline.
		creates a logger and inject it to function.

	"""
	appName = path.basename(sys.argv[0]).split('-')[-1]
	parser = argparse.ArgumentParser(prog=appName,
		description=__doc__, epilog=EPILOG% tuple([appName] * EPILOG.count('%s')), 
		formatter_class=argparse.RawDescriptionHelpFormatter)
	parser.add_argument('-v', '--verbose', action='store_true', 
		help='if enabled will spit every command and its resulting data.')
	parser.add_argument('-c', '--compose', action='store_true', 
		help='compose message in default git editor to be sent prefixed with diff')
	parser.add_argument('-to', type=__validate_address, metavar='Email', nargs='+',
		help='enter a valid email you want to send to.')
	parser.add_argument('-p', '--patches', type=int, default=0, metavar='*.patch files',
		help='total number of pathces of last commits to email')
	parser.add_argument('-d', '--diff', required=False, default='HEAD^ HEAD',
		metavar='HEAD^ HEAD', help='if present pass arguments to it as you \
		will do to git diff in inverted commas')
	parser.add_argument('-u', required=False, action='store_true', help='pass argument \
		to email diff of uncommited changes.')

	args = parser.parse_args()

	logger = logging.getLogger(appName)
	handler = logging.StreamHandler()

	DATE_FORMAT = '%H:%M'
	formatter = ColoredFormatter(
		"%(log_color)s%(name)s %(asctime)-2s%(reset)s %(message_log_color)s%(message)s",
		secondary_log_colors={
				'message': {
						'ERROR': 'red',
						'CRITICAL': 'red',
						'INFO': 'cyan',
						'WARNING': 'yellow'
	 
						}
				},
		datefmt=DATE_FORMAT,
		)
	handler.setFormatter(formatter)
	logger.addHandler(handler)
	logger.setLevel(logging.DEBUG)

	__pre_Check(args, logger)

def __update_config(log, key, value):
	"""	Function to update the global config git file.
		:param key(string): key of the git command
		:param value(string): value of the key

		.. document private functions
		.. automethod:: _evaporate
	"""
	_exec_git_command(log, 'git config --global %s %s' % (key, value))


def _guarantee_bool(function):
	"""	A decorator that guarantees a true/false response.
	"""
	def wrapper(*args, **kargs):
		try:
			return bool(function(*args, **kargs))
		except:
			return False
	return wrapper

def config_db(log):
	"""	
		Reads git global config file

		:param log: logger to log information
		:type log: logging.Logger


		:returns config: git config settings
		:type config: dict
	"""
	# Read git config file
	configFile, _ = _exec_git_command(log, 'git config --list')
	config = {}
	for line in (_line for _line in configFile.split("\n") if _line):
		config[line.split("=")[0]] = line.split("=")[-1]

	return config

def launchEditor(editor):
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

def _setUp_maildiff(log, config):
	"""	this function prompts user to enter email settings
		for this git maildiff command to store in .gitconfig
		while password is stored in os keychain.

		Args:
			config(dict): existing config from .gitconfig
	"""
	# check if data in  global config
	if not config.has_key('maildiff.mailfrom'):
		log.info("\x1b[32mFirst time mail setup.\x1b[m")
		userEmail = config['user.email']
		log.warning("Do you want to use your git email '%s' to send diffs or any other email address ?", userEmail)
		ret = raw_input('[YES]')
		if ret.lower() in ['', 'yes', 'y']:
			ret = userEmail
			__update_config(log, 'maildiff.mailfrom', ret)
		else:
			ret = __validate_address(ret)
			_exec_git_command(log, 'git maildiff.mailfrom %s' % ret)
		__update_config(log, 'maildiff.mailfrom', ret)
		log.info("Please enter password for the email: %s" , ret)
		emailPwd = getpass.getpass(prompt=" Password: ")
		keyring.set_password('maildiff', ret, emailPwd)
	# enter SMTP details for sending emails
	if not config.has_key('maildiff.smtpserver'):
		log.info("Add SMTP details for '%s'.", ret)
		smtpServer = raw_input(" SMTP Server: ")
		__update_config(log, 'maildiff.smtpserver', smtpServer)
		smtpServerPort = raw_input(" SMTP Server Port: ")
		__update_config(log, 'maildiff.smtpserverport', smtpServerPort)
		smtpEncryption = raw_input(" Server Encryption: ")
		__update_config(log, 'maildiff.smtpencryption', smtpEncryption)
	return True

def __pre_Check(args, log):
	"""	This function do a pre-check of the repository state
		and default value to variables from git config

		Args:
			args(argparse.Namespace): data from git config
	"""
	config = config_db(log)

	editor = config['core.editor'] if config.has_key('core.editor') else 'vi'

	VERBOSE = args.verbose

	diffCmd = 'git diff' if args.u  else 'git diff %s' % args.diff

	branchName, _ = _exec_git_command(log, 'git rev-parse --abbrev-ref HEAD')

	if not branchName:
		return

	# stripping newline character which got appended when pulling branch name
	branchName = branchName.split("\n")[0]
	commitComment, _ = _exec_git_command(log, 'git log -1 --pretty=%B')
	subject = "%s: %s" % (branchName, commitComment)

	# check for fatal error when executing git command
	diffData, error = _exec_git_command(log, diffCmd, VERBOSE)
	if 'fatal' not in error.split(":"):
		modifiedData, error = _exec_git_command(log, 'git status', VERBOSE)
		if any([re.search(word, modifiedData) for word in ['modified', 'untracked']]):
			log.warning('You have uncommited changes.')
			if not args.u:
				log.info("Use git maildiff -u to email diff of uncommited changes")
				return

		name, _ = _exec_git_command(log, 'git format-patch -%s' % args.patches)
		patches = [item for item in name.split("\n") if item]
		if diffData:
			message = ""
			if args.compose:
				message = launchEditor(editor)

			htmlDiff = get_Html(diffData.split("\n"))
			remotePath, _ = _exec_git_command(log, 'git config --get remote.origin.url')
			message = "%s<br>git clone %s<br><br>%s" % (message, remotePath, htmlDiff)

			updateComplete = _setUp_maildiff(log, config)
			if updateComplete:
				# update the user email info by reading config again
				config = config_db(log)

			mailtos = args.to if args.to else [raw_input(
				"Who do you want to send to ?")]
			for mailto in mailtos:
				log.info("Trying to send to %s", mailto)
				__email_diff(log, subject, mailto, message, patches)
	else:
		log.error(error.capitalize())

def get_Html(linesfromDiff, sideBySide=False):
	"""	Converts plain git diff text to html color code

		:param linesfromDiff: diff between commits in simple text
		:type linesfromDiff: str

		:param sideBySide: whether diff to be displayed side
						by side or not
		:type sideBySide: bool

		:Returns lines: colored html diff text
		:type lines: str
	"""
	openTag = """<span style='font-size:1.0em; color: """
	openTagEnd = ";font-family: courier, arial, helvetica, sans-serif;'>"
	nbsp = '&nbsp;&nbsp;&nbsp;&nbsp;'


	if sideBySide:
		# TODO
		# build data of side by side html lines with color formating
		pass
	else:
		return _traditional_diff(linesfromDiff, openTag, openTagEnd, nbsp)

def _traditional_diff(linesfromDiff, openTag, openTagEnd, nbsp):
	lines = []	
	line_num = 0

	def updateLine(line_num, color, line):
		tabs = line.count('\t')
		lines.append("%s:%s#%s%s%s%s</span><br>" % 
		((repr(line_num), openTag, color, openTagEnd, nbsp*tabs, line)))
		return lines

	for line in linesfromDiff:
		if (line.startswith('diff ') or
				line.startswith('index ') or
				line.startswith('--- ')):
			color = "10EDF5"
			updateLine(line_num, color, line)
			continue

		if line.startswith('-'):
			color = "ff0000"
			updateLine(line_num, color, line)
			continue


		if line.startswith('+++ '):
			color = "07CB14"
			updateLine(line_num, color, line)
			continue

		if line.startswith('@@ '):
			_, old_nr, new_nr, _ = line.split(' ', 3)
			line_num = int(new_nr.split(',')[0])
			color = "5753BE"
			updateLine(line_num, color, line)
			continue

		if line.startswith('+'):
			color = "007900"
			updateLine(line_num, color, line)

		if line.startswith('+') or line.startswith(' '):
			line_num += 1

	return ''.join(lines)



def _exec_git_command(log, command, verbose=False):
	"""	Function used to get data out of git commads
		and errors in case of failure.

		Args:
			command(string): string of a git command
			verbose(bool): whether to display every command
			and its resulting data.
		Returns:
			(tuple): string of Data and error if present
	"""
	# converts multiple spaces to single space
	command = re.sub(' +',' ',command)
	pr = subprocess.Popen(command, shell=True,
		stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	msg = pr.stdout.read()
	err = pr.stderr.read()
	if err:
		log.error(err)
		if 'Could not resolve host' in err:
			return
	if verbose and msg:
		log.info("Executing '%s' %s", command, msg)
	return msg, err


def __email_diff(log, subject, emailTo, htmlDiff, attachment):
	""" This function send color diff via email

		Args:
			subject(string): name of the branch with commit message
			htmlDiff(string): html formatted string
			attachment(list): list of file names to be attached
	"""
	# add tool signature
	htmlDiff = """%s<br><br>
	Sent using git maildiff<br>
	git clone https://sanfx@bitbucket.org/sanfx/git-maildiff.git""" % htmlDiff
	emailInfo = config_db(log)
	pwd = str(keyring.get_password('maildiff', emailInfo['maildiff.mailfrom']))
	mail = send.EMail(
						mailfrom=emailInfo['maildiff.mailfrom'], 
						server=emailInfo['maildiff.smtpserver'], 
						usrname=emailInfo['maildiff.mailfrom'].split('@')[0],
						password=pwd,
						logger=log,
						debug=False
					)
	try:
		emailTo = __validate_address(emailTo)
	except argparse.ArgumentTypeError as er:
		log.error("%s. Message not sent.", er)
	else:
		isSent = mail.sendMessage(subject, htmlDiff, attachment, emailTo)
		if isSent:
			msg = ' Diff of branch, %s sent to email: %s .' % (subject, emailTo)
			log.info(msg)


