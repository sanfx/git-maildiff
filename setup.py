"""
Setup module for git-maildiff.

This module configures the package installation and metadata.
"""

from pathlib import Path
from setuptools import setup

def read(fname):
    return Path(__file__).parent.joinpath(fname).read_text()

reqs_path = Path(__file__).parent.joinpath('requirements.txt')

with open(reqs_path, 'r') as reqh:
	install_reqs = reqh.readlines()

v = open(Path(__file__).parent.joinpath('VERSION'))
VERSION = v.readline().strip()
v.close()

setup(
	name='maildiff',
	version=VERSION,
	author='Sanjeev Kumar',
	author_email='sansupercool@duck.com',
	packages=['emaildiff', 'emaildiff/mail',],
	data_files = ['VERSION'],
	scripts=['scripts/git-maildiff'],
	url='https://github.com/sanfx/git-maildiff',
	license='BSD',
	description='Package to email color git diff',
	long_description=(open('README.md').read()),
	long_description_content_type='text/markdown',
	setup_requires=["setuptools>=58.0.4"],
	install_requires=install_reqs,
	entry_points={
	'console_scripts':
		['git-maildiff=emaildiff.maildiff_cmd:main']
				},
	 classifiers=[
			'Development Status :: 5 - Production/Stable',
			'Environment :: Console',
			'Intended Audience :: Developers',
			'Intended Audience :: System Administrators',
			'License :: OSI Approved :: BSD License',
			'Operating System :: Unix',
			'Programming Language :: Python',
			'Programming Language :: Python :: 3',
			'Programming Language :: Python :: 3.7',
			'Programming Language :: Python :: 3.8',
			'Programming Language :: Python :: 3.9',
			'Programming Language :: Python :: 3.10',
			'Programming Language :: Python :: 3.11',
			'Programming Language :: Python :: 3.12',
			'Programming Language :: Python :: 3.13',
			'Topic :: Software Development',
			'Topic :: Software Development :: Version Control',
			'Topic :: Utilities',
			],
	   platforms=['Unix', 'Darwin', 'Windows']
)
