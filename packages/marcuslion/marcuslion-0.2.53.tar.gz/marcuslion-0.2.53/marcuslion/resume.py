from marcuslion.restcontroller import RestController
from marcuslion.config import IS_BACKEND_PARAM


class Resume(RestController):
    def __init__(self):
        super().__init__("/resume")

    def upload(self, file_path) -> any:
        return super().upload_file("/upload", file_path, {
            IS_BACKEND_PARAM: True
        })
