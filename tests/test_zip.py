import unittest
import zipfile
from unittest.mock import patch
from pathlib import Path

from convert import process_zip
from exceptions import ZipFileError


class TestProcessZip(unittest.TestCase):
    def setUp(self):
        self.temp_dir = Path("temp")
        self.temp_dir.mkdir(exist_ok=True)

    def tearDown(self):
        if self.temp_dir.exists():
            for file in self.temp_dir.iterdir():
                file.unlink()
            self.temp_dir.rmdir()

    def test_process_zip_successful(self):
        with zipfile.ZipFile("test.zip", "w") as zip_file:
            zip_file.writestr("test.html", "<html></html>")

        files = process_zip(self.temp_dir, "test.zip")

        self.assertEqual(len(files), 1)
        self.assertEqual(files[0], self.temp_dir / "test.html")
        self.assertTrue((self.temp_dir / "test.html").exists())

    def test_process_nonexist_zipfile(self):
        with self.assertRaises(FileNotFoundError):
            process_zip(self.temp_dir, "nonexistent.zip")

    def test_process_zip_bad_zipfile(self):
        with open("bad_zipfile.zip", "w") as f:
            f.write("this is not a zip file")

        with patch("zipfile.ZipFile.open") as mock_open:
            mock_open.side_effect = zipfile.BadZipfile
            with self.assertRaises(ZipFileError):
                process_zip(self.temp_dir, "bad_zipfile.zip")

        self.assertEqual(len(list(self.temp_dir.glob("*"))), 0)
