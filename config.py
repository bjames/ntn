RENDERER_CONFIG = {
    "input_directory": "./raw/",
    "input_file_extensions": (".md"),
    "output_directory": "./rendered/",
    "pandoc_extra_args": ["--toc"],
}
NOTES_DIR = "notes"
SITE_NAME = "Never The Network"
HEADER_TEXT = "It's Never The Network"
HEADER_IMAGE = "ntn_black.png"
NAV_LINKS = [
    ["/", "Home"],
    ["/about", "About"]
]
STYLESHEET = "notes-core.css"