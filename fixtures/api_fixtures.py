import random
from dataclasses import dataclass

import allure
import pytest

from auth.credentials import Credentials
from services.comments.payloads import  CreateCommentPayload
from services.likes.payloads import LikePostPayload
from services.messages.payloads import CreateMessagePayload
from services.posts.params import GetPostsParams
from services.posts.payloads import CreatePostPayload
from utils.data_helper import DataHelper
from auth.role_factory import MultiRoleServiceFactory, ServiceContainer

creds = Credentials()


@dataclass
class UserInfo:
    role: str
    user_id: str
    is_verified: bool
    is_active: bool
    email:str=None
    password:str=None


@pytest.fixture()
@allure.title("API Fixture: Get fist matched post with likes (post_id)")
def get_post_with_likes():
    """
    API Fixture: Get fist matched post with likes (performs by certain user - by alias)
    :return: post_id
    """

    def get_posts_with_likes(post_service) -> str:
        params = GetPostsParams(sort_by="likes_count")
        post = post_service.get_list_posts(params=params).items[0]
        return post.id

    yield get_posts_with_likes


@pytest.fixture(scope="session")
@allure.title("API Fixture: Setup - Build general multi services factory")
def get_service_by_role():
    """
    Fixture. Setup - build general multi services factory for specified user (by alias)
    :return:
    """
    factory = MultiRoleServiceFactory()

    def _get_service_container_for_user(role):
        return factory.get_services(role)

    return _get_service_container_for_user


def _get_posts_list_for_user(users_post_service) -> list[dict]:
    """
    Method, returned posts lists
    :param users_post_service: provided post service of certain user
    :return: List of objets (posts) -> list[dict]
    """
    posts_list_response = users_post_service.get_list_posts()
    return posts_list_response.items


def _get_username_by_role(get_service_by_role, services_for_role: str) -> str:
    """
    Returned username of certain user
    :param get_service_by_role: list of prepared api_clients
    :param services_for_role: user's alias used to retrieve desired api_client
    :return: Username as str
    """
    user_auth_service = get_service_by_role(services_for_role).auth_api
    get_me_response = user_auth_service.get_me()
    return get_me_response.username


@pytest.fixture()
@allure.title("API Fixture: Setup - Build general multi services factory")
def build_conversation(get_service_by_role, db_get_conversation, db_get_username):
    """
    API & DB fixture: Prepared conversation between users by provided aliases before test (performs by certain user - by alias). If conversation exists, returns it.
    Else - create new conversation
    :param get_service_by_role: api client for fixture
    :param db_get_conversation: db fixture, used to check if conversation exists
    :param db_get_username: db fixture, to retrieve username. Requires to initiate conversation
    :return: id of conversation
    """

    def _build(role: str, participant_role: str) -> str:
        existed_conversation = db_get_conversation(role, participant_role)
        if existed_conversation is not None:
            return existed_conversation
        messages_service = get_service_by_role(role).messages_api
        participant_username = db_get_username(participant_role)
        conversation = messages_service.find_or_create_dm(participant_username)
        return conversation.id

    yield _build  # test get build function


@pytest.fixture()
@allure.title("API & DB fixture: create message before test at certain conversation")
def build_message(get_service_by_role, db_get_rand_user_conversation):
    """
    Build message at any existed conversation for user with provided alias
    :param get_service_by_role:
    :param db_get_rand_user_conversation: retrieves existed user's conversations, picks any from list
    :return: Created message id as string
    """

    def _build(role: str) -> str:
        message_service = get_service_by_role(role).messages_api
        payload = CreateMessagePayload(content="M")
        conversation = db_get_rand_user_conversation(role)
        message = message_service.send_message(conversation_id=conversation, payload=payload)
        return message.id

    yield _build


