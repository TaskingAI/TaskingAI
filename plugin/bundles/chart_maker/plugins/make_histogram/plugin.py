from typing import List

import base64
from app.service.image_storage import save_base64_image_to_s3_or_local

from bundle_dependency import *
import plotly.express as px

from config import CONFIG


class MakeHistogram(PluginHandler):
    async def execute(self, credentials: BundleCredentials, plugin_input: PluginInput) -> PluginOutput:
        values: List[str] = plugin_input.input_params.get("values")
        title: str = plugin_input.input_params.get("title", "Histogram")
        x_title: str = plugin_input.input_params.get("x_title", "x")

        project_id: str = plugin_input.project_id

        if not project_id:
            raise_http_error(ErrorCode.REQUEST_VALIDATION_ERROR, "project_id is required")

        fig = px.histogram(x=values, title=title, labels={"x": x_title})
        bytes_fig = fig.to_image(format="png")
        # convert image bytes to base64 string
        base_64_fig = base64.b64encode(bytes_fig).decode("utf-8")

        url = await save_base64_image_to_s3_or_local(
            base_64_fig, project_id, "png", "chart_maker/make_histogram"
        )

        return PluginOutput(data={"url": url})
