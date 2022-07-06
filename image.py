import PIL
import tempfile
import os
import threading
import shutil
import logging


class SaveJob:
    MOUNT_FOLDER = "/media"
    FILE_INDEX = -1

    def __init__(self, fh):
        self.source_fh = fh
        self.cancel_req = False
        self.status_val = False
        self.thread = threading.Thread(target=self.run)
        self.thread.start()

    def run(self):
        self.destinations = self.find_destinations()
        target_file = self.find_usable_filename()
        self.progress = 0
        for idx, dest in enumerate(self.destinations):
            if self.cancel_req:
                break
            else:
                dest_path = os.path.join(dest, target_file)
                try:
                    shutil.copyfile(src=self.source_fh.name, dst=dest_path)
                    logging.info(f"Stored {self.source_fh.name} to {dest_path}")
                except OSError as exc:
                    logging.warning(f"Could not store {self.source_fh.name} to {dest_path}", exc_info=exc)
                self.progress = 100 * idx / (len(self.destinations) + 1)
        os.sync()
        self.status_val = True
        self.progress = 100

    def find_destinations(self):
        destinations = []
        for name in os.listdir(self.MOUNT_FOLDER):
            full_path = os.path.join(self.MOUNT_FOLDER, name)
            if os.path.isdir(full_path):
                destinations.append(full_path)
        return destinations

    def find_usable_filename(self):
        SaveJob.FILE_INDEX += 1
        while True:
            target_file = f"IMG{SaveJob.FILE_INDEX:06d}.jpg"
            if self.is_usable_filename(target_file):
                return target_file
            # Otherwise, increase index to next number divisible by 1000
            SaveJob.FILE_INDEX = int(SaveJob.FILE_INDEX / 1000 + 1) * 1000

    def is_usable_filename(self, target_file):
        for dest in self.destinations:
            if os.path.exists(os.path.join(dest, target_file)):
                return False
        return True

    def status(self):
        return (self.status_val, self.progress)

    def cancel(self):
        self.cancel_req = True


# The thumbnail file will be deleted when the object is deleted. Therefore, always store a reference to the object as long as the file is required.
class Thumbnail:

    def __init__(self, orig):
        im = PIL.Image.open(orig)
        im.thumbnail((600, 400))
        self.file = tempfile.NamedTemporaryFile(suffix=".jpg")
        self.path = self.file.name
        im.save(self.file, "JPEG")

    def __del__(self):
        os.remove(self.path)


class Image:

    def __init__(self):
        self.file = tempfile.NamedTemporaryFile(suffix=".jpg")
        self.path = self.file.name

    def start_store(self):
        return SaveJob(self.file)
