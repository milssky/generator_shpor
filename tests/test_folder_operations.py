import os
import shutil
import unittest
from pathlib import Path

from convert import clear_directory, delete_directory


class TestDirectoryOperations(unittest.TestCase):
    def setUp(self):
        self.temp_dir = Path("test_directory")
        self.temp_dir.mkdir()

    def tearDown(self):
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)


class TestDeleteDirectory(TestDirectoryOperations):
    def setUp(self):
        super().setUp()
        with open(self.temp_dir / "test_file.txt", "w") as file:
            file.write("Test data")

    def test_delete_directory(self):
        """Проверка, что функция корректно удаляет директорию и все ее содержимое."""
        directory = "test_directory"
        delete_directory(directory)
        self.assertFalse(os.path.exists(directory))


class TestClearDirectory(TestDirectoryOperations):
    def setUp(self):
        super().setUp()
        with open(self.temp_dir / "test_file1.txt", "w") as f:
            f.write("Test data")
        with open(self.temp_dir / "test_file2.txt", "w") as f:
            f.write("Test data")

    def test_clear_directory(self):
        """Проверка что функция создает пустую директорию."""
        clear_directory(self.temp_dir)
        self.assertTrue(self.temp_dir.exists())
        self.assertEqual(len(os.listdir(self.temp_dir)), 0)

    def test_clear_directory_with_nonexistent_directory(self):
        """Проверка, что функция корректно работает с несуществующей директорией."""
        nonexistent_directory = Path("nonexistent_directory")
        self.assertFalse(nonexistent_directory.exists())
        clear_directory(nonexistent_directory)
        self.assertTrue(nonexistent_directory.exists())
        self.assertEqual(len(os.listdir(nonexistent_directory)), 0)
        nonexistent_directory.rmdir()
