import asyncio
import pytest

from backend.tests.api_services.sample_code.sample_code import get_sample_code
from backend.tests.common.config import CONFIG


@pytest.mark.web_test
class TestGetCode:

    modules = ["assistant", "model", "collection"]

    @pytest.mark.asyncio
    @pytest.mark.run(order=101)
    @pytest.mark.parametrize("module", modules)
    async def test_get_code(self, module):
        data = {"module": module}
        res = await get_sample_code(data)
        res_json = res.json()
        assert res.status_code == 200,  res.json()
        assert res_json.get("status") == "success"
        assert len(res_json.get("data")) > 0
