import os

SCRIPT_PATH = f"{os.path.split(os.path.abspath(__file__))[0]}"
RENDERER_CONFIG = {
    "input_directory": f"{SCRIPT_PATH}/raw/",
    "input_file_extensions": (".md", ".markdown"),
    "image_file_extensions": (".jpg", ".jpeg", ".png", ".svg"),
    "output_directory": f"{SCRIPT_PATH}/static/rendered/",
    "image_directory": f"{SCRIPT_PATH}/static/images/post/",
    "pandoc_extra_args": [],
}
NOTES_DIR = "notes"
SITE_NAME = "It's Never The Network"
HEADER_TEXT = "It's Never The Network"
DEFAULT_META_DESCRIPTION = "It's Never The Network! Technical deep dives, network tools and more!"
HEADER_IMAGE = "ntn.png"
NAV_LINKS = [
    ["/", "Home"],
    ["/tools", "Tools"],
    ["/about", "About"],
]
STYLESHEET = "notes-core.css"
URI = "neverthenetwork.com"
PANDOC_PATH = "/usr/bin/pandoc"
PRODUCTION = True
