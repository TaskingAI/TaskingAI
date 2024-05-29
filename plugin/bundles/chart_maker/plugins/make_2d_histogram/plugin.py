import base64
from typing import List

from app.service.image_storage import save_base64_image_to_s3_or_local
from bundle_dependency import *
import plotly.express as px

from config import CONFIG


class Make2DHistogram(PluginHandler):
    async def execute(self, credentials: BundleCredentials, plugin_input: PluginInput) -> PluginOutput:
        x_values: List[float] = plugin_input.input_params.get("x_values")
        y_values: List[float] = plugin_input.input_params.get("y_values")
        title: str = plugin_input.input_params.get("title", "2D Histogram")
        x_title: str = plugin_input.input_params.get("x_title", "x")
        y_title: str = plugin_input.input_params.get("y_title", "y")
        project_id: str = plugin_input.project_id

        if not project_id:
            raise_http_error(ErrorCode.REQUEST_VALIDATION_ERROR, "project_id is required")

        if len(x_values) != len(y_values):
            raise_http_error(ErrorCode.REQUEST_VALIDATION_ERROR, message="Number of x values and y values do not match")

        fig = px.density_heatmap(x=x_values, y=y_values, title=title, labels={"x": x_title, "y": y_title})
        bytes_fig = fig.to_image(format="png")
        # convert image bytes to base64 string
        base_64_fig = base64.b64encode(bytes_fig).decode("utf-8")

        url = await save_base64_image_to_s3_or_local(
            base_64_fig, project_id, "png", "chart_maker/make_2d_histogram"
        )

        return PluginOutput(data={"url": url})
