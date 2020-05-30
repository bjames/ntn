import pypandoc
import os
import re

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


def render_all():

    notes = []

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

            notes.append(Note(output_file, clean_filename, **metadata))

    return notes

if __name__ == "__main__":

    render_all()
