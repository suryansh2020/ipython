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

import nose.tools as nt
from nose import SkipTest

from IPython.testing import decorators as dec
from IPython.testing import tools as tt
from IPython.utils import py3compat
from IPython.utils.io import capture_output
from IPython.utils.tempdir import TemporaryDirectory
from IPython.core import debugger

#--------------------------------------------------------------------
# Test functions begin
#--------------------------------------------------------------------

# Modeled after TestMagicRunPass() in test_run.py
class TestMagicRunCopyPass(tt.TempFileMixin):

    def setUp(self):
        """ Make a valid python temp file. """
        self.mktmp('pass\n')

    def run_tmpfile(self):
        _ip = get_ipython()
        # watch out for windows here, check test_run.py
        _ip.magic('run %s' % self.fname) # not understanding this bit

    def run_tmpfile_p(self):
        _ip = get_ipython()
        # watch out for windows
        _ip.magic('run -p %s' % self.fname)

        
