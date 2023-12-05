import ez_setup
ez_setup.use_setuptools()
# help on python packaging: http://python-packaging.readthedocs.io/en/latest/index.html
try:
	from setuptools import setup
except ImportError:
	from distutils.core import setup

from distutils.core import setup
from os import path

try: # for pip >= 10
	from pip._internal.req import parse_requirements
except ImportError: # for pip <= 9.0.3
	from pip.req import parse_requirements
try:
	from pip._internal.download import PipSession
except ImportError:
	from pip.download import PipSession

install_reqs = list(parse_requirements("requirements.txt", session=PipSession()))

with open('requirements.txt', 'r') as reqh:
	install_reqs = reqh.readlines()


v = open(path.join(path.dirname(__file__), 'VERSION'))
VERSION = v.readline().strip()
v.close()

setup(
	name='maildiff',
	version=VERSION,
	author='Sanjeev Kumar',
	author_email='sanjeev@outlook.in',
	packages=['emaildiff', 'emaildiff/mail',],
	data_files = ['VERSION'],
	scripts=['scripts/git-maildiff'],
	url='https://bitbucket.org/sanfx/git-maildiff',
	license='BSD',
	description='Package to email color git diff',
	long_description=(open('README.md').read()),
	long_description_content_type='text/markdown',
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
			'Programming Language :: Python :: 2',
			'Programming Language :: Python :: 2.7',
			'Programming Language :: Python :: 3',
			'Programming Language :: Python :: 3.3',
			'Programming Language :: Python :: 3.4',
			'Topic :: Software Development',
			'Topic :: Software Development :: Version Control',
			'Topic :: Utilities',
			],
	   platforms=['Unix', 'Darwin', 'Windows']
)
