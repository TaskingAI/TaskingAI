from bundle_dependency import *


class Subtract(PluginHandler):

    async def execute(
            self,
            credentials: BundleCredentials,
            plugin_input: PluginInput,
    ) -> PluginOutput:

        input_params = plugin_input.input_params
        number_1 = input_params["number_1"]
        number_2 = input_params["number_2"]

        return PluginOutput(
            data={
                "result": number_1 - number_2
            }
        )

