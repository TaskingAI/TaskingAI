import random

from bundle_dependency import *


class GenerateRandomIntegers(PluginHandler):
    async def execute(self, credentials: BundleCredentials, plugin_input: PluginInput) -> PluginOutput:
        min: int = plugin_input.input_params.get("min")
        max: int = plugin_input.input_params.get("max")
        number: int = plugin_input.input_params.get("number")

        if min >= max:
            raise_http_error(ErrorCode.REQUEST_VALIDATION_ERROR, "min should be less than max")

        results = []
        for i in range(number):
            results.append(random.randint(min, max))

        return PluginOutput(status=200, data={"result": results})
