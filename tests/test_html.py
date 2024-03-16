import re
import unittest
from pathlib import Path

from constants import (
    FILE_ICON_REGEX,
    HEAD_ADD_PRISM_ICONS_STYLES_HTML,
    PROPERTIES_TABLE_REGEX,
    SCRIPT_LINK_REMOVE_REGEX,
)
from convert import process_html


class TestProcessHtml(unittest.TestCase):
    def setUp(self):
        self.test_file_path = Path("test_file.html")
        with open(self.test_file_path, "w", encoding="utf-8") as file:
            # Создаем тестовый файл с HTML содержимым
            file.write(
                """
                <html>
                <head>
                    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/prism.min.js" integrity="sha512-7Z9J3l1+EYfeaPKcGXu3MS/7T+w19WtKQY/n+xzmw4hZhJ9tyYmcUS+4QqAlzhicE5LAfMQSF3iFTK9bQdTxXg==" crossorigin="anonymous" referrerPolicy="no-referrer"></script><link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/themes/prism.min.css" integrity="sha512-tN7Ec6zAFaVSGadasddadsda"/>
                
                </head>
                <body>
                    <table class="properties">
                        <tr>
                            <td>ID</td>
                            <td>001</td>
                        </tr>
                        <tr>
                            <td>Property</td>
                            <td>Value</td>
                        </tr>
                    </table>
                    <div class="page-header-icon"></div>
                </body>
                </html>
                """
            )

    def test_process_html(self):
        new_file_name = process_html(self.test_file_path)

        self.assertFalse(self.test_file_path.exists())
        new_file_path = self.test_file_path.parent / (new_file_name)
        self.assertTrue(new_file_path.exists())

        # Проверяем, что ненужные теги были удалены, а нужный тег добавлен
        with open(new_file_path, "r", encoding="utf-8") as new_file:
            new_html_content = new_file.read()
            self.assertNotRegex(new_html_content, re.compile(SCRIPT_LINK_REMOVE_REGEX))
            self.assertNotRegex(new_html_content, re.compile(PROPERTIES_TABLE_REGEX))
            self.assertNotRegex(new_html_content, re.compile(FILE_ICON_REGEX))
            self.assertRegex(
                new_html_content,
                re.compile(re.compile(HEAD_ADD_PRISM_ICONS_STYLES_HTML)),
            )
        Path.unlink(new_file_path)
