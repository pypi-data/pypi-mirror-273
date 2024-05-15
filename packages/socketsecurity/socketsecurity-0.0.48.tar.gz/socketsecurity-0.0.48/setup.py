from setuptools import setup, find_packages

setup(
   name='socketsecurity',
   version='0.0.48',
   python_requires='>3.10.1',
   packages=find_packages(),
   install_requires=[
      'requests',
      'mdutils',
      'prettytable',
      'argparse'
   ],
   entry_points='''
      [console_scripts]
      socketcli=socketsecurity.socketcli:cli
      ''',
)