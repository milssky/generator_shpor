import pathlib
import re
import shutil
import zipfile

from transliterate import translit

from constants import (
    ZIPFILE_DIR,
    RESULT_DIR,
    TEMP_DIR,
    CLEAN_FILE_NAME_REGEX,
    FILE_ICON_REGEX,
    PROPERTIES_TABLE_REGEX,
    SCRIPT_LINK_REMOVE_REGEX,
    HEAD_ADD_PRISM_HTML,
)
from exceptions import DirectoryDoesNotExist, HTMLFileNotFoundError


SCRIPT_LINK_REMOVE_COMPILED_REGEX = re.compile(SCRIPT_LINK_REMOVE_REGEX)
PROPERTIES_TABLE_COMPILED_REGEX = re.compile(PROPERTIES_TABLE_REGEX)
FILE_ICON_REGEX_COMPILED = re.compile(FILE_ICON_REGEX)
CLEAN_FILE_NAME_REGEX_COMPILED = re.compile(CLEAN_FILE_NAME_REGEX)


def transliterate_text(text):
    text = translit(text, "ru", reversed=True).lower()
    return text


def delete_directory(directory):
    """Удаляет директорию со всеми вложенными директориями и файлами."""
    for item in directory.iterdir():
        if item.is_dir():
            delete_directory(item)
        else:
            item.unlink()
    directory.rmdir()


def process_zip(TEMP_DIR, file_path):
    if not TEMP_DIR.exists():
        TEMP_DIR.mkdir()
    with zipfile.ZipFile(file_path, "r") as zip_file:
        zip_file.extractall(TEMP_DIR)
    return list(TEMP_DIR.glob("*.html"))


def process_html(file_path):
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


def main(ZIPFILE_DIR, TEMP_DIR, process_zip):
    for file_path in ZIPFILE_DIR.glob("*.zip"):
        source_htmls = process_zip(TEMP_DIR, file_path)
        if not source_htmls:
            raise HTMLFileNotFoundError("Zip file doesn't contain html files")
        file_name = process_html(source_htmls[0])
        destination_folder = RESULT_DIR / file_name
        shutil.copytree(TEMP_DIR, destination_folder)
        delete_directory(TEMP_DIR)


if __name__ == "__main__":
    if not ZIPFILE_DIR.exists():
        raise DirectoryDoesNotExist(f"{ZIPFILE_DIR} does not exist")

    if not TEMP_DIR.exists():
        TEMP_DIR.mkdir()
    else:
        delete_directory(TEMP_DIR)
        TEMP_DIR.mkdir()

    if not RESULT_DIR.exists():
        RESULT_DIR.mkdir()
    else:
        delete_directory(RESULT_DIR)
        RESULT_DIR.mkdir()

    main(ZIPFILE_DIR, TEMP_DIR, process_zip)
    shutil.copytree("./prism", RESULT_DIR / "prism")
    shutil.copytree("./static", RESULT_DIR / "static")
