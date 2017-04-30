# -*- coding: utf-8 -*-
"""
Created on 04/30/17 20:36:42

setup.py for koala

@author: eqs
"""

import sys
import os
import os.path
import PyQt5
from cx_Freeze import setup, Executable

base = None

if sys.platform == "win32":
    base = "Win32GUI"

build_options = dict(
    packages = [], 
    excludes = [], 
    includes = [], 
    include_files = ['koala_config.py', 'startimage.png']
)

# Setting Environment Variables
import os, os.path, PyQt5
from PyQt5.QtWidgets import QApplication
plugins = os.path.join(os.path.dirname(PyQt5.__file__), 
                       '..', '..', '..', 'Library', 'plugins')
QApplication.addLibraryPath(plugins)


setup(name="koala", 
      version="0.1", 
      description="converter", 
      options=dict(build_exe=build_options), 
      executables=[Executable("main.py", base=base)])

