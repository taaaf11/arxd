import os
import shutil
import unittest
from string import ascii_lowercase
from tempfile import TemporaryDirectory, mkdtemp

from src.arxd import arxd
from src.arxd.config import Config

pjoin = os.path.join
pexists = os.path.exists
pbasename = os.path.basename


class TestArxd(unittest.TestCase):
    def setUp(self):
        def create_empty_file(filename, parent="."):
            path = pjoin(parent, filename)
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
        for count, rest in enumerate(shutil.get_unpack_formats()):
            fmt_name, fmt_exts, fmt_desc = rest
            path = shutil.make_archive(f"archive{count}", fmt_name, "files")
            self.ar_paths.append(pbasename(path))

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
        for count, path in enumerate(self.ar_paths):
            self.assertTrue(arxd.strip_ext(path) == f"archive{count}")

    def test_strip_ext_non_archive(self):
        for path in self.non_ar_paths:
            self.assertTrue(arxd.strip_ext(path) is None)

    def test_ex_ar_without_prefix(self):
        for count, path in enumerate(self.ar_paths):
            arxd.ex_ar(path, "")
            self.assertTrue(
                set(os.listdir(f"archive{count}")) -
                set(map(pbasename, self.tmp_files_paths)) ==
                set()
            )
            shutil.rmtree(f"archive{count}")

    def test_ex_ar_with_prefix(self):
        for count, path in enumerate(self.ar_paths):
            with TemporaryDirectory(".") as tmpdir:
                arxd.ex_ar(path, tmpdir)
                self.assertTrue(
                    set(os.listdir(pjoin(tmpdir, f"archive{count}"))) -
                    set(map(pbasename, self.tmp_files_paths)) ==
                    set()
                )

    def test_extract_archives_with_auto_del(self):
        with TemporaryDirectory(dir=".") as tmpdir:
            config = Config(
                prefix=pbasename(tmpdir),
                auto_del=True,
                ignore_pattern="~^",
                verbosity=False
            )
            arxd.extract_archives(self.ar_paths, config)
            for path in self.ar_paths:
                self.assertFalse(pexists(path))

    def test_extract_archives_with_auto_del_false(self):
        with TemporaryDirectory(dir=".") as tmpdir:
            config = Config(
                prefix=pbasename(tmpdir),
                auto_del=False,
                ignore_pattern="~^",
                verbosity=False
            )
            arxd.extract_archives(self.ar_paths, config)
            for path in self.ar_paths:
                self.assertTrue(pexists(path))

    def test_extract_archives_with_ignore_pattern(self):
        with TemporaryDirectory(dir=".") as tmpdir:
            config = Config(
                prefix=pbasename(tmpdir),
                auto_del=False,
                ignore_pattern="archive0",  # we ignore archive0.*
                verbosity=False
            )
            arxd.extract_archives(self.ar_paths, config)

            self.assertFalse(pexists("archive0"))
            for count, path in enumerate(self.ar_paths[1:], 1):
                # path to where archive is extracted
                extracted_path = pjoin(tmpdir, f"archive{count}")
                self.assertTrue(pexists(extracted_path))

    def tearDown(self):
        os.chdir(self.old_cwd)
        shutil.rmtree(self.test_dir)
