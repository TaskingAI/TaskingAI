import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from bundle_dependency import *


class SendEmail(PluginHandler):
    async def execute(
        self, credentials: BundleCredentials, execution_config, plugin_input: PluginInput
    ) -> PluginOutput:
        smtp_server = execution_config.get("smtp_server")
        smtp_port = execution_config.get("smtp_port")
        smtp_username = execution_config.get("smtp_username")
        smtp_password = execution_config.get("smtp_password")

        body = plugin_input.input_params.get("body")
        recipient_email = plugin_input.input_params.get("recipient_email")
        subject = plugin_input.input_params.get("subject")

        msg = MIMEMultipart()
        msg["From"] = smtp_username
        msg["To"] = recipient_email
        msg["Subject"] = subject

        msg.attach(MIMEText(body, "plain"))

        try:
            with smtplib.SMTP(smtp_server, smtp_port, local_hostname="localhost") as server:
                server.set_debuglevel(1)
                server.starttls()
                server.login(smtp_username, smtp_password)
                text = msg.as_string()
                server.sendmail(smtp_username, recipient_email, text)
            return PluginOutput(data={"result": f"Email successfully sent to {recipient_email}"})
        except Exception as e:
            return PluginOutput(data={"result": f"Error sending email: {e}"})
