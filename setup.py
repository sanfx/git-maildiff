import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

reqs_path = os.path.join(os.path.dirname(__file__), 'requirements.txt')

with open(reqs_path, 'r') as reqh:
	install_reqs = reqh.readlines()

v = open(os.path.join(os.path.dirname(__file__), 'VERSION'))
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
			'Programming Language :: Python :: 3.3',
			'Programming Language :: Python :: 3.4',
			'Programming Language :: Python :: 3.7',
			'Topic :: Software Development',
			'Topic :: Software Development :: Version Control',
			'Topic :: Utilities',
			],
	   platforms=['Unix', 'Darwin', 'Windows']
)
