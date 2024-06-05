import pytest
import os

from backend.tests.api_services.image.image import upload_image, download_image


@pytest.mark.api_test
class TestUploadImage:
    max_image_data = None
    normal_image_data = None
    base_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    image_names = os.listdir(base_path + "/image")
    for image_name in image_names:
        image_path = os.path.join(base_path, "image", image_name)
        if os.path.isfile(image_path):
            upload_image_dict = {
                "module": "assistant",
                "purpose": "user_message_image",
            }
            upload_image_dict.update({"image": image_path})
            if "5M" in image_name:
                max_image_data = upload_image_dict
            else:
                normal_image_data = upload_image_dict

    @pytest.mark.run(order=201)
    @pytest.mark.asyncio
    async def test_upload_image(self):
        res = await upload_image(self.normal_image_data)
        assert res.status_code == 200, res.json()
        assert res.json()["status"] == "success"
        url = res.json()["data"]["url"]
        assert url is not None
        get_res = await download_image(url)
        assert get_res.status_code == 200, get_res.json()

    @pytest.mark.run(order=201)
    @pytest.mark.asyncio
    async def test_upload_max_image(self):
        res = await upload_image(self.max_image_data)
        assert res.status_code == 422, res.json()
        assert res.json()["status"] == "error"
        assert res.json()["error"]["code"] == "REQUEST_VALIDATION_ERROR"
