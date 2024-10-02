import os
import shutil
import unittest
from tempfile import mkdtemp

from src.arxd import utils


class TestUtils(unittest.TestCase):
    def setUp(self):
        self.test_dir = mkdtemp("test_arxd_utils")
        self.old_cwd = os.getcwd()
        os.chdir(self.test_dir)

    def test_create_missing_dirs_with_prefix(self):
        prefix = "hello"
        ex_dir = "world"

        utils.create_missing_dirs(prefix, ex_dir)

        self.assertTrue(
            os.path.isdir(prefix) and
            os.path.isdir(os.path.join(prefix, ex_dir))
        )

    def test_create_missing_dirs_with_empty_prefix(self):
        prefix = ""
        ex_dir = 'hello'

        utils.create_missing_dirs(prefix, ex_dir)

        self.assertFalse(os.path.isdir(prefix))
        self.assertTrue(os.path.isdir(ex_dir))

    def tearDown(self):
        os.chdir(self.old_cwd)
        shutil.rmtree(self.test_dir)
