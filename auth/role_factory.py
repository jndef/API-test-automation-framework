from config.headers import Headers
from auth.token_provider import TokenProvider
from services.auth.api import AuthAPI
from services.bookmarks.api import BookmarksAPI
from services.comments.api import CommentsAPI
from services.follows.api import FollowsAPI
from services.likes.api import LikesAPI
from services.messages.api import MessagesAPI
from services.notifications.api import NotificationsAPI
from services.posts.api import PostsAPI
from services.upload.api import UploadsAPI
from services.users.api import UsersAPI


class ServiceContainer:
    def __init__(self):
        self.auth_api = AuthAPI()
        self.users_api = UsersAPI()
        self.follows_api = FollowsAPI()
        self.posts_api = PostsAPI()
        self.comments_api = CommentsAPI()
        self.likes_api = LikesAPI()
        self.bookmarks_api = BookmarksAPI()
        self.messages_api = MessagesAPI()
        self.upload_api = UploadsAPI()
        self.notifications_api = NotificationsAPI()

class MultiRoleServiceFactory:

    def __init__(self):
        self._cache = {}

    def _get_headers_for_role(self, role:str=None):
        headers = Headers()

        if role is not None:
            token = TokenProvider().get_token_for_role(role)
            headers.basic = {"Authorization": f"Bearer {token}"}
        return headers




    def get_services(self, role: str = None) -> ServiceContainer:
        # role=None — публичные эндпоинты, без токена

        if role in self._cache:
            return self._cache[role]

        headers = self._get_headers_for_role(role)
        services_apis = {
            "auth_api": AuthAPI(),
            "users_api": UsersAPI(),
            "follows_api": FollowsAPI(),
            "posts_api" : PostsAPI(),
            "comments_api" : CommentsAPI(),
            "likes_api": LikesAPI(),
            "bookmarks_api": BookmarksAPI(),
            "messages_api": MessagesAPI(),
            "upload_api": UploadsAPI(),
            "notifications_api": NotificationsAPI()
            # More api_serives
        }
        if role is None:
            services_apis = {
                "auth_api": AuthAPI(),
            }

        for api in services_apis.values():
            api.headers = headers

        services = ServiceContainer()

        for name, api in services_apis.items():
            setattr(services, name, api)

        self._cache[role] = services

        return services
