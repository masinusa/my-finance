
from os.path import dirname, basename, isfile, join
import glob
import importlib
import sys
from pathlib import Path
import os

files = glob.glob(join(dirname(__file__), "*.py"))
file_names = [ basename(f)[:-3] for f in files if isfile(f) and not f.endswith('__init__.py')]


cwd = str(Path(os.path.abspath(__file__)).parents[0]).replace('\\', '/')
sys.path.append(cwd)
for category in file_names:
    modu = __import__(category, fromlist=[category])
    locals()[category] = getattr(modu, category)

del files
del file_names
del modu
del category
del dirname
del basename
del isfile
del join
del glob
del importlib
del sys
del Path
del os
del cwd