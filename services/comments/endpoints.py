from config.stages import get_stage

STAGE = get_stage()
SERVICE_POSTS_URL = "/api/posts"
SERVICE_COMMENTS_URL = "/api/comments"


class Endpoints:
    get_list_comments = lambda self, post_id: f"{STAGE}{SERVICE_POSTS_URL}/{post_id}/comments"
    create_comment = lambda self, post_id: f"{STAGE}{SERVICE_POSTS_URL}/{post_id}/comments"
    update_comment = lambda self, comment_id: f"{STAGE}{SERVICE_COMMENTS_URL}/{comment_id}"
    delete_comment = lambda self, comment_id: f"{STAGE}{SERVICE_COMMENTS_URL}/{comment_id}"
    get_list_replies = lambda self, comment_id: f"{STAGE}{SERVICE_COMMENTS_URL}/{comment_id}/replies"
    create_reply = lambda self, comment_id: f"{STAGE}{SERVICE_COMMENTS_URL}/{comment_id}/replies"
