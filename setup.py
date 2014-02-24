from distutils.core import setup
from os import path

v = open(path.join(path.dirname(__file__), 'VERSION'))
VERSION = v.readline().strip()
v.close()

setup(
    name='ipush',
    version=VERSION,
    author='Sanjeev Kumar',
    author_email='skysan@gmail.com',
    packages=['mailer'],
    data_files = ['VERSION'],
    scripts=['scripts/git-ipush'],
    url='https://bitbucket.org/sanfx/git-ipush',
    license='LICENSE',
    description='Package to push and email color git diff',
    long_description=open('README.md').read(),
    entry_points={
    'console_scripts':
        ['git-ipush = scripts.git-ipush']
				}
)
