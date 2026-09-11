from config.stages import get_stage

STAGE = get_stage()
SERVICE_POSTS_URL = "/api/posts"
SERVICE_BOOKMARK_URL = "/api/bookmarks"


class Endpoints:
    get_bookmarks_list = f"{STAGE}{SERVICE_BOOKMARK_URL}"
    bookmark_post = lambda self, post_id: f"{STAGE}{SERVICE_POSTS_URL}/{post_id}/bookmark"
    unbookmark_post = lambda self, post_id: f"{STAGE}{SERVICE_POSTS_URL}/{post_id}/bookmark"
