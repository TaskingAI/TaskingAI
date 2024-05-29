import pytest
import os

from test.api_service.image.image import execute

current_file_path = os.path.abspath(__file__)
parent_directory = os.path.dirname(os.path.dirname(current_file_path))
base_path = os.path.join(parent_directory, "app")

class TestExecute:
    request_data = {
    "bundle_id": "chart_maker",
    "plugin_id": "make_line_chart",
    "input_params": {
        "x_values": [1, 2, 3],
        "y_values": [10, 20, 30],
        "title":"test_title",
        "x_title": "test_x",
        "y_title": "test_y"
    },
    "credentials": {

    },
    "project_id":"test_project"
}

    openai_data = {
    "bundle_id": "gpt_vision_models",
    "plugin_id": "chat_completion_by_gpt4_turbo",
    "input_params": {
        "prompt": "Please describe the image.",
        "image_url": "IMAGE_URL"
    },
    "credentials": {
        "OPENAI_API_KEY": os.environ.get("OPENAI_API_KEY", None)
    }
}
    gemini_data = {
    "bundle_id": "gemini_vision_models",
    "plugin_id": "chat_completion_by_gemini_1_0_pro",
    "input_params": {
        "prompt": "Please describe this image",
        "image_url": ""
    },
    "credentials": {
        "GOOGLE_GEMINI_API_KEY": os.environ.get("GOOGLE_GEMINI_API_KEY", None)
    }
}
    S3_BUCKET_PUBLIC_DOMAIN = os.environ.get("S3_BUCKET_PUBLIC_DOMAIN", None)
    S3_ENDPOINT = os.environ.get("S3_ENDPOINT", None)
    HOST_URL = os.environ.get("HOST_URL", None)
    PATH_TO_VOLUME = os.environ.get("PATH_TO_VOLUME", None)

    @pytest.mark.asyncio
    async def test_generate_image_s3_with_public_domain(self):

        res = await execute(self.request_data)
        assert res.status_code == 200, res.json()
        assert res.json()["status"] == "success"
        res_data = res.json()["data"]
        assert res_data["status"] == 200, res_data
        url = res_data["data"]["url"]
        assert url is not None

        self.openai_data["input_params"]["image_url"] = url
        openai_res = await execute(self.openai_data)
        assert openai_res.status_code == 200, openai_res.json()

        self.gemini_data["input_params"]["image_url"] = url
        gemini_res = await execute(self.gemini_data)
        assert gemini_res.status_code == 200, gemini_res.json()

    @pytest.mark.asyncio
    async def test_generate_image_s3_without_public_domain(self):
        res = await execute(self.request_data)
        assert res.status_code == 200, res.json()
        assert res.json()["status"] == "success"
        res_data = res.json()["data"]
        assert res_data["status"] == 200, res_data
        url = res_data["data"]["url"]
        assert url is not None

        self.openai_data["input_params"]["image_url"] = url
        openai_res = await execute(self.openai_data)
        assert openai_res.status_code == 200, openai_res.json()

        self.gemini_data["input_params"]["image_url"] = url
        gemini_res = await execute(self.gemini_data)
        assert gemini_res.status_code == 200, gemini_res.json()

    @pytest.mark.asyncio
    async def test_generate_image_local(self):
        res = await execute(self.request_data)
        assert res.status_code == 200, res.json()
        assert res.json()["status"] == "success"
        res_data = res.json()["data"]
        assert res_data["status"] == 200
        url = res_data["data"]["url"]
        assert url is not None
        assert url.startswith(self.HOST_URL)

        self.openai_data["input_params"]["image_url"] = url
        openai_res = await execute(self.openai_data)
        assert openai_res.status_code == 200, openai_res.json()

        self.gemini_data["input_params"]["image_url"] = url
        gemini_res = await execute(self.gemini_data)
        assert gemini_res.status_code == 200, gemini_res.json()
