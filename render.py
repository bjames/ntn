import pypandoc
import os

from config import renderer_config

input_directory = os.fspath(renderer_config["input_directory"])
output_directory = os.fspath(renderer_config["output_directory"])

for file in os.listdir(input_directory):

    filename = os.fsdecode(file)
    clean_filename = filename.strip(renderer_config["input_file_extensions"])
    file_path = f"{input_directory}{filename}"

    if filename.endswith(renderer_config["input_file_extensions"]):

        pypandoc.convert_file(
            file_path,
            "html",
            outputfile=f"{output_directory}{clean_filename}.html",
            extra_args=(renderer_config["pandoc_extra_args"])
        )