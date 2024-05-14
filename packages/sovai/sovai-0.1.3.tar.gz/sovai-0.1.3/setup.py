from setuptools import setup
from setuptools.command.install import install

class CustomInstallCommand(install):
    def run(self):
        install.run(self)
        print("Please subscribe before installing this package at https://sov.ai/home")

setup(
    name='sovai',
    version='0.1.3',
    packages=['sovai'],
    description='Please first subscribe at https://sov.ai/home before using this package.',
    author='sov.ai',
    url='https://sov.ai/home',
    cmdclass={
        'install': CustomInstallCommand,
    },
    post_install_message='''
    Thank you for installing sovai!
    Please subscribe at https://sov.ai/home before using this package.
    '''
)