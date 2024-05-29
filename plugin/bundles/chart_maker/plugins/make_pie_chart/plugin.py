from typing import List

import base64
from app.service.image_storage import save_base64_image_to_s3_or_local

from bundle_dependency import *
import plotly.express as px

from config import CONFIG


class MakePieChart(PluginHandler):
    async def execute(self, credentials: BundleCredentials, plugin_input: PluginInput) -> PluginOutput:
        labels: List[str] = plugin_input.input_params.get("labels")
        values: List[float] = plugin_input.input_params.get("values")
        title: str = plugin_input.input_params.get("title", "Pie Chart")

        project_id: str = plugin_input.project_id

        if not project_id:
            raise_http_error(ErrorCode.REQUEST_VALIDATION_ERROR, "project_id is required")

        if len(labels) != len(values):
            raise_http_error(ErrorCode.REQUEST_VALIDATION_ERROR, "Number of labels and values do not match")

        fig = px.pie(names=labels, values=values, title=title)
        bytes_fig = fig.to_image(format="png")
        # convert image bytes to base64 string
        base_64_fig = base64.b64encode(bytes_fig).decode("utf-8")

        url = await save_base64_image_to_s3_or_local(
            base_64_fig, project_id, "png", "chart_maker/make_pie_chart"
        )

        return PluginOutput(data={"url": url})