import allure
import pytest

from config.base_test import BaseTest
from services.upload.payload import UploadImageByRoleTestCase


@allure.epic("Upload Service")
@allure.feature("Upload")
@allure.parent_suite("Tests Upload service API")
@allure.title("Tests Upload service API")
@pytest.mark.upload
class TestUpload(BaseTest):

    @allure.suite("Upload image")
    @allure.story("User can upload image to attach it to post/comment/message")
    @allure.description("Upload image")
    @pytest.mark.parametrize("case", [
        pytest.param(UploadImageByRoleTestCase(role="admin", file="image.jpg"),
                     id="Upload image, allowed - jpg"),
        pytest.param(UploadImageByRoleTestCase(role="user_bob", file="image.png"),
                     id="Upload image, allowed - png"),
        pytest.param(UploadImageByRoleTestCase(role="moderator", file="image.webp"),
                     id="Upload image, allowed - webp"),
        pytest.param(UploadImageByRoleTestCase(role="user_eve", file="image.gif"),
                     id="Upload image, allowed - gif"),
        pytest.param(UploadImageByRoleTestCase(role="user_eve", file="image.jpeg"),
                     id="Upload image, allowed - jpeg"),
        pytest.param(UploadImageByRoleTestCase(role="user_eve", file="4.2-MB.jpg"),
                     id="Upload image, Size > 4 MB"),
    ])
    def test_upload_image(self, case):
        upload_service = self.get_actor(case.role).upload_api
        upload_service.upload_image(case.file)


    @allure.suite("Upload image")
    @allure.story("User can upload image to attach it to post/comment/message")
    @allure.description("Upload image - invalid file")
    @pytest.mark.parametrize("case", [
        pytest.param(UploadImageByRoleTestCase(role="admin", file="test.txt"),
                     id="Upload image, not allowed - txt"),
        pytest.param(UploadImageByRoleTestCase(role="admin", file="image.svg"),
                     id="Upload image, not allowed - svg"),
        pytest.param(UploadImageByRoleTestCase(role="admin", file="image.exe"),
                     id="Upload image, not allowed - exe"),
        pytest.param(UploadImageByRoleTestCase(role="admin", file="image.zip"),
                     id="Upload image, not allowed - zip"),
        pytest.param(UploadImageByRoleTestCase(role="admin", file="image.png.jpg"),
                     id="Upload image, not allowed - .png.jpg"),
        pytest.param(UploadImageByRoleTestCase(role="admin", file="7.2-MB.jpg"),
                     id="Upload image, too large > 5 Mb"),
    ])
    def test_upload_image_invalid_extension(self, case):
        upload_service = self.get_actor(case.role).upload_api
        upload_service.upload_image(case.file, expected_success=False, status_code=400)