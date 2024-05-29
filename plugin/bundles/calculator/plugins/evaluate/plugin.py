from bundle_dependency import *
import sympy as sp


class Evaluate(PluginHandler):
    async def execute(self, credentials: BundleCredentials, plugin_input: PluginInput) -> PluginOutput:
        expression: str = plugin_input.input_params.get("expression")
        try:
            expression = sp.sympify(expression)
            result = expression.evalf()
            return PluginOutput(data={"result": str(result)})
        except Exception as e:
            raise_http_error(
                ErrorCode.REQUEST_VALIDATION_ERROR, "Invalid expression. Please provide a valid expression."
            )
