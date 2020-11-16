from PIL import Image


def thumbnail(orig):
    im = Image.open(orig)
    im.thumbnail((600, 400))
    thumb = orig + ".thumbnail"
    im.save(thumb, "JPEG")
    return thumb
