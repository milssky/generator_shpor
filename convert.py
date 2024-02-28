import logging
import shutil
import sys
import zipfile
from pathlib import Path
from typing import Callable, Sequence

from bs4 import BeautifulSoup
from transliterate import translit

from constants import (
    CLEAN_FILE_NAME_REGEX_COMPILED,
    BODY_ADD_HTML,
    CLEAR_BODY_STYLE_REGEX_COMPILED,
    DIRS_FOR_COPY,
    FILE_ICON_REGEX_COMPILED,
    HEAD_ADD_PRISM_ICONS_STYLES_HTML,
    LAMP_ICON_REMOVE_REGEX_COMPILED,
    NEW_BODY_STYLE,
    PROPERTIES_TABLE_REGEX_COMPILED,
    RESULT_DIR,
    SCRIPT_LINK_REMOVE_REGEX_COMPILED,
    TEMP_DIR,
    ZIPFILE_DIR,
)
from exceptions import DirectoryDoesNotExistError, HTMLFileNotFoundError, ZipFileError


def transliterate_text(text):
    """Транслитерует текст."""
    if not isinstance(text, str):
        raise TypeError("Параметр text должен иметь тип str")
    return translit(text, "ru", reversed=True).lower()


def delete_directory(directory):
    """Удаляет директорию со всеми вложенными директориями и файлами."""
    shutil.rmtree(directory)


def process_zip(TEMP_DIR, file_path):
    """Обработчик одного архива. Извлекает файлы и папки из архива."""
    if not TEMP_DIR.exists():
        TEMP_DIR.mkdir()
    try:
        with zipfile.ZipFile(file_path, "r") as zip_file:
            zip_file.extractall(TEMP_DIR)
    except FileNotFoundError:
        raise FileNotFoundError("Файл не найден")
    except zipfile.BadZipfile:
        raise ZipFileError(f"Ошибка во время открытия zip файла - {file_path}")
    return list(TEMP_DIR.glob("*.html"))


def find_id(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    rows = soup.find_all('tr')
    for row in rows:
        if 'ID' in row.text:
            return row.find('td').text
    


def process_html(file_path):
    """
    Функция, удаляющая ненужные теги и добавляющая нужные теги в html страничку.
    Возвращает имя нового html файла.
    """

    with open(file_path, "r", encoding="utf-8") as html_file:
        html_content = html_file.read()

    html_content = SCRIPT_LINK_REMOVE_REGEX_COMPILED.sub("", html_content)

    cheatsheet_id = find_id(html_content)

    html_content = PROPERTIES_TABLE_REGEX_COMPILED.sub("", html_content)
    html_content = FILE_ICON_REGEX_COMPILED.sub("", html_content)
    html_content = LAMP_ICON_REMOVE_REGEX_COMPILED.sub("", html_content)
    html_content = CLEAR_BODY_STYLE_REGEX_COMPILED.sub(NEW_BODY_STYLE, html_content)

    head_idx = html_content.find("</head>")
    html_content = (
        html_content[:head_idx] + HEAD_ADD_PRISM_ICONS_STYLES_HTML + html_content[head_idx:]
    )
    body_idx = html_content.find("</body>")
    html_content = (
        html_content[:body_idx] + BODY_ADD_HTML + html_content[body_idx:]
    )

    new_file_name = cheatsheet_id + '-' + generate_new_filename(file_path) + ".html"
    file_path.unlink()

    with open(
        file_path.parent / new_file_name, "w", encoding="utf-8"
    ) as html_file:
        html_file.write(html_content)
    return new_file_name


def generate_new_filename(file_path):
    """Генерирует новое имя файла из имени html файла шпоры."""
    html_file_name = "-".join(file_path.name.split(" ")[:-1])
    new_file_name = transliterate_text(html_file_name)
    new_file_name = CLEAN_FILE_NAME_REGEX_COMPILED.sub("", new_file_name)
    return new_file_name.replace('-ja', '')


def clear_directory(directory):
    """Создает гарантированно пустую директорию."""
    if not directory.exists():
        directory.mkdir()
    else:
        delete_directory(directory)
        directory.mkdir()


def main(
    zip_dir: Path,
    temp_dir: Path,
    result_dir: Path,
    commot_static_dirs: tuple,
    process_zip: Callable[[Path, Path], Sequence[Path]],
):
    """Главная функция, обрабатывающая архивы."""
    if not zip_dir.exists():
        raise DirectoryDoesNotExistError(
            f"Директория {zip_dir} недоступна! Создайте ее и положите внутрь zip-архивы шпор!"
        )

    for directory in (temp_dir, result_dir):
        clear_directory(directory)

    for file_path in zip_dir.glob("*.zip"):
        source_htmls = process_zip(temp_dir, file_path)
        if not source_htmls:
            raise HTMLFileNotFoundError("Внутри zip-архива нет html файлов!")
        file_name = process_html(source_htmls[0])
        destination_folder = result_dir / file_name
        try:
            shutil.copytree(temp_dir, destination_folder)
        except Exception:
            pass
        delete_directory(temp_dir)
        logging.info(f"Created {destination_folder}")

    for directory in commot_static_dirs:
        shutil.copytree(directory, result_dir / directory)



if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s: %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],
    )

    try:
        main(ZIPFILE_DIR, TEMP_DIR, RESULT_DIR, DIRS_FOR_COPY, process_zip)
    except Exception as e:
        logging.error(e)
