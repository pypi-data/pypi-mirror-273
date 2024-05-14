from setuptools import setup
from setuptools.command.install import install

class CustomInstallCommand(install):
    def run(self):
        print("Please subscribe before installing this package at https://sov.ai/home!")
        install.run(self)

setup(
    name='sovai',
    version='0.1.1',
    packages=['sovai'],
    description='A brief description of your package',
    author='sov.ai',
    url='https://sov.ai/home',
    cmdclass={
        'install': CustomInstallCommand,
    },
)