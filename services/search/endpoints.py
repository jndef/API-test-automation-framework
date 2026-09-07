from config.stages import get_stage

STAGE = get_stage()
SERVICE_SEARCH_URL = "/api/search"


class Endpoints:
    search_users = lambda self, search_query: f"{STAGE}{SERVICE_SEARCH_URL}/users{"?q="+search_query if search_query else ""}"
    search_posts = lambda self, search_query: f"{STAGE}{SERVICE_SEARCH_URL}/posts{"?q="+search_query if search_query else ""}"
    search_hashtags = lambda self, search_query: f"{STAGE}{SERVICE_SEARCH_URL}/hashtags{"?q="+search_query if search_query else ""}"
    search_trending = f"{STAGE}{SERVICE_SEARCH_URL}/trending/hashtags"
