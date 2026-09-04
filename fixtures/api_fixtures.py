import random

import allure
import pytest
from faker import Faker

from auth.credentials import Credentials
from services.comments.payloads import CreateCommentBody, CreateCommentPayloadQuery
from services.likes.payloads import LikePostPayload
from services.messages.payloads import CreateMessagePayload
from services.posts.params import GetPostsParams
from services.posts.payloads import CreatePostPayload
from utils.data_helper import DataHelper as data_helper
from auth.role_factory import MultiRoleServiceFactory, ServiceContainer

fake = Faker()
creds = Credentials()


@pytest.fixture()
def get_post_with_likes():
    def get_posts_with_likes(post_service):
        params = GetPostsParams(sort_by="likes_count")
        post = post_service.get_list_posts(params=params).items[0]
        return post.id
    yield get_posts_with_likes

@pytest.fixture(scope="session")
@allure.title("Setup - Build general multi services factory")
def get_service_by_role():
    """
    Fixture. Setup - build general multi services factory for specified user (by alias)
    :return:
    """
    factory = MultiRoleServiceFactory()
    def _get_service_container_for_user(role):
        return factory.get_services(role)
    return _get_service_container_for_user

@pytest.fixture()
def get_not_existed_uuid() -> str:
    return fake.uuid4()

def _get_posts_list_for_user(users_post_service) -> list[dict]:
    posts_list_response = users_post_service.get_list_posts()
    return posts_list_response.items


def _get_username_by_role(get_service_by_role, services_for_role:str):
    user_auth_service = get_service_by_role(services_for_role).auth_api
    get_me_response = user_auth_service.get_me()
    return get_me_response.username


@pytest.fixture()
def create_remove_post_by_user(request, get_service_by_role):
    create_post_by:str = request.param
    post_service = get_service_by_role(create_post_by).posts_api
    payload=CreatePostPayload(content="B")

    post = post_service.create_post(payload)
    yield post.id
    post_service.delete_post(post.id)

@pytest.fixture()
def build_conversation(get_service_by_role, db_get_conversation, db_get_username):
    def _build(role:str, participant_role:str):
        existed_conversation = db_get_conversation(role, participant_role)
        if existed_conversation is not None:
            return existed_conversation
        messages_service = get_service_by_role(role).messages_api
        participant_username = db_get_username(participant_role)
        conversation = messages_service.find_or_create_dm(participant_username)
        return conversation.id
    yield _build  # тест получает функцию регистрации

@pytest.fixture()
def build_message(get_service_by_role, db_get_rand_user_conversation):
    def _build(role:str):
        message_service = get_service_by_role(role).messages_api
        payload = CreateMessagePayload(content="M")
        conversation = db_get_rand_user_conversation(role)
        message = message_service.send_message(conversation_id=conversation, payload=payload)
        return message.id
    yield _build

@pytest.fixture()
def build_message_remove_at_certain_conversation(get_service_by_role):
    created_messages:list[tuple] = []

    def _build(role:str, conversation:str):
        message_service = get_service_by_role(role).messages_api
        payload = CreateMessagePayload(content="M")
        message = message_service.send_message(conversation_id=conversation, payload=payload)
        created_messages.append((role, message.id))
        return message.id
    yield _build
    for role, message_id in reversed(created_messages):
        get_service_by_role(role).messages_api.remove_message(message_id)

@pytest.fixture()
def build_message_at_certain_conversation(get_service_by_role):
    def _build(role:str, conversation:str):
        message_service = get_service_by_role(role).messages_api
        payload = CreateMessagePayload(content=data_helper.generate_text(max_len=20))
        message = message_service.send_message(conversation_id=conversation, payload=payload)
        return message.id
    yield _build


@pytest.fixture()
def get_removed_message(get_service_by_role, db_get_rand_user_conversation):
    def _build(role:str):
        message_service = get_service_by_role(role).messages_api
        payload = CreateMessagePayload(content="M")
        conversation = db_get_rand_user_conversation(role)
        message = message_service.send_message(conversation_id=conversation, payload=payload)
        message_service.remove_message(message.id)
        return message.id
    yield _build

@pytest.fixture()
@allure.title("API fixture: init adding  avatar to profile")
def add_avatar_to_profile(get_service_by_role):
    """
    API Fixture. Upload avatar for user by provided alias
    :param get_service_by_role:
    :return:
    """
    def _add_avatar(role:str):
        user_service = get_service_by_role(role).users_api
        user_service.update_profile_avatar(image_name="image.png")
    yield _add_avatar


@pytest.fixture()
def build_post_remove(get_service_by_role):
    created_posts:list[tuple] = []

    def _build(role:str):
        post_service = get_service_by_role(role).posts_api
        payload = CreatePostPayload(content="B")

        post = post_service.create_post(payload)
        created_posts.append((role, post.id))
        return post.id
    yield _build  # тест получает функцию регистрации

    for role, post_id in reversed(created_posts):
        get_service_by_role(role).posts_api.delete_post(post_id)

