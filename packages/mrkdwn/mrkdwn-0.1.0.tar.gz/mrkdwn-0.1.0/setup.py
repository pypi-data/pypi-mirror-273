from setuptools import setup, find_packages
from setuptools.command.install import install
import os
import platform
import subprocess

class PostInstallCommand(install):
    """Post-installation for installation mode."""
    def run(self):
        install.run(self)
        if platform.system() == 'Windows':
            script = os.path.join(os.path.dirname(__file__), 'scripts', 'installer.bat')
            subprocess.run(['cmd', '/c', script])
        else:
            script = os.path.join(os.path.dirname(__file__), 'scripts', 'installer.sh')
            subprocess.run(['sh', script])

setup(
    name='mrkdwn',
    version='0.1.0',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'markdown=mrkdwn.main:main',
        ],
    },
    install_requires=[],
    include_package_data=True,
    scripts=['scripts/installer.sh', 'scripts/installer.bat'],
    author='Joel Yisrael Biton',
    author_email='joel@sss.bot',
    description='A tool to generate markdown from directory contents',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/schizoprada/mrkdwn',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.0',
    cmdclass={
        'install': PostInstallCommand,
    },
)
