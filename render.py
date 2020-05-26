import pypandoc
import os

from config import renderer_config
from yaml import safe_load

from notes import Note

input_directory = os.fspath(renderer_config["input_directory"])
output_directory = os.fspath(renderer_config["output_directory"])

def get_metadata(file_path: str) -> dict:

    with open(file_path) as markdown_file:

        metadata = ""
        meta_delimiter_count = 0

        for line in markdown_file:

            if "---" in line:

                meta_delimiter_count = meta_delimiter_count + 1

                if meta_delimiter_count > 1:

                    break
            
            elif meta_delimiter_count > 0:

                metadata += line

    return(safe_load(metadata))



def render_all():

    notes = []

    for file in os.listdir(input_directory):

        filename = os.fsdecode(file)
        clean_filename = filename.strip(renderer_config["input_file_extensions"])
        file_path = f"{input_directory}{filename}"

        if filename.endswith(renderer_config["input_file_extensions"]):

            output_file = f"{output_directory}{clean_filename}.html"

            pypandoc.convert_file(
                file_path,
                "html5",
                outputfile=output_file,
                extra_args=(renderer_config["pandoc_extra_args"])
            )

            metadata = get_metadata(file_path)

            notes.append(Note(output_file, clean_filename, **metadata))

    return notes

if __name__ == "__main__":

    render_all()
