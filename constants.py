import pathlib

BASE_DIR = pathlib.Path(__file__).resolve().parent
ZIPFILE_DIR = BASE_DIR / "zip"
RESULT_DIR = BASE_DIR / "result"
TEMP_DIR = BASE_DIR / "temp"

SCRIPT_LINK_REMOVE_REGEX = r"<script src=\"https:\/\/cdnjs\.cloudflare.com\/ajax\/libs\/prism\/.*<\/script><link rel=\"stylesheet\" href=\"https:\/\/cdnjs\.cloudflare.com\/ajax\/libs\/prism\/.*\/>"
PROPERTIES_TABLE_REGEX = r"<table class=\"properties\".+<\/table>"
FILE_ICON_REGEX = r"<div class=\"page-header-icon.+<\/div>"
CLEAN_FILE_NAME_REGEX = r"[^a-zA-Z0-9\ \-]"

HEAD_ADD_PRISM_HTML = """
<link href="../prism/prism.css" rel="stylesheet" />
<script src="../prism/prism.js"></script>
<link rel="icon" href="../static/favicon.ico" type="image/x-icon">
<link href="../static/custom.css" rel="stylesheet" />
<script src="../static/custom.js"></script>
"""

PRISM_DIR = 'prism'
STATIC_DIR = 'static'
DIRS_FOR_COPY = (PRISM_DIR, STATIC_DIR)