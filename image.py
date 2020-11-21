from PIL import Image





class Thumbnail:
    thumb_id = 0

    def __init__(self, orig):
        im = Image.open(orig)
        im.thumbnail((600, 400))
        self.path = "/tmp/thumbnail{:06d}.jpg".format(Thumbnail.thumb_id)
        Thumbnail.thumb_id += 1
        im.save(self.path, "JPEG")
