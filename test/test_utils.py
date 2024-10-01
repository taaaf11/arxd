import os
import shutil
import unittest
from tempfile import mkdtemp

from arxd import utils


class TestUtils(unittest.TestCase):
    def setUp(self):
        self.test_dir = mkdtemp("test_arxd_utils")
        self.old_cwd = os.getcwd()
        os.chdir(self.test_dir)

    def test_create_missing_dirs(self):
        prefix = "hello"
        ex_dir = "world"

        isdir = os.path.isdir

        utils.create_missing_dirs(prefix, ex_dir)

        self.assertTrue(
            isdir(prefix) and
            isdir(os.path.join(prefix, ex_dir))
        )

    def tearDown(self):
        shutil.rmtree(self.test_dir)
        os.chdir(self.old_cwd)
