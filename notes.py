import os

class Note:

    """
        contains paths to raw note files and attributes about the note files

        TODO: This should be more dynamic, specifically I would like the metadata types to be changable
    """

    def __init__(self, path: str, filename: str, **kwargs):

        self.path = os.fsdecode(path)    
        self.filename = filename    
        self.title = kwargs.get("title")
        self.author = kwargs.get("author")
        self.published = kwargs.get("published") 
        self.category = kwargs.get("category")
        self.summary = kwargs.get("summary")
        self.update_interval = kwargs.get("update_interval")
        self.post_image = kwargs.get("post_image")

    def __init_note_from_file(self):

        """ returns note attributes from parsing metadata in file """

    def __str__(self):

        return( 
            f"Path: {self.path}\n"
            f"Title: {self.title}\n"
            f"Author: {self.author}\n"
            f"Published: {self.published}\n"
            f"Category: {self.category}\n"
            f"Summary: {self.summary}\n"
            f"Update Interval: {self.update_interval}\n"
            f"Post Image: {self.post_image}\n"
        )
