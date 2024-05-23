
import json
from backend.tests.api_services.tool.plugin import *
from backend.tests.services_tests.tool import Tool
from backend.tests.common.logger import *
from backend.tests.common.utils import *


# @pytest.mark.bundle_instance

@pytest.mark.web_test
class TestBundleInstance(Tool):


    @pytest.mark.run(order=171)
    @pytest.mark.asyncio
    async def test_list_bundles(self):

        logger.info("*************** start testcase ***************")

        list_bundles_dict = {"limit": "100", "offset": 0}
        except_dict = {"except_http_code": "200", "except_status": "success"}

        res = await list_bundles(list_bundles_dict)


        logger_info_base(except_dict["except_http_code"], except_dict["except_status"], res)
        assume_count(res, except_dict)
        Tool.bundles = res.json()["data"]


        logger.info("*************** end testcase ***************")


    @pytest.mark.run(order=171)
    @pytest.mark.asyncio
    async def test_list_plugins(self):

        logger.info("*************** start testcase ***************")

        list_plugins_dict = {"bundle_id": "open_weather"}
        except_dict = {"except_http_code": "200", "except_status": "success"}

        res = await list_plugins(list_plugins_dict)

        logger_info_base(except_dict["except_http_code"], except_dict["except_status"], res)
        assume(res, except_dict)
        pytest.assume(len(res.json()["data"]) >= 0)
        for plugin in res.json()["data"]:
            assert plugin["bundle_id"] == list_plugins_dict["bundle_id"]


        logger.info("*************** end testcase ***************")


    @pytest.mark.run(order=172)
    @pytest.mark.asyncio
    async def test_success_create_bundle_instance(self):

        logger.info("*************** start testcase ***************")
        except_dict = {"except_http_code": "200", "except_status": "success"}

        create_bundle_instance_dict_list = [
            {"name": "exchangerate_api",
             "credentials": {
                 "EXCHANGERATE_API_API_KEY": CONFIG.EXCHANGERATE_API_API_KEY
             },
             "bundle_id": "exchangerate_api"

            },
            {"name": "open_weather",
             "credentials": {
                 "OPEN_WEATHER_API_KEY": CONFIG.OPEN_WEATHER_API_KEY
             },
             "bundle_id": "open_weather"}
        ]

        for bundle_instance_dict in create_bundle_instance_dict_list:

            res = await create_bundle_instance(bundle_instance_dict)

            res_data = res.json()["data"]
            logger_info_base(except_dict["except_http_code"], except_dict["except_status"], res)
            assume(res, except_dict)


            assume_bundle_instance(res_data, bundle_instance_dict)

            Tool.bundle_instance_id = res_data["bundle_instance_id"]
            Tool.bundle_instance_name = res_data["name"]
            Tool.bundle_credentials = bundle_instance_dict["credentials"]
            Tool.run_bundles.append(res_data["bundle_instance_id"])

            get_res = await get_bundle_instance(Tool.bundle_instance_id)

            logger_info_base("200", "success", get_res)
            assume(get_res, {"except_http_code": "200", "except_status": "success"})
            pytest.assume(get_res.json()["data"]["bundle_instance_id"] == Tool.bundle_instance_id)
            assume_bundle_instance(get_res.json()["data"], bundle_instance_dict)

        logger.info("*************** end testcase ***************")


    @pytest.mark.run(order=173)
    @pytest.mark.asyncio
    async def test_list_bundle_instances(self):

        logger.info("*************** start testcase ***************")

        list_bundle_instances_data_list = [
            {
                "limit": 10,
                "order": "desc",
                "after": Tool.bundle_instance_id
            },
            {
                "limit": 10,
                "order": "asc",
                "prefix_filter": json.dumps({"name": Tool.bundle_instance_name[:4]})
            },
            {
                "limit": 10,
                "order": "desc",
                "prefix_filter": json.dumps({"bundle_instance_id": Tool.bundle_instance_id[:10]})
            }
        ]

        except_dict = {
            "except_http_code": "200",
            "except_status": "success"
        }
        for list_bundle_instances_dict in list_bundle_instances_data_list:
            res = await list_bundle_instances(list_bundle_instances_dict)
            res_json = res.json()

            logger_info_base(except_dict["except_http_code"], except_dict["except_status"], res)
            assert res.status_code == 200,  res.json()
            assert res_json.get("status") == "success"
            assert len(res_json.get("data")) == 1
            assert res_json.get("fetched_count") == 1
            assert res_json.get("has_more") is False
            if list_bundle_instances_dict.get("prefix_filter"):
                prefix_filter_dict = json.loads(list_bundle_instances_dict.get("prefix_filter"))
                for key in prefix_filter_dict:
                    assert res_json.get("data")[0].get(key).startswith(prefix_filter_dict.get(key))


        logger.info("*************** end testcase ***************")


    @pytest.mark.run(order=174)
    @pytest.mark.asyncio
    async def test_success_get_bundle_instance(self):

        logger.info("*************** start testcase ***************")

        get_res = await get_bundle_instance(Tool.bundle_instance_id)

        logger_info_base("200", "success", get_res)
        assume(get_res, {"except_http_code": "200", "except_status": "success"})

        pytest.assume(get_res.json()["data"]["bundle_instance_id"] == Tool.bundle_instance_id)


        logger.info("*************** end testcase ***************")


    @pytest.mark.run(order=175)
    @pytest.mark.asyncio
    async def test_success_update_bundle_instance(self):

        logger.info("*************** start testcase ***************")

        update_bundle_instance_dict = {"name": "hello bundle", "credentials": Tool.bundle_credentials}
        except_dict = {"except_http_code": "200", "except_status": "success"}

        res = await update_bundle_instance(Tool.bundle_instance_id, update_bundle_instance_dict)

        logger_info_base(except_dict["except_http_code"], except_dict["except_status"], res)
        assume(res, except_dict)
        assume_bundle_instance(res.json()['data'], update_bundle_instance_dict)

        get_res = await get_bundle_instance(Tool.bundle_instance_id)

        logger_info_base("200", "success", get_res)
        assume(get_res, {"except_http_code": "200", "except_status": "success"})
        assume_bundle_instance(get_res.json()['data'], update_bundle_instance_dict)

        pytest.assume(get_res.json()["data"]["bundle_instance_id"] == Tool.bundle_instance_id)


        logger.info("*************** end testcase ***************")


    @pytest.mark.run(order=230)
    @pytest.mark.asyncio
    async def test_success_delete_bundle_instance(self):

        logger.info("*************** start testcase ***************")



        bundle_instances_res = await list_bundle_instances({"limit": 100})
        bundle_instances_data = bundle_instances_res.json()["data"]

        for bundle_instance in bundle_instances_data:
            delete_res = await delete_bundle_instance(bundle_instance["bundle_instance_id"])
            logger_info_base("200", "success", delete_res)
            assume(delete_res, {"except_http_code": "200", "except_status": "success"})

            get_res = await get_bundle_instance(bundle_instance["bundle_instance_id"])
            logger_info_base("404", "error", get_res)
            assume_error(get_res,
                         {"except_http_code": "404", "except_status": "error", "except_error_code": "OBJECT_NOT_FOUND"})


        logger.info("*************** end testcase ***************")
