import base64
from io import BytesIO

from app.service.image_storage import save_base64_image_to_s3_or_local
from bundle_dependency import *
import qrcode

from config import CONFIG


class GenerateQrCode(PluginHandler):
    async def execute(self, credentials: BundleCredentials, plugin_input: PluginInput) -> PluginOutput:
        text: str = plugin_input.input_params.get("text")
        img = qrcode.make(text)

        project_id: str = plugin_input.project_id

        if not project_id:
            raise_http_error(ErrorCode.REQUEST_VALIDATION_ERROR, "project_id is required")

        # get base64 string of the image
        image_bytes = None

        with BytesIO() as output:
            img.save(output, format="PNG")
            image_bytes = output.getvalue()

        base_64_fig = base64.b64encode(image_bytes).decode("utf-8")

        url = await save_base64_image_to_s3_or_local(
            base_64_fig, project_id, "png", "qr_code_generator/generate_qr_code"
        )

        return PluginOutput(data={"url": url})
