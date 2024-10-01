import itertools
import os
import shutil
import tempfile
import unittest
from string import ascii_lowercase
from tempfile import mkdtemp

from arxd import arxd


class TestArxd(unittest.TestCase):
    def setUp(self):
        def create_empty_file(filename, parent="."):
            path = os.path.join(parent, filename)
            open(path, "w").close()
            return path

        self.test_dir = mkdtemp("test_arxd_arxd")
        self.old_cwd = os.getcwd()
        os.chdir(self.test_dir)

        self.ar_paths = []
        self.non_ar_paths = []
        self.tmp_files_paths = []

        # directory hold temp files
        os.mkdir("files")

        # create temporary files
        for char in ascii_lowercase:
            path = create_empty_file(f"tmp_{char}", "files")
            self.tmp_files_paths.append(path)

        # create temporary archives
        for fmt_name, fmt_exts, fmt_desc in shutil.get_unpack_formats():
            path = shutil.make_archive("archive", fmt_name, "files")
            self.ar_paths.append(path)

        # create temporary non-archive files
        for path in self.tmp_files_paths:
            path = create_empty_file(path + ".txt")
            self.non_ar_paths.append(path)

    def test_avail_ar_exts(self):
        data = list(arxd.avail_ar_exts())
        accurate_data = []
        for fmt_name, fmt_exts, fmt_desc in shutil.get_unpack_formats():
            accurate_data.extend(fmt_exts)
        self.assertTrue(data, accurate_data)

    def test_is_ar(self):
        self.assertTrue(
            all(map(arxd.is_ar, self.ar_paths)) and
            not all(map(arxd.is_ar, self.non_ar_paths))
        )

    def test_strip_ext_with_archive(self):
        basename = os.path.basename
        for path in self.ar_paths:
            self.assertTrue(basename(arxd.strip_ext(path)) == "archive")
        
    def test_strip_ext_non_archive(self):
        for path in self.non_ar_paths:
            self.assertTrue(arxd.strip_ext(path) is None)

    def test_ex_ar_without_prefix(self):
        basename = os.path.basename
        for path in self.ar_paths:
            with tempfile.TemporaryDirectory() as tmpdir:
                arxd.ex_ar(path, "")
                self.assertTrue(
                    set(os.listdir("archive")) -
                    set(map(basename, self.tmp_files_paths)) ==
                    set()
                )

    def test_ex_ar_with_prefix(self):
        basename = os.path.basename
        for path in self.ar_paths:
            with tempfile.TemporaryDirectory() as tmpdir:
                arxd.ex_ar(basename(path), tmpdir)
                self.assertTrue(
                    set(os.listdir(os.path.join(tmpdir, "archive"))) -
                    set(map(basename, self.tmp_files_paths)) ==
                    set()
                )

    def tearDown(self):
        os.chdir(self.old_cwd)
        shutil.rmtree(self.test_dir)