@pytest.fixture()
@allure.title("API fixture: create message before test at certain conversation")
def build_message_remove_at_certain_conversation(get_service_by_role):
    """
    API Fixture: Creates a message before test, add to list of messages for removing after test (performs by certain user - by alias), return message id at test. After test - removes all messages added to list
    :param get_service_by_role: api_client of user. Requires to provide user alias to perform actions by certain user
    :return:
    """
    created_messages: list[tuple] = []

    def _build(role: str, conversation: str) -> str:
        message_service = get_service_by_role(role).messages_api
        payload = CreateMessagePayload(content="M")
        message = message_service.send_message(conversation_id=conversation, payload=payload)
        created_messages.append((role, message.id))
        return message.id

    yield _build
    for role, message_id in reversed(created_messages):
        get_service_by_role(role).messages_api.remove_message(message_id)


@pytest.fixture()
@allure.title("API fixture: create message before test at certain conversation")
def build_message_at_certain_conversation(get_service_by_role):
    """
    API Fixture. Creates a message by certain user (by provided alias) before test (performs by certain user - by alias)
    :param get_service_by_role: api client, used to perform actions by certain user
    :return: created message id
    """

    def _build(role: str, conversation: str) -> str:
        data_helper = DataHelper()
        message_service = get_service_by_role(role).messages_api
        payload = CreateMessagePayload(content=data_helper.generate_text(max_len=20))
        message = message_service.send_message(conversation_id=conversation, payload=payload)
        return message.id

    yield _build


@pytest.fixture()
@allure.title("API & DB fixture: creates message at certain conversation and removes it before test")
def get_removed_message(get_service_by_role, db_get_rand_user_conversation):
    """
    API & DB Fixture - creates message at certain conversation and removes it before test (performs by certain user - by alias)
    :param get_service_by_role: api client, used to perform actions by certain user
    :param db_get_rand_user_conversation: retrieves existed user's conversations, picks any from list
    :return: Returns id of removed message
    """

    def _build(role: str):
        data_helper = DataHelper()
        message_service = get_service_by_role(role).messages_api
        payload = CreateMessagePayload(content=data_helper.generate_text(max_len=20))
        conversation = db_get_rand_user_conversation(role)
        message = message_service.send_message(conversation_id=conversation, payload=payload)
        message_service.remove_message(message.id)
        return message.id

    yield _build


@pytest.fixture()
@allure.title("API fixture: adding avatar to profile")
def add_avatar_to_profile(get_service_by_role):
    """
    API Fixture. Upload avatar for user by provided alias before test (performs by certain user - by alias)
    :param get_service_by_role: api client, used to perform actions by certain user
    :return:
    """

    def _add_avatar(role: str):
        user_service = get_service_by_role(role).users_api
        user_service.update_profile_avatar(image_name="image.png")

    yield _add_avatar


@pytest.fixture()
@allure.title("API fixture: creates post and removes it before test")
def build_post_remove(get_service_by_role):
    """
    API Fixture. Creates post and removes it before test (performs by certain user - by alias). Returns id of removed post
    :param get_service_by_role: api client, used to perform actions by certain user
    :return: Returns id of removed post
    """
    created_posts: list[tuple] = []

    def _build(role: str) -> str:
        data_helper = DataHelper()
        post_service = get_service_by_role(role).posts_api
        payload = CreatePostPayload(content=data_helper.generate_text(50))

        post = post_service.create_post(payload)
        created_posts.append((role, post.id))
        return post.id

    yield _build

    for role, post_id in reversed(created_posts):
        get_service_by_role(role).posts_api.delete_post(post_id)


@pytest.fixture()
@allure.title("API Fixture: creates follow request before test, returns follow request at test and removes it after")
def create_follow_request_remove(get_service_by_role):
    """
    API Fixture -  creates follow request before test (performs by certain user - by alias), returns follow request at test and removes it after
    :param get_service_by_role: api client, used to perform actions by certain user
    :return:
    """
    follow_users: list[tuple] = []

    def _follow(role: str, user_name: str):
        follow_service = get_service_by_role(role).follows_api
        follow_service.follow_user(user_name)
        follow_users.append((role, user_name))

    yield _follow

    for role, user_name in reversed(follow_users):
        get_service_by_role(role).follows_api.unfollow_user(user_name)


