from setuptools import setup
from setuptools.command.install import install

class CustomInstallCommand(install):
    def run(self):
        install.run(self)
        print("Please subscribe before installing this package at https://sov.ai/home")

setup(
    name='sovai',
    version='0.1.2',
    packages=['sovai'],
    description='A brief description of your package',
    author='sov.ai',
    url='https://sov.ai/home',
    cmdclass={
        'install': CustomInstallCommand,
    },
)