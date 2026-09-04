from config.stages import get_stage

STAGE = get_stage()
SERVICE_NOTIFICATIONS_URL = "/api/notifications"


class Endpoints:
    get_notifications = f"{STAGE}{SERVICE_NOTIFICATIONS_URL}"
    get_unread_count = f"{STAGE}{SERVICE_NOTIFICATIONS_URL}/unread-count"
    mark_read = lambda self, notification_id: f"{STAGE}{SERVICE_NOTIFICATIONS_URL}/{notification_id}/read"
    mark_read_all = f"{STAGE}{SERVICE_NOTIFICATIONS_URL}/read-all"
