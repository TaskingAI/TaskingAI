from typing import List

import base64
from app.service.image_storage import save_base64_image_to_s3_or_local
from bundle_dependency import *
from config import CONFIG

import plotly.express as px


class MakeLineChart(PluginHandler):
    async def execute(self, credentials: BundleCredentials, plugin_input: PluginInput) -> PluginOutput:
        x_values: List[float] = plugin_input.input_params.get("x_values")
        y_values: List[float] = plugin_input.input_params.get("y_values")
        title: str = plugin_input.input_params.get("title", "Line Chart")
        x_title: str = plugin_input.input_params.get("x_title", "x")
        y_title: str = plugin_input.input_params.get("y_title", "y")

        project_id: str = plugin_input.project_id

        if not project_id:
            raise_http_error(ErrorCode.REQUEST_VALIDATION_ERROR, "project_id is required")

        if len(x_values) != len(y_values):
            raise_provider_api_error("Number of labels and values do not match")

        fig = px.line(x=x_values, y=y_values, title=title, labels={"x": x_title, "y": y_title})

        bytes_fig = fig.to_image(format="png")
        # convert image bytes to base64 string
        base_64_fig = base64.b64encode(bytes_fig).decode("utf-8")

        url = await save_base64_image_to_s3_or_local(
            base_64_fig, project_id, "png", "chart_maker/make_line_chart"
        )

        return PluginOutput(data={"url": url})
