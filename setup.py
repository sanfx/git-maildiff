import ez_setup
ez_setup.use_setuptools()
try:
	from setuptools import setup
except ImportError:
	from distutils.core import setup

from distutils.core import setup
from os import path
from emaildiff import version
from pip.req import parse_requirements
from pip.download import PipSession

install_reqs = list(parse_requirements("requirements.txt", session=PipSession()))

with open('requirements.txt', 'r') as reqh:
	install_reqs = reqh.readlines()

# reqs = [str(ir.req) for ir in install_reqs]

v = open(path.join(path.dirname(__file__), 'VERSION'))
VERSION = v.readline().strip()
v.close()

setup(
	name='maildiff',
	version=VERSION,
	author='Sanjeev Kumar',
	author_email='skysan@gmail.com',
	packages=['emaildiff', 'emaildiff/mail',],
	data_files = ['VERSION'],
	scripts=['scripts/git-maildiff'],
	url='https://bitbucket.org/sanfx/git-maildiff',
	license='LICENSE',
	description='Package to email color git diff',
	long_description=open('README.md').read(),
	install_requires=install_reqs,
	entry_points={
	'console_scripts':
		['git<dash>maildiff=emaildiff.maildiff_cmd:_main']
				}
)
