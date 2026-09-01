import mimetypes

from common.base_api import BaseAPI
from config.headers import Headers
from services.upload.endpoints import Endpoints
from services.upload.models.model_upload_image import ResponseUploadImageModel
from utils.data_helper import DataHelper

data_helper = DataHelper()

class UploadsAPI(BaseAPI):
    def __init__(self):
        super().__init__()
        self.endpoints = Endpoints()
        self.headers = Headers()

    def upload_image(self, image_name: str, status_code: int = 200, expected_success: bool = True):
        """
        API, used for uploading images
        :param image_name: provided image name with extension
        :param status_code:
        :param expected_success:
        :return:
        """
        bin_file = data_helper.get_file_as_binary(image_name)
        content_type, _ = mimetypes.guess_type(image_name)
        response =  self.request()\
            .set_url(self.endpoints.upload_image) \
            .set_headers(self.headers.basic) \
            .set_multipart_file(
                file_name=image_name,
                content_type=content_type,
                file_content=bin_file,
                )\
            .send("POST")
        return self.validate_response(response, ResponseUploadImageModel, status_code=status_code, expected_success=expected_success)