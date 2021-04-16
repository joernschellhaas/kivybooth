from PIL import Image
import tempfile
import os


# The thumbnail file will be deleted when the object is deleted. Therefore, always store a reference to the object as long as the file is required.
class Thumbnail:

    def __init__(self, orig):
        im = Image.open(orig)
        im.thumbnail((600, 400))
        fileno, self.path = tempfile.mkstemp(suffix=".jpg")
        with open(fileno) as file:
            im.save(file, "JPEG")

    def __del__(self):
        os.remove(self.path)
