from config.stages import get_stage

STAGE = get_stage()
SERVICE_ADMIN_URL = "/api/admin"


class Endpoints:
    get_stats = f"{STAGE}{SERVICE_ADMIN_URL}/stats"
    get_list_users_all = lambda self, search_query: f"{STAGE}{SERVICE_ADMIN_URL}/users{"?q=" + search_query if search_query else ""}"
    update_user_by_admin = lambda self, user_id: f"{STAGE}{SERVICE_ADMIN_URL}/users/{user_id}"
    deactivate_user_by_admin = lambda self, user_id: f"{STAGE}{SERVICE_ADMIN_URL}/users/{user_id}"
    get_list_posts_all = f"{STAGE}{SERVICE_ADMIN_URL}/posts"
    remove_post_by_admin = lambda self, post_id: f"{STAGE}{SERVICE_ADMIN_URL}/posts/{post_id}"
