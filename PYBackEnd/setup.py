import os
import sys
from setuptools import setup, find_packages
from setuptools.command.install import install
import argparse

from conf.db_session import create_tables


def read_requirements():
    requirements_path = os.path.join(os.path.dirname(__file__), 'requirements.txt')
    if os.path.isfile(requirements_path):
        with open(requirements_path, 'r', encoding='utf-16le') as req_file:
            requirements = req_file.read().splitlines()
            if requirements and requirements[0].startswith('\ufeff'):
                requirements[0] = requirements[0][1:]
            return requirements


class CustomInstallCommand(install):
    """Custom handler for the 'install' command."""
    def run(self):
        install.run(self)
        create_tables()


setup(
    name="PYBackEnd",
    version="0.1.0",
    packages=find_packages(),
    install_requires=read_requirements(),
    entry_points={
        "console_scripts": [
            "run_sender_side=arduino_communication.sender_side.main:main",
            "run_receiver_side=arduino_communication.receiver_side.main:main",
        ],
    },
    cmdclass={
        'install': CustomInstallCommand,
    },
)
