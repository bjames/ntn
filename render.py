import pypandoc
import os

from config import renderer_config
from yaml import load

input_directory = os.fspath(renderer_config["input_directory"])
output_directory = os.fspath(renderer_config["output_directory"])

for file in os.listdir(input_directory):

    filename = os.fsdecode(file)
    clean_filename = filename.strip(renderer_config["input_file_extensions"])
    file_path = f"{input_directory}{filename}"

    if filename.endswith(renderer_config["input_file_extensions"]):

        pypandoc.convert_file(
            file_path,
            "html5",
            outputfile=f"{output_directory}{clean_filename}.html",
            extra_args=(renderer_config["pandoc_extra_args"])
        )

        with open(file_path) as markdown_file:

            metadata = ""
            meta_block_delimiter = 0

            for line in markdown_file:
    
                if "---" in line:

                    meta_block_delimiter = meta_block_delimiter + 1

                    if meta_block_delimiter > 1:

                        break
                
                elif meta_block_delimiter > 0:

                    metadata += line

            test = load(metadata)

        print(test)