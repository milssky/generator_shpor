import unittest

from main import transliterate_text


class TestTransliterate(unittest.TestCase):
    def test_transliterate_text(self):
        """Проверка, что функция корректно транслитерирует текст."""
        input_text = "Привет, мир!"
        expected_output = "privet, mir!"
        self.assertEqual(transliterate_text(input_text), expected_output)

    def test_transliterate_text_with_empty_input(self):
        """Проверка, что функция возвращает пустую строку при пустом вводе."""
        input_text = ""
        expected_output = ""
        self.assertEqual(transliterate_text(input_text), expected_output)

    def test_transliterate_text_with_non_string_input(self):
        """Проверка, что функция вызывает исключение, если на вход подается не строка."""
        input_text = 123
        with self.assertRaises(TypeError):
            transliterate_text(input_text)
