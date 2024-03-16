import os
import pathlib
import re

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = pathlib.Path(__file__).resolve().parent
ZIPFILE_DIR = BASE_DIR / "zip"
RESULT_DIR = BASE_DIR / "result"
TEMP_DIR = BASE_DIR / "temp"

SCRIPT_LINK_REMOVE_REGEX = r"<script src=\"https:\/\/cdnjs\.cloudflare.com\/ajax\/libs\/prism\/.+?<\/script><link rel=\"stylesheet\" href=\"https:\/\/cdnjs\.cloudflare.com\/ajax\/libs\/prism\/.*?\/>"
PROPERTIES_TABLE_REGEX = r"<table class=\"properties\".+<\/table>"
FILE_ICON_REGEX = r"<div class=\"page-header-icon.+?<\/div>"
CLEAN_FILE_NAME_REGEX = r"[^a-zA-Z0-9\ \-]"
LAMP_ICON_REMOVE_REGEX = r"<span class=\"icon\">.+?<\/span>"
CLEAR_BODY_STYLE_REGEX = r"""body {
	line-height: 1.5;
	white-space: pre-wrap;
}"""


SCRIPT_LINK_REMOVE_REGEX_COMPILED = re.compile(SCRIPT_LINK_REMOVE_REGEX)
PROPERTIES_TABLE_REGEX_COMPILED = re.compile(PROPERTIES_TABLE_REGEX)
FILE_ICON_REGEX_COMPILED = re.compile(FILE_ICON_REGEX)
CLEAN_FILE_NAME_REGEX_COMPILED = re.compile(CLEAN_FILE_NAME_REGEX)
LAMP_ICON_REMOVE_REGEX_COMPILED = re.compile(LAMP_ICON_REMOVE_REGEX)
CLEAR_BODY_STYLE_REGEX_COMPILED = re.compile(CLEAR_BODY_STYLE_REGEX)

HEAD_ADD_PRISM_ICONS_STYLES_HTML = """
<link rel="apple-touch-icon" sizes="180x180" href="../static/ico/apple-touch-icon.png">
<link rel="icon" type="image/png" sizes="32x32" href="../static/ico/favicon-32x32.png">
<link rel="icon" type="image/png" sizes="16x16" href="../static/ico/favicon-16x16.png">
<link rel="manifest" href="../static/ico/site.webmanifest">
<link rel="mask-icon" href="../static/ico/safari-pinned-tab.svg" color="#5bbad5">
<link rel="shortcut icon" href="../static/ico/favicon.ico">
<meta name="msapplication-TileColor" content="#da532c">
<meta name="msapplication-config" content="../static/ico/browserconfig.xml">
<meta name="theme-color" content="#ffffff">
<link href="../prism/prism.css" rel="stylesheet" />
<script src="../prism/prism.js"></script>
<link href="../static/custom.css" rel="stylesheet" />
<script src="../static/custom.js"></script>
<base target="_blank">
"""

NEW_BODY_STYLE = """body {
	line-height: 1.5;
}"""

BODY_ADD_HTML = """
<div id="footer">
	<div id="saying" class="sans">
		<div class="text"></div> 
        <div class="src"></div>
	</div>
</div>
"""

PRISM_DIR = "prism"
STATIC_DIR = "static"
DIRS_FOR_COPY = (PRISM_DIR, STATIC_DIR)


# TODO: Измени на переменную окружения
API_TOKEN = os.getenv("API_TOKEN")
WELCOME_MESSAGE = (
    "Привет! \n\nЭто генератор шпор для ЯПа из Notion. \n\n"
    "Чтобы мной воспользоваться, убедись, что "
    "в Notion в шпаргалке в верхней таблице есть атрибут ID. "
    "После этого экспортируй шпору в формате HTML. \n"
    "Полученный архив отправь мне. \n\n"
    "В архиве будут добавлены файлы статики и скриптов, необходимые для шпор. \n"
    "Пока поддерживается обработка архива с одной шпаргалкой!\n\n"
    "Все остальные сообщения будут проигнорированы. ⬇️"
)
WRONG_FORMAT_MESSAGE = "Отправлен не .zip архив. Попробуйте снова."
HANDLE_ZIP_MESSAGE = "Получен архив со шпаргалкой. Обработка. В ответе будет готовая для загрузки шпаргалка в .zip архиве."
