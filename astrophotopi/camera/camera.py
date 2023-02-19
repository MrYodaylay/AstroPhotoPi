import gphoto2 as gp

class Camera():

    camera_obj : gp.Camera = None
    camera_config = None

    def __init__(self):
        self.camera_obj = gp.Camera()
        self.camera_obj.init()
        self.camera_config = self.camera_obj.get_config()

    def get_name(self):
        return str(self.camera_config.get_child_by_name("cameramodel").get_value())
