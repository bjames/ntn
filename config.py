import os

SCRIPT_PATH = f"{os.path.split(os.path.abspath(__file__))[0]}"
RENDERER_CONFIG = {
    "input_directory": f"{SCRIPT_PATH}/raw/",
    "input_file_extensions": (".md", ".markdown"),
    "output_directory": f"{SCRIPT_PATH}/static/rendered/",
    "pandoc_extra_args": [],
}
NOTES_DIR = "notes"
SITE_NAME = "Never The Network"
HEADER_TEXT = "It's Never The Network"
HEADER_IMAGE = "ntn_black.png"
NIGHT_MODE_HEADER_IMAGE = "ntn_night.png"
NAV_LINKS = [
    ["/", "Home"],
    ["/about", "About"],
]
STYLESHEET = "notes-core.css"
URI = "neverthenetwork.com"
PANDOC_PATH = "/usr/bin/pandoc"
PRODUCTION = False