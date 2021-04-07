import kivysome
import os.path


#KIT = "https://kit.fontawesome.com/58bcf53674.js"
VERSION = "5.15.3"
FOLDER = os.path.join(os.path.dirname(__file__), "..", "venv", "lib", "fonts")


# Test whether kivysome caching actually works
def test_caching():
    # Remove kivysome internet access
    kivysome.kivysome.urllib3 = None
    kivysome.kivysome.lastversion = None
    # We cannot load a specific kit here, this is not supported offline by kivysome.
    kivysome.enable(VERSION, font_folder=FOLDER)


kivysome.enable(VERSION, font_folder=FOLDER, group=kivysome.FontGroup.SOLID)
if __name__ == "__main__":
    test_caching()
    print("Successfully chached fontawesome {}".format(VERSION))
