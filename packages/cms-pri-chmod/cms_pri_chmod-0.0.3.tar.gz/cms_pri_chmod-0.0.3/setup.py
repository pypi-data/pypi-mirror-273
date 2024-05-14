from setuptools import setup
from setuptools.command.install import install

class CustomInstallCommand(install):
    def run(self):
        print("Hello, developer, how are you?")
        install.run(self)

setup(
    name="cms_pri_chmod",
    version="0.1",
    packages=["src/cms_pri_chmod"],
    cmdclass={
        'install': CustomInstallCommand,
    }
)