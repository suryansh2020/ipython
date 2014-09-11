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
from IPython.extensions.autoreload.tests import Fixture
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

    def test_run_file(self):
        """ Test a file without dependencies """
        self.mktmp("avar = 1\n"
                   "def afunc():\n"
                   "  return avar\n")

        _ip.magic('run %s' % self.fname)
        nt.assert_equal(_ip.user_ns['afunc'](), 1)

    def test_run_deep_copy_without_raising_error(self):
        """ Test deep copy flag to see if it throws an error """
        self.mktmp("avar = 1\n"
                   "def afunc():\n"
                   "  return avar\n")

        _ip.magic('run -C %s' % self.fname)
        nt.assert_equal(_ip.user_ns['afunc'](), 1)

    def test_module_change_with_no_dependency(self):
        """ Autoreload module without dependencies """
        self.mktmp("avar = 6\n"
                   "def afunc():\n"
                   "  return avar\n")
       
        _ip.magic('run -C %s' % self.fname)
        nt.assert_equal(_ip.user_ns['afunc'](), 6)

        # now change contents of temp file
        self.mktmp("avar = 7\n"
                   "def afunc():\n"
                   "  return avar\n")
        _ip.magic('run -C %s' % self.fname)
        nt.assert_equal(_ip.user_ns['afunc'](), 7)

        # third time is the charm
        self.mktmp("avar = 42\n"
                   "def afunc():\n"
                   "  return avar\n")
        _ip.magic('run -C %s' % self.fname)
        nt.assert_equal(_ip.user_ns['afunc'](), 42)

class TestRunCopyDependencies(Fixture):
    """ Trying to get deep copy working when file has dependencies """

    def test_smoketest(self):
        """ Tests for test config components """

        dep_name, dep_fn = self.new_module("""
var = 6
""")
        mod_name, mod_fn = self.new_module("""
from %s import var\n
\n
variable = var\n
\n
def afunc():\n
    return variable\n
        """ % dep_name)

        #
        # Test module contents
        #
        mod = sys.modules[mod_name]
        dep = sys.modules[dep_name]

        def check_module_contents():
            nt.assert_equal(mod.var, 6)
            nt.assert_equal(dep.variable, 6)

        check_module_contents()

        #
        # Load module with a dependency
        #
        
        

    def test_module_change_with_dependency(self):
        """ Autoreload module with dependencies """
        # not going to be able to use temp files here.

        
        pass
        
        
        


        
