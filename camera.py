import emulation
import image

import PIL
import io

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

    def preview(self):
        # required configuration will depend on camera type!
        print('Checking camera config')
        # get configuration tree
        config = gp.check_result(gp.gp_camera_get_config(self.camera))
        # find the image format config item
        # camera dependent - 'imageformat' is 'imagequality' on some
        OK, image_format = gp.gp_widget_get_child_by_name(config, 'imageformat')
        if OK >= gp.GP_OK:
            # get current setting
            value = gp.check_result(gp.gp_widget_get_value(image_format))
            # make sure it's not raw
            if 'raw' in value.lower():
                print('Cannot preview raw images')
                return 1
        # find the capture size class config item
        # need to set this on my Canon 350d to get preview to work at all
        OK, capture_size_class = gp.gp_widget_get_child_by_name(
            config, 'capturesizeclass')
        if OK >= gp.GP_OK:
            # set value
            value = gp.check_result(gp.gp_widget_get_choice(capture_size_class, 2))
            gp.check_result(gp.gp_widget_set_value(capture_size_class, value))
            # set config
            gp.check_result(gp.gp_camera_set_config(camera, config))
        # capture preview image (not saved to camera memory card)
        print('Capturing preview image')
        camera_file = gp.check_result(gp.gp_camera_capture_preview(camera))
        file_data = gp.check_result(gp.gp_file_get_data_and_size(camera_file))
        # display image
        data = memoryview(file_data)
        print(type(data), len(data))
        print(data[:10].tolist())
        image = PIL.Image.open(io.BytesIO(file_data))
        return image

    def capture(self):
        print('Capturing image')
        if emulation.active():
            return "res/kivybooth-test.jpg"
        else:
            file_path = self.camera.capture(gp.GP_CAPTURE_IMAGE)
            print('Camera file path: {0}/{1}'.format(file_path.folder, file_path.name))
            img = image.Image()
            print('Copying image to', img.path)
            camera_file = self.camera.file_get(
                file_path.folder, file_path.name, gp.GP_FILE_TYPE_NORMAL)
            camera_file.save(img.path)
            return img

    def close(self):
        if self.camera:
            self.camera.exit()
            self.camera = None

    def __del__(self):
        self.close()


if __name__ == "__main__":
    with Camera() as cam: 
        cam.capture()