@pytest.fixture()
@allure.title("API Fixture - creates follow request before test, returns follow request id")
def get_follow_request(get_service_by_role):
    """
    API Fixture. Creates follow request for user by provided alias before test (performs by certain user - by alias)
    :param get_service_by_role: api client, used to perform actions by certain user
    :return:
    """

    def _follow(role: str, user_name: str) -> str:
        follow_service = get_service_by_role(role).follows_api
        follow = follow_service.follow_user(user_name)
        return follow.id

    yield _follow


@pytest.fixture()
@allure.title("API Fixture - creates post and pins it before test, removes it after test")
def build_post_pin_remove(get_service_by_role):
    """
    API Fixture. Creates post and pins it before test (performs by certain user - by alias), removes it after test
    :param get_service_by_role: api client, used to perform actions by certain user
    :return:
    """
    created_posts: list[tuple] = []

    def _build(role: str) -> str:
        post_service = get_service_by_role(role).posts_api
        data_helper = DataHelper()
        payload = CreatePostPayload(content=data_helper.generate_text(50))
        post = post_service.create_post(payload)
        post_service.pin_post(post.id)
        created_posts.append((role, post.id))
        return post.id

    yield _build  # test gets build function

    for role, post_id in reversed(created_posts):
        get_service_by_role(role).posts_api.delete_post(post_id)


@pytest.fixture()
@allure.title("API Fixture - creates post and bookmarks it before test, removes it after test")
def build_post_bookmark_remove(get_service_by_role):
    """
    Creates post and bookmarks it before test (performs by certain user - by alias), removes it after test
    :param get_service_by_role: api client, used to perform actions by certain user
    :return:
    """
    created_posts: list[tuple] = []

    def _build(role: str):
        api_client = get_service_by_role(role)
        post_service = api_client.posts_api
        bookmark_service = api_client.bookmarks_api
        data_helper = DataHelper()
        payload = CreatePostPayload(content=data_helper.generate_text(50))

        post = post_service.create_post(payload)
        bookmark_service.bookmark_post(post.id)
        created_posts.append((role, post.id))
        return post.id

    yield _build  # test gets build function

    for role, post_id in reversed(created_posts):
        get_service_by_role(role).posts_api.delete_post(post_id)


@pytest.fixture()
@allure.title("API Fixture - creates post and likes it before test, removes it after test")
def build_post_like_remove(get_service_by_role):
    """
    API Fixture - creates post and likes it before test, returns post_id to test and removes post after test (performs by certain user - by alias)
    :param get_service_by_role: api client, used to perform actions by certain user
    :return:
    """
    created_posts: list[tuple] = []

    def _build(role: str, reaction: str = "like") -> str:
        app_services = get_service_by_role(role)
        data_helper = DataHelper()
        post_service = app_services.posts_api
        post_payload = CreatePostPayload(content=data_helper.generate_text(50))
        post = post_service.create_post(post_payload)

        like_service = app_services.likes_api
        like_payload = LikePostPayload(reaction=reaction)
        like_service.like_post(post.id, payload=like_payload)
        created_posts.append((role, post.id))
        return post.id

    yield _build

    for role, post_id in reversed(created_posts):
        get_service_by_role(role).posts_api.delete_post(post_id)


@pytest.fixture()
@allure.title(
    "API Fixture - creates comment at random post, likes it before test, returns comment_id at test and removes comment after test")
def build_comment_like_remove(get_service_by_role):
    """
    API Fixture - creates comment at random post, likes it before test, returns comment_id at test and removes comment after test (performs by certain user - by alias)
    :param get_service_by_role: api client, used to perform actions by certain user
    :return:
    """
    created_comments: list[tuple] = []

    def _build(role: str, reaction: str = "like") -> str:
        app_services = get_service_by_role(role)
        data_helper = DataHelper()

        post_service = app_services.posts_api
        comment_service = app_services.comments_api
        like_service = app_services.likes_api

        post = random.choice(_get_posts_list_for_user(post_service))
        comment = comment_service.create_comment(post.id,
                                                 payload=CreateCommentPayload(content=data_helper.generate_text(25)))
        like_service.like_comment(comment.id, payload=LikePostPayload(reaction=reaction))
        created_comments.append((role, comment.id))
        return comment.id

    yield _build

    for role, comment_id in reversed(created_comments):
        get_service_by_role(role).comments_api.delete_comment(comment_id)


