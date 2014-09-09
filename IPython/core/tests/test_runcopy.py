""" Testing %run -C foo.py

This should be an extension of %autoreload when completed.
"""

from __future__ import absolute_import # not sure why I need this
#-----------------------------------------------------------------
import functools
import os
from os.path import join as pjoin
import random
import sys
import tempfile
import textwrap
import unittest
import time

import nose.tools as nt
from nose import SkipTest

from IPython.testing import decorators as dec
from IPython.testing import tools as tt
from IPython.utils import py3compat
from IPython.utils.io import capture_output
from IPython.utils.tempdir import TemporaryDirectory
from IPython.core import debugger
from IPython.extensions.autoreload import ModuleReloader
#--------------------------------------------------------------------
# Test functions begin
#--------------------------------------------------------------------

# Modeled after TestMagicRunPass() in test_run.py
class TestMagicRunCopyPass(tt.TempFileMixin):

    def setUp(self):
        """ Make a valid python temp file. """
        self.mktmp('pass\n')
        # reloader module
        self._reloader = ModuleReloader()

    def tearDown(self):
        """ Make sure reloader module is off """
        # shut down autoreload
        self._reloader.enabled = False

    def run_tmpfile(self):
        _ip = get_ipython()
        # watch out for windows here, check test_run.py
        _ip.magic('run %s' % self.fname) # not understanding this bit

    def write_file(self, filename, content):
        """
        Write a file, and force a timestamp difference of at least one second

        Notes
        -----
        Python's .pyc files record the timestamp of their compilation
        with a time resolution of one second.

        Therefore, we need to force a timestamp difference between .py
        and .pyc, without having the .py file be timestamped in the
        future, and without changing the timestamp of the .pyc file
        (because that is stored in the file).  The only reliable way
        to achieve this seems to be to sleep.
        """

        # Sleep one second + eps
        time.sleep(1.05)

        # Write
        f = open(filename, 'w')
        try:
            f.write(content)
        finally:
            f.close()

    def new_module(self, code):
        mod_name, mod_fn = self.get_module()
        f = open(mod_fn, 'w')
        try:
            f.write(code)
        finally:
            f.close()
        return mod_name, mod_fn

    def test_run_file(self):
        """ Test a file without dependencies """
        self.mktmp("avar = 1\n"
                   "def afunc():\n"
                   "  return avar\n")
        empty = tt.TempFileMixin()
        empty.mktmp("")

        _ip.magic('run %s' % self.fname)
        nt.assert_equal(_ip.user_ns['afunc'](), 1)

    def test_run_deep_copy_without_raising_error(self):
        """ Test deep copy flag to see if it throws an error """
        self.mktmp("avar = 1\n"
                   "def afunc():\n"
                   "  return avar\n")
        empty = tt.TempFileMixin()
        empty.mktmp("")

        _ip.magic('run -C %s' % self.fname)
        nt.assert_equal(_ip.user_ns['afunc'](), 1)

    def test_module_change_with_no_dependency(self):
        """ Autoreload module without dependencies """
        # create new module
        self.write_file('mod_fn.py', """
x = 6

def afunc():
    return x
""")
        _ip.magic('run -C %s' % 'mod_fn.py')
        nt.assert_equal(_ip.user_ns['afunc'](), 6)
        # change new module
        self.write_file('mod_fn.py', """
x = 7

def afunc():
    return x
""")
        _ip.magic('run -C %s' % 'mod_fn.py')
        nt.assert_equal(_ip.user_ns['afunc'](), 7)

    def test_module_change_with_dependency(self):
        """ Autoreload module with dependencies """

        # create dependency
        self.write_file('my_dependency.py', """
var = 6
""")
        # create module
        self.write_file('mod_fn.py', """
from my_dependency import var

x = var

def afunc():
    return x
""")
        # test module (mod_fn)
        nt.assert_equal(_ip.user_ns['afunc'](), 6) # take a closer
        # look at user_ns
        
        
        


        
