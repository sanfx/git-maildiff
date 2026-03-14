"""
Email validation module for git-maildiff.
"""

import argparse

from dataclasses import dataclass
import re


@dataclass(frozen=True)
class EmailAddress:
    value: str

    def __post_init__(self):
        if not re.match(r'^([^@\s]+)@((?:[-a-z0-9]+\.)+[a-z]{2,})$', self.value, re.IGNORECASE):
            raise ValueError("Invalid email address")


def validate_address(address: str) -> EmailAddress:
	"""If address looks like a valid e-mail address, return it. Otherwise
	raise ArgumentTypeError.

	Args:
		address(string): email address to validate
	"""
	try:
		return EmailAddress(address)
	except ValueError:
		raise argparse.ArgumentTypeError('Invalid e-mail address: %s' % address)
