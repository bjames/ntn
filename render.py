import pypandoc
import os
import re

from pathlib import Path
from config import RENDERER_CONFIG
from yaml import safe_load

from notes import Note

input_directory = os.fspath(RENDERER_CONFIG["input_directory"])
output_directory = os.fspath(RENDERER_CONFIG["output_directory"])


def get_metadata(file_path: str) -> dict:

    with open(file_path) as markdown_file:

        metadata = ""
        meta_delimiter_count = 0

        for line in markdown_file:

            if "---" in line:

                meta_delimiter_count = meta_delimiter_count + 1

                if meta_delimiter_count > 1:

                    parsed_metadata = safe_load(metadata)

                    return parsed_metadata
            
            elif meta_delimiter_count > 0:

                metadata += line


def get_summary_from_html(output_file):

    paragraph = re.compile(r"(?:<p>)(.*)(?:</p>)")
    decorators = re.compile(r"<.*?>")
    sup = re.compile(r"<sup?>.*?</sup?>")

    with open(output_file) as html_file:

        for line in html_file:

            try:
                
                result = paragraph.search(line)
                result = sup.sub("", result[1])
                return(decorators.sub("", result))

            except TypeError:

                continue

    return ""


def get_tags(notes):

    tag_set = set()

    for note in notes:

        for tag in note.tags:

            tag_set.add(tag)

    return sorted(tag_set)




def render_all():

    notes = set()
    static_pages = set()

    Path(output_directory).mkdir(parents=True, exist_ok=True)

    for file in os.listdir(input_directory):

        filename = os.fsdecode(file)
        clean_filename = filename.strip(RENDERER_CONFIG["input_file_extensions"])
        file_path = f"{input_directory}{filename}"

        if filename.endswith(RENDERER_CONFIG["input_file_extensions"]):

            output_file = f"{output_directory}{clean_filename}.html"

            pypandoc.convert_file(
                file_path,
                "html5",
                outputfile=output_file,
                extra_args=(RENDERER_CONFIG["pandoc_extra_args"])
            )

            metadata = get_metadata(file_path)

            if "summary" not in metadata:

                metadata["summary"] = get_summary_from_html(output_file)


            if "static_url" in metadata:

                static_pages.add(
                    Note(output_file, clean_filename, **metadata)
                )

            else:

                notes.add(Note(output_file, clean_filename, **metadata))

    tag_set = get_tags(notes)

    published_notes = (note for note in notes if note.publication_date is not None)

    published_notes = sorted(published_notes, reverse=True,
                    key=lambda n: n.publication_date)

    return published_notes, tag_set, static_pages

if __name__ == "__main__":

    render_all()
