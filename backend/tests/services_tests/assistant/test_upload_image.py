import pytest
import os

from backend.tests.api_services.image.image import upload_image


@pytest.mark.api_test
class TestUploadImage:
    upload_image_list = []
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
            upload_image_list.append(upload_image_dict)

    @pytest.mark.run(order=201)
    @pytest.mark.asyncio
    @pytest.mark.parametrize("upload_image_data", upload_image_list[:2])
    async def test_upload_image(self, upload_image_data):
        res = await upload_image(upload_image_data)
        assert res.status_code == 200, res.json()
        assert res.json()["status"] == "success"
        url = res.json()["data"]["url"]
        assert url is not None
        assert os.path.isfile(url)
