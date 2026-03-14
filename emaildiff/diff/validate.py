"""
Diff validation module for git-maildiff.
"""

import logging
import re

_log = logging.getLogger(__name__)


def validate_diff(diffCmd, args, verbose, exec_cmd):
	"""Runs the diff command and checks repo state for errors or uncommitted changes.

	Args:
		diffCmd(str): git diff command to run
		args(argparse.Namespace): parsed CLI arguments
		verbose(bool): whether to log command output
		exec_cmd(callable): function to execute git commands

	Returns:
		tuple: (diffData, patches) or None if the workflow should abort.
	"""
	diffData, error = exec_cmd(diffCmd, verbose)
	if 'fatal' in error.split(":"):
		_log.error(error.capitalize())
		return None

	modifiedData, _ = exec_cmd('git status', verbose)
	if any(re.search(word, modifiedData) for word in ['modified', 'untracked']):
		_log.warning('You have uncommited changes.')
		if not args.u:
			_log.info("Use git maildiff -u to email diff of uncommited changes")
			return None

	name, _ = exec_cmd('git format-patch -%s' % args.patches)
	patches = [item for item in name.split("\n") if item]
	return diffData, patches