@pytest.fixture()
@allure.title("API Fixture - create follow request before and remove after")
def create_follow_request_remove(get_service_by_role):
    """
    API Fixture - create follow request before and remove after
    :param get_service_by_role:
    :return:
    """
    follow_users:list[tuple]=[]
    def _follow(role, user_name:str):
        follow_service = get_service_by_role(role).follows_api
        follow_service.follow_user(user_name)
        follow_users.append((role, user_name))
    yield _follow  # тест получает функцию регистрации

    for role, user_name in reversed(follow_users):
        get_service_by_role(role).follows_api.unfollow_user(user_name)

@pytest.fixture()
@allure.title("API Fixture - create follow request before")
def get_follow_request(get_service_by_role):
    """
    API Fixture. Upload follow request for user by provided alias
    :param get_service_by_role:
    :return:
    """
    def _follow(role, user_name:str):
        follow_service = get_service_by_role(role).follows_api
        follow = follow_service.follow_user(user_name)
        return follow.id
    yield _follow  # тест получает функцию регистрации



@pytest.fixture()
def build_post_pin_remove(get_service_by_role):
    created_posts:list[tuple] = []

    def _build(role:str):
        post_service = get_service_by_role(role).posts_api
        payload = CreatePostPayload(content="B")

        post = post_service.create_post(payload)
        post_service.pin_post(post.id)
        created_posts.append((role, post.id))
        return post.id
    yield _build  # тест получает функцию регистрации

    for role, post_id in reversed(created_posts):
        get_service_by_role(role).posts_api.delete_post(post_id)

@pytest.fixture()
def build_post_bookmark_remove(get_service_by_role):
    created_posts:list[tuple] = []

    def _build(role:str):
        api_client = get_service_by_role(role)
        post_service = api_client.posts_api
        bookmark_service = api_client.bookmarks_api
        payload = CreatePostPayload(content="B")

        post = post_service.create_post(payload)
        bookmark_service.bookmark_post(post.id)
        created_posts.append((role, post.id))
        return post.id
    yield _build  # тест получает функцию регистрации

    for role, post_id in reversed(created_posts):
        get_service_by_role(role).posts_api.delete_post(post_id)

@pytest.fixture()
def build_post_like_remove(get_service_by_role):
    created_posts:list[tuple] = []

    def _build(role:str, reaction:str="like"):
        app_services = get_service_by_role(role)

        post_service = app_services.posts_api
        post_payload = CreatePostPayload(content="B")
        post = post_service.create_post(post_payload)

        like_service = app_services.likes_api
        like_payload = LikePostPayload(reaction=reaction)
        like_service.like_post(post.id, payload=like_payload)
        created_posts.append((role, post.id))
        return post.id
    yield _build  # тест получает функцию регистрации

    for role, post_id in reversed(created_posts):
        get_service_by_role(role).posts_api.delete_post(post_id)

@pytest.fixture()
def build_comment_like_remove(get_service_by_role):
    created_comments:list[tuple] = []

    def _build(role:str, reaction:str="like"):
        app_services = get_service_by_role(role)

        post_service = app_services.posts_api
        comment_service = app_services.comments_api
        like_service = app_services.likes_api

        comment_payload = CreateCommentPayloadQuery(content="B")
        like_payload = LikePostPayload(reaction=reaction)

        post = random.choice(_get_posts_list_for_user(post_service))
        comment = comment_service.create_comment(post.id, comment_payload)


        like_service.like_comment(comment.id, payload=like_payload)
        created_comments.append((role, comment.id))
        return comment.id
    yield _build  # тест получает функцию регистрации

    for role, comment_id in reversed(created_comments):
        get_service_by_role(role).comments_api.delete_comment(comment_id)



@pytest.fixture()
def get_removed_post(get_service_by_role):

    def _remove_post_by(role):
        post_service = get_service_by_role(role).posts_api
        payload = CreatePostPayload(content="B")

        post = post_service.create_post(payload)
        post_service.delete_post(post.id)
        return post.id

    yield _remove_post_by

@pytest.fixture()
def get_removed_bookmarked_post(get_service_by_role):

    def _remove_post_by(role):
        api_client = get_service_by_role(role)
        post_service = api_client.posts_api
        bookmark_service = api_client.bookmarks_api
        payload = CreatePostPayload(content="B")

        post = post_service.create_post(payload)
        bookmark_service.bookmark_post(post.id)
        post_service.delete_post(post.id)
        return post.id

    yield _remove_post_by

@pytest.fixture()
def create_and_get_post(get_service_by_role):
    def _create(role:str):
        post_service = get_service_by_role(role).posts_api
        payload = CreatePostPayload(content="B")

        post = post_service.create_post(payload)
        return post.id
    yield _create

