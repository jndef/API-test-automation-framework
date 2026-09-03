from config.stages import get_stage

STAGE = get_stage()
SERVICE_USERS_URL = "/api/users"
SERVICE_FOLLOWS_URL = "/api/follows"


class Endpoints:
    follow_user = lambda self, username: f"{STAGE}{SERVICE_USERS_URL}/{username}/follow"
    unfollow_user = lambda self, username: f"{STAGE}{SERVICE_USERS_URL}/{username}/follow"
    get_follow_req = f"{STAGE}{SERVICE_FOLLOWS_URL}/requests"
    accept_follow_req = lambda self, follow_id: f"{STAGE}{SERVICE_FOLLOWS_URL}/requests/{follow_id}/accept"
    reject_follow_req = lambda self, follow_id: f"{STAGE}{SERVICE_FOLLOWS_URL}/requests/{follow_id}/reject"
