from config.stages import get_stage

STAGE = get_stage()
SERVICE_URL = "/api/auth"

class Endpoints:

    register_account = f"{STAGE}{SERVICE_URL}/register"
    login_account = f"{STAGE}{SERVICE_URL}/login"
    refresh = f"{STAGE}{SERVICE_URL}/refresh"
    logout = f"{STAGE}{SERVICE_URL}/logout"
    get_me = f"{STAGE}{SERVICE_URL}/me"