@pytest.fixture()
@allure.title("API Fixture - creates new post and removes it, returns post_id at test")
def get_removed_post(get_service_by_role):
    """
    API Fixture - creates new post and removes it, returns post_id at test (performs by certain user - by alias)
    :param get_service_by_role: api client, used to perform actions by certain user
    :return:
    """

    def _remove_post_by(role: str) -> str:
        data_helper = DataHelper()
        post_service = get_service_by_role(role).posts_api
        post = post_service.create_post(CreatePostPayload(content=data_helper.generate_text(25)))
        post_service.delete_post(post.id)
        return post.id

    yield _remove_post_by


@pytest.fixture()
@allure.title("API Fixture - creates new post, bookmarks and removes it, returns post_id at test")
def get_removed_bookmarked_post(get_service_by_role):
    """
    API Fixture - creates new post, bookmarks and removes it, returns post_id at test (performs by certain user - by alias)
    :param get_service_by_role: api client, used to perform actions by certain user
    :return:
    """

    def _remove_post_by(role: str) -> str:
        data_helper = DataHelper()
        api_client = get_service_by_role(role)
        post_service = api_client.posts_api
        bookmark_service = api_client.bookmarks_api

        post = post_service.create_post(CreatePostPayload(content=data_helper.generate_text(25)))
        bookmark_service.bookmark_post(post.id)
        post_service.delete_post(post.id)
        return post.id

    yield _remove_post_by


@pytest.fixture()
@allure.title("API Fixture - creates new post returns post_id at test")
def create_and_get_post(get_service_by_role):
    """
    API Fixture - creates new post returns post_id at test (performs by certain user - by alias)
    :param get_service_by_role: api client, used to perform actions by certain user
    :return:
    """

    def _create(role: str) -> str:
        data_helper = DataHelper()
        post_service = get_service_by_role(role).posts_api
        post = post_service.create_post(payload=CreatePostPayload(content=data_helper.generate_text(25)))
        return post.id

    yield _create


@pytest.fixture()
@allure.title("API Fixture - creates new comment at random post, returns post_id at test and remove it after test")
def build_comment_remove(get_service_by_role):
    """
    API Fixture - creates new comment at random post, returns post_id at test and remove it after test (performs by certain user - by alias)
    :param get_service_by_role: api client, used to perform actions by certain user
    :return:
    """
    created_comments: list[tuple] = []

    def _build_comment(role: str) -> str:
        data_helper = DataHelper()
        app_services: ServiceContainer = get_service_by_role(role)
        payload = CreateCommentPayload(content=data_helper.generate_text(25))
        posts: list[dict] = _get_posts_list_for_user(app_services.posts_api)
        comment = app_services.comments_api.create_comment(post_id=(random.choice(posts)).id, payload=payload)
        created_comments.append((role, comment.id))
        return comment.id

    yield _build_comment  # тест получает функцию регистрации

    for role, comment_id in reversed(created_comments):
        get_service_by_role(role).comments_api.delete_comment(comment_id)


@pytest.fixture()
@allure.title("API Fixture - creates new comment at random post, returns post_id at test")
def create_and_get_comment(get_service_by_role):
    """
    API Fixture - creates new comment at random post, returns post_id at test (performs by certain user - by alias)
    :param get_service_by_role: api client, used to perform actions by certain user
    :return:
    """

    def _create_comment(role: str) -> str:
        data_helper = DataHelper()
        app_services: ServiceContainer = get_service_by_role(role)
        payload = CreateCommentPayload(content=data_helper.generate_text(25))
        posts: list[dict] = _get_posts_list_for_user(app_services.posts_api)
        comment = app_services.comments_api.create_comment(post_id=random.choice(posts).id, payload=payload)
        return comment.id

    yield _create_comment


