import os
import sys
import markovify

class Model:
    def resource_path(self, relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        if hasattr(sys, '_MEIPASS'):
            return os.path.join(sys._MEIPASS, relative_path)
        elif os.path.exists(relative_path):
            return os.path.abspath(relative_path)
        else:
            base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
            return os.path.join(base_path, relative_path)

    def __init__(self):
        # Load the text corpus to use for generating sentences
        with open(self.resource_path("logs.txt"), encoding="utf8") as f:
            text = f.read()
        # Build the Markov model for the text
        self.model = markovify.Text(text)