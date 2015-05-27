#run using "python setup.py py2exe" on a windows machine with py2exe installed
from distutils.core import setup
import py2exe

setup(console=['getNgrams.py'])