@pytest.fixture()
@allure.title("API Fixture - creates new comment at random post, removes it and returns post_id at test")
def get_removed_comment(get_service_by_role):
    """
    API Fixture - creates new comment at random post, removes it and returns post_id at test (performs by certain user - by alias)
    :param get_service_by_role: api client, used to perform actions by certain user
    :return:
    """

    def _remove_comment_by(role: str) -> str:
        data_helper = DataHelper()
        app_services: ServiceContainer = get_service_by_role(role)
        posts: list[dict] = _get_posts_list_for_user(app_services.posts_api)

        payload = CreateCommentPayload(content=data_helper.generate_text(25))
        comment = app_services.comments_api.create_comment(random.choice(posts).id, payload)
        app_services.comments_api.delete_comment(comment.id)
        return comment.id

    yield _remove_comment_by


@pytest.fixture()
@allure.title("API Fixture. Clean (remove) comment after test")
def comment_cleaner(get_service_by_role):
    """
    API Fixture. Clean (remove) comment after test (performs by certain user - by alias)
    :param get_service_by_role: api client, used to perform actions by certain user
    :return:
    """
    created_ids = []

    def _register(comment_id, role="user_eve"):
        created_ids.append((comment_id, role))

    yield _register  # test gets register function

    for comment_id, role in created_ids:  # cleanup all that was registered
        get_service_by_role(role).comments_api.delete_comment(comment_id)


@pytest.fixture()
@allure.title("API Fixture. Clean (remove) message after test")
def message_cleaner(get_service_by_role):
    """
    API Fixture. Clean (remove) message after test (performs by certain user - by alias)
    :param get_service_by_role: api client, used to perform actions by certain user
    :return:
    """
    created_ids = []

    def _register(message_id: str, role: str):
        created_ids.append((message_id, role))

    yield _register

    for message_id, role in created_ids:  # cleanup всего что зарегистрировано
        get_service_by_role(role).messages_api.remove_message(message_id)


# @pytest.fixture()
# @allure.title("API Fixture - pins created post, returns post_id at test ")
# def create_pin_and_get_post(get_service_by_role, create_and_get_post):
#     """
#     API Fixture - pins created post, returns post_id at test (performs by certain user - by alias)
#     :param get_service_by_role: api client, used to perform actions by certain user
#     :param create_and_get_post: API fixture, creates new post returns post_id at test
#     :return:
#     """
#     def _pin(role:str) -> str:
#         created_post_id:str = create_and_get_post(role)
#         post_service = get_service_by_role(role).posts_api
#         post_service.pin_post(created_post_id)
#         return created_post_id
#     yield _pin


@pytest.fixture()
@allure.title("API Fixture - API fixture, returns post, created later than 15 minutes")
def get_expired_to_edit_post(get_service_by_role):
    """
    API fixture, returns post, created later than 15 minutes (performs by certain user - by alias)
    :param get_service_by_role: api client, used to perform actions by certain user
    :return:
    """

    def _get_expired_post(role: str) -> str:
        data_helper = DataHelper()
        app_services = get_service_by_role(role)
        json_posts = _get_posts_list_for_user(app_services.posts_api)
        own_username = _get_username_by_role(get_service_by_role, role)
        post_id = data_helper.find_not_recent_post(json_posts, own_username)
        if post_id is None:
            raise BaseException(
                f"Error on setup. Failed to find post matched to requirements (created later than 15 minutes) for user ({role})")
        return post_id

    yield _get_expired_post


@pytest.fixture()
@allure.title("API Fixture. Clean (remove) post after test")
def post_cleaner(get_service_by_role):
    """
    API fixture. Remove added post after test (performs by certain user - by alias)
    :param get_service_by_role: api client, used to perform actions by certain user
    :return:
    """
    created_ids = []

    def _register(post_id: str, role: str):
        created_ids.append((post_id, role))

    yield _register  # test gets register function, result of launch

    for post_id, role in created_ids:  # cleanup all that registered
        get_service_by_role(role).posts_api.delete_post(post_id)