@pytest.fixture()
def build_comment_remove(request, get_service_by_role):
    created_comments:list[tuple] = []

    def _build_comment(role:str):
        app_services:ServiceContainer = get_service_by_role(role)
        payload = CreateCommentBody(content="B")
        posts:list[dict] = _get_posts_list_for_user(app_services.posts_api)
        comment = app_services.comments_api.create_comment(post_id=(random.choice(posts)).id, payload=payload)
        created_comments.append((role, comment.id))
        return comment.id
    yield _build_comment  # тест получает функцию регистрации

    for role, comment_id in reversed(created_comments):
        get_service_by_role(role).comments_api.delete_comment(comment_id)

@pytest.fixture()
def create_and_get_comment(get_service_by_role):
    def _create_comment(role:str):
        app_services:ServiceContainer = get_service_by_role(role)
        payload = CreateCommentBody(content="B")
        posts:list[dict] = _get_posts_list_for_user(app_services.posts_api)
        comment = app_services.comments_api.create_comment(post_id=random.choice(posts).id, payload=payload)
        return comment.id
    yield _create_comment

@pytest.fixture()
def get_removed_comment(get_service_by_role):

    def _remove_comment_by(role):
        app_services:ServiceContainer = get_service_by_role(role)
        posts:list[dict] = _get_posts_list_for_user(app_services.posts_api)

        payload = CreateCommentBody(content="B")
        comment = app_services.comments_api.create_comment(random.choice(posts).id, payload)
        app_services.comments_api.delete_comment(comment.id)
        return comment.id

    yield _remove_comment_by

@pytest.fixture()
def comment_cleaner(get_service_by_role):
    created_ids = []

    def register(comment_id, role="user_eve"):
        created_ids.append((comment_id, role))

    yield register  # тест получает функцию регистрации

    for comment_id, role in created_ids:  # cleanup всего что зарегистрировано
        get_service_by_role(role).comments_api.delete_comment(comment_id)


@pytest.fixture()
def message_cleaner(get_service_by_role):
    created_ids = []

    def register(message_id, role:str):
        created_ids.append((message_id, role))

    yield register  # тест получает функцию регистрации

    for message_id, role in created_ids:  # cleanup всего что зарегистрировано
        get_service_by_role(role).messages_api.remove_message(message_id)

@pytest.fixture()
def create_pin_and_get_post(get_service_by_role, create_and_get_post):
    def _pin(role):
        created_post = create_and_get_post(role)
        post_service = get_service_by_role(role).posts_api
        post_service.pin_post(created_post)
        return created_post
    yield _pin



@pytest.fixture()
def get_expired_to_edit_post(get_service_by_role):
    def _get_expired_post(role:str):
        app_services = get_service_by_role(role)
        json_posts = _get_posts_list_for_user(app_services.posts_api)
        own_username = _get_username_by_role(get_service_by_role, role)
        post_id = data_helper.find_not_recent_post(json_posts, own_username)
        assert post_id is not None, f"Precondition error. Failed to find post matched to requirements for user: {role}"
        return post_id
    yield _get_expired_post

@pytest.fixture()
def post_cleaner(get_service_by_role):
    created_ids = []
    def register(post_id, role:str):
        created_ids.append((post_id, role))
    yield register  # тест получает функцию регистрации
    for post_id, role in created_ids:  # cleanup всего что зарегистрировано
        get_service_by_role(role).posts_api.delete_post(post_id)

@pytest.fixture()
@allure.title("API Fixture. Clean (remove) follow request after test")
def follow_request_cleaner(get_service_by_role):
    """
    Clean (remove) follow request after test
    :param get_service_by_role:
    :return:
    """
    created_ids = []
    def _register(user_name, role:str):
        created_ids.append((user_name, role))
    yield _register  # тест получает функцию регистрации
    for user_name, role in created_ids:  # cleanup всего что зарегистрировано
        get_service_by_role(role).follows_api.unfollow_user(user_name)






@pytest.fixture()
def follow_unfollow(request, get_service_by_role):
    params = request.param
    callspec = getattr(request.node, "callspec", None)

    if callspec:
        data_params = callspec.params
    else:
        data_params = None
    if data_params and data_params["expected_success"]:
        # print("FIXTURE. EXPECTED SUCCESS")
        user_services = get_service_by_role(params[0])
        if params[2] == "follow":
            try:
                user_services.follows_api.follow_user(params[1])
            except AssertionError:
                pass
        elif params[2] == "unfollow":
            try:
                user_services.follows_api.unfollow_user(params[1])
            except AssertionError:
                pass
    yield



@pytest.fixture()
def bookmark_post_only(request, get_service_by_role):
    user = get_service_by_role(request.param["create_by"])
    post = user.posts_api.get_list_posts().items[0]
    user.bookmarks_api.bookmark_post(post.id)
    yield post.id