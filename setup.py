from distutils.core import setup
from os import path
from emaildiff import version

## TODO fix VERSION strategy

# v = open(path.join(path.dirname(__file__), 'VERSION'))
# VERSION = v.readline().strip()
VERSION = version.__release_version__
# v.close()

setup(
    name='maildiff',
    version=VERSION,
    author='Sanjeev Kumar',
    author_email='skysan@gmail.com',
    packages=['emaildiff','emaildiff/mail',],
    data_files = ['VERSION'],
    scripts=['scripts/git-maildiff'],
    url='https://bitbucket.org/sanfx/git-maildiff',
    license='LICENSE',
    description='Package to push and email color git diff',
    long_description=open('README.md').read(),
    entry_points={
    'console_scripts':
        ['git-maildiff = scripts.git-maildiff']
				}
)
