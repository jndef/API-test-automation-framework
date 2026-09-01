from config.stages import get_stage

STAGE = get_stage()
SERVICE_POSTS_URL = "/api/upload"

class Endpoints:
    upload_image = f"{STAGE}{SERVICE_POSTS_URL}/image"
