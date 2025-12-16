import re
from apps.notifications.models import NotificationTemplate, ApiNotification

class NotificationService:
    def __init__(self):
        pass


    def notification_contents(self, template, payload):
        """
        Populate the template with dynamic data from the payload.
        """
        content = template
        for key, value in payload.items():
            content = re.sub(
                rf"{{{{\s*{key}\s*}}}}",
                str(value),
                content,
            )
        return content

    def api_notification(self):
        pass
        



