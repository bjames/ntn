RENDERER_CONFIG = {
    "input_directory": "./raw/",
    "input_file_extensions": (".md"),
    "output_directory": "./rendered/",
    "pandoc_extra_args": ["--toc"],
}
NOTES_DIR = "notes"
SITE_NAME = "Notes Core"
NAV_LINKS = [
    ["/", "Home"],
    ["/about", "About"]
]
STYLESHEET = "notes-core.css"