import os

class Note:

    """
        contains paths to raw note files and attributes about the note files

        TODO: This should be more dynamic, specifically I would like the metadata types to be changable
    """

    def __init__(self, path: str, filename: str, **kwargs):

        # provided by the renderer
        self.path = os.fsdecode(path)    
        self.filename = filename

        # default/required  
        self.title = kwargs.get("title")
        self.author = kwargs.get("author")
        self.publication_date = kwargs.get("publication_date")
        self.summary = kwargs.get("summary")

        self.tags = kwargs.get("tags")

        if self.tags == None:
            self.tags = ["Unfiled"]

        # non-default, default value provided in config
        self.post_image = kwargs.get("post_image")

    def __str__(self):

        return( 
            f"Path: {self.path}\n"
            f"Title: {self.title}\n"
            f"Author: {self.author}\n"
            f"Published: {self.published}\n"
            f"Tags: {self.tags}\n"
            f"Summary: {self.summary}\n"
            f"Update Interval: {self.update_interval}\n"
            f"Post Image: {self.post_image}\n"
        )
