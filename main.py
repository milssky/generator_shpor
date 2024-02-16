import logging
import re
import shutil
import sys
import zipfile

from transliterate import translit

from constants import (
    CLEAN_FILE_NAME_REGEX,
    DIRS_FOR_COPY,
    FILE_ICON_REGEX,
    HEAD_ADD_PRISM_HTML,
    PROPERTIES_TABLE_REGEX,
    RESULT_DIR,
    SCRIPT_LINK_REMOVE_REGEX,
    TEMP_DIR,
    ZIPFILE_DIR,
)
from exceptions import HTMLFileNotFoundError

SCRIPT_LINK_REMOVE_COMPILED_REGEX = re.compile(SCRIPT_LINK_REMOVE_REGEX)
PROPERTIES_TABLE_COMPILED_REGEX = re.compile(PROPERTIES_TABLE_REGEX)
FILE_ICON_REGEX_COMPILED = re.compile(FILE_ICON_REGEX)
CLEAN_FILE_NAME_REGEX_COMPILED = re.compile(CLEAN_FILE_NAME_REGEX)


def transliterate_text(text):
    """Транслитерует текст."""
    return translit(text, "ru", reversed=True).lower()


def delete_directory(directory):
    """Удаляет директорию со всеми вложенными директориями и файлами."""
    shutil.rmtree(directory)


def process_zip(TEMP_DIR, file_path):
    """Обработчик одного архива."""
    if not TEMP_DIR.exists():
        TEMP_DIR.mkdir()
    with zipfile.ZipFile(file_path, "r") as zip_file:
        zip_file.extractall(TEMP_DIR)
    return list(TEMP_DIR.glob("*.html"))


def process_html(file_path):
    """
    Функция, удаляющая ненужные теги и добавляющая нужные теги в html страничку.
    Возвращает имя нового html файла.
    """

    with open(file_path, "r", encoding="utf-8") as html_file:
        html_content = html_file.read()

    html_content = SCRIPT_LINK_REMOVE_COMPILED_REGEX.sub("", html_content)
    html_content = PROPERTIES_TABLE_COMPILED_REGEX.sub("", html_content)
    html_content = FILE_ICON_REGEX_COMPILED.sub("", html_content)
    head_idx = html_content.find("</head>")
    html_content = (
        html_content[:head_idx] + HEAD_ADD_PRISM_HTML + html_content[head_idx:]
    )

    html_file_name = "-".join(file_path.name.split(" ")[:-1])
    new_file_name = transliterate_text(html_file_name)
    new_file_name = CLEAN_FILE_NAME_REGEX_COMPILED.sub("", new_file_name)

    file_path.unlink()

    with open(
        file_path.parent / (new_file_name + ".html"), "w", encoding="utf-8"
    ) as html_file:
        html_file.write(html_content)
    return new_file_name


def clear_directory(directory):
    """Создает гарантированно пустую директорию."""
    if not directory.exists():
        directory.mkdir()
    else:
        delete_directory(directory)
        directory.mkdir()


def main(ZIPFILE_DIR, TEMP_DIR, process_zip):
    """ "Главная функция, обрабатывающая архивы."""
    for file_path in ZIPFILE_DIR.glob("*.zip"):
        source_htmls = process_zip(TEMP_DIR, file_path)
        if not source_htmls:
            raise HTMLFileNotFoundError("Zip file doesn't contain html files")
        file_name = process_html(source_htmls[0])
        destination_folder = RESULT_DIR / file_name
        shutil.copytree(TEMP_DIR, destination_folder)
        delete_directory(TEMP_DIR)
        logging.info(f"Created {destination_folder}")


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s: %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],
    )

    if not ZIPFILE_DIR.exists():
        logging.error(
            f"Directory {ZIPFILE_DIR} does not exist! Create it and put into shopora zip-files!"
        )
        sys.exit(-1)

    for directory in (TEMP_DIR, RESULT_DIR):
        clear_directory(directory)

    main(ZIPFILE_DIR, TEMP_DIR, process_zip)
    for directory in DIRS_FOR_COPY:
        shutil.copytree(directory, RESULT_DIR / directory)
