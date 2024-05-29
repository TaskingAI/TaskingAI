from bundle_dependency import *


class Divide(PluginHandler):

    async def execute(
            self,
            credentials: BundleCredentials,
            plugin_input: PluginInput,
    ) -> PluginOutput:

        input_params = plugin_input.input_params
        number_1 = input_params["number_1"]
        number_2 = input_params["number_2"]

        if number_2 == 0:
            raise_http_error(
                ErrorCode.PROVIDER_ERROR,
                "number_2 cannot be 0"
            )

        return PluginOutput(
            data={
                "result": number_1 / number_2
            }
        )

