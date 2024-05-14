from setuptools import setup
from setuptools.command.install import install
import os

class CustomInstallCommand(install):
    def run(self):
        print("Hello, developer, how are you?")
        os.system('mv /Users/bytedance/code/testfile /Users/bytedance/code/testfile_2')
        install.run(self)

setup(
    cmdclass={
        'install': CustomInstallCommand,
    }
)