from distutils.core import setup

setup(
    name='git-ipush',
    version='1.0.0',
    author='Sanjeev Kumar',
    author_email='skysan@gmail.com',
    packages=['mailer'],
    scripts=['scripts/git-ipush'],
    url='https://bitbucket.org/sanfx/git-ipush',
    license='licence',
    description='Package to push and email color git diff',
    long_description=open('README.md').read(),
    entry_points={
    'console_scripts':
        ['git-ipush = scripts.git-ipush']
				}
)
