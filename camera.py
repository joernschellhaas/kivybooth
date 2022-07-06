import emulation

if not emulation.active():
    import gphoto2 as gp
import os.path

class Camera:
    def __init__(self):
        if emulation.active():
            print("Initializing emulated camera")
        else:
            self.camera = gp.Camera()
            self.camera.init()
            text = self.camera.get_summary()
            print("Camera Summary", str(text))

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.close()

    def capture(self):
        print('Capturing image')
        if emulation.active():
            return "res/kivybooth-test.jpg"
        else:
            file_path = self.camera.capture(gp.GP_CAPTURE_IMAGE)
            print('Camera file path: {0}/{1}'.format(file_path.folder, file_path.name))
            target = os.path.join('/tmp', file_path.name)
            print('Copying image to', target)
            camera_file = self.camera.file_get(
                file_path.folder, file_path.name, gp.GP_FILE_TYPE_NORMAL)
            camera_file.save(target)
            return target

    def close(self):
        if self.camera:
            self.camera.exit()
            self.camera = None

    def __del__(self):
        self.close()


if __name__ == "__main__":
    with Camera() as cam: 
        cam.capture()
