import os

class Note:

    """
        contains paths to raw note files and attributes about the note files
    """

    def __init__(self, path: str, **kwargs):

        self.path = os.fsdecode(path)
        
        try:
            
            # TODO init note from DB
            raise KeyError

        except KeyError:

            self.__init_note_from_file()
            self.__store_in_db()

    def __init_note_from_file(self):

        """ returns note attributes from parsing metadata in file """

        self.title = "test"
        self.author = "Brandon James"

Note("./")