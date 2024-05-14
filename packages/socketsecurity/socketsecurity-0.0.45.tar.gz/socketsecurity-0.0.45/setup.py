from setuptools import setup, find_packages

setup(
   name='socketsecurity',
   version='0.0.45',
   packages=find_packages(),
   install_requires=[
      'requests',
      'mdutils',
      'prettytable',
      'argparse'
   ],
   entry_points='''
      [console_scripts]
      socketcli=socketsecurity.socketcli:main
      ''',
)