@pytest.fixture()
@allure.title("API Fixture. Clean (remove) follow request after test")
def follow_request_cleaner(get_service_by_role):
    """
    API Fixture. Clean (remove) follow request after test (performs by certain user - by alias)
    :param get_service_by_role: api client, used to perform actions by certain user
    :return:
    """
    created_ids = []

    def _register(user_name: str, role: str):
        created_ids.append((user_name, role))

    yield _register  # test gets register function, result of launch
    for user_name, role in created_ids:  # # cleanup all that registered
        get_service_by_role(role).follows_api.unfollow_user(user_name)


@pytest.fixture()
@allure.title("API Fixture. Gets certain info about user and returns it to test")
def get_me_of_certain_user(get_service_by_role):
    """
    API fixture. Request account general info by certain user (performs by certain user - by alias). Returns specified info about user
    :param get_service_by_role: api client, used to perform actions by certain user
    :return:
    """

    def _ger_user_info(role: str) -> UserInfo:
        api_services = get_service_by_role(role)
        user_info = api_services.auth_api.get_me()
        return UserInfo(
            role=user_info.role,
            is_verified=user_info.is_verified,
            is_active=user_info.is_active,
            user_id=user_info.id)

    yield _ger_user_info


@pytest.fixture()
@allure.title("API Fixture. Register new user for test")
def register_new_account(get_service_by_role):
    """
    API Fixture. Register new user for test (performs using 'public' client, not required access token)
    :param get_service_by_role: api client, used to perform actions by certain user
    :return:
    """
    guest_service = get_service_by_role(None)
    data_helper = DataHelper()
    payload = data_helper.get_random_register_account_payload()
    created_user = guest_service.auth_api.register(payload)
    yield UserInfo(
        role=created_user.role,
        is_verified=created_user.is_verified,
        is_active=created_user.is_active,
        user_id=created_user.id)


@pytest.fixture()
@allure.title("API Fixture. Register new user for test")
def register_remove_new_account(get_service_by_role):
    """
    API Fixture. Registers new user for test, returns certain info about new user to test (performs using 'public' client, not required access token)
    and deactivate it after by admin
    :param get_service_by_role: api client, used to perform actions by certain user
    :return:
    """
    created_ids = []

    def _create() -> UserInfo:
        guest_service = get_service_by_role(None)
        data_helper = DataHelper()
        payload = data_helper.get_random_register_account_payload()
        created_user = guest_service.auth_api.register(payload)
        created_ids.append(created_user.id)
        user_data = UserInfo(
            role=created_user.role,
            is_verified=created_user.is_verified,
            is_active=created_user.is_active,
            user_id=created_user.id)
        return user_data

    yield _create
    admin_service = get_service_by_role("admin").admin_api
    for user_id in created_ids:
        admin_service.deactivate_user_by_admin(user_id)


@pytest.fixture()
@allure.title("API Fixture. Clean (deactivate) account after test")
def account_cleaner(get_service_by_role):
    """
    API Fixture. Clean (deactivate) account after test by admin using provided id of created user
    :param get_service_by_role: api client, used to perform actions by admin
    :return:
    """
    created_ids = []

    def _register(user_id: str):
        created_ids.append(user_id)

    yield _register  # test gets register function, result of launch
    for user_id in created_ids:  # # cleanup all that registered
        get_service_by_role("admin").admin_api.deactivate_user_by_admin(user_id)

@pytest.fixture()
@allure.title("API Fixture. Get deactivated account for test")
def register_remove_new_account(get_service_by_role):
    """
    API Fixture. Register new user (performs using 'public' client, not required access token) and deactivate it by admin. Return user's info for test
    :param get_service_by_role: api client, used to perform actions by certain user
    :return:
    """
    guest_service = get_service_by_role(None)
    data_helper = DataHelper()
    payload = data_helper.get_random_register_account_payload()
    created_user = guest_service.auth_api.register(payload)
    admin_service = get_service_by_role("admin").admin_api
    admin_service.deactivate_user_by_admin(created_user.id)
    yield UserInfo(
        role=created_user.role,
        is_verified=created_user.is_verified,
        is_active=created_user.is_active,
        user_id=created_user.id,
        email=created_user.email,
        password=payload.password)
