import random
from dataclasses import dataclass

import faker
import pytest
from faker import Faker

from services.comments.payloads import CreateCommentBody
from services.posts.params import GetPostsParams
from services.posts.payloads import CreatePostBodyParams
from utils.data_helper import DataHelper as data_helper
from auth.role_factory import MultiRoleServiceFactory, ServiceContainer
from utils.data_helper import find_other_authors_post

fake = Faker()




@pytest.fixture(scope="session")
def get_service_by_role():
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
    payload=CreatePostBodyParams(content="B")

    post = post_service.create_post(payload)
    yield post.id
    post_service.delete_post(post.id)

@pytest.fixture()
def build_post_remove(get_service_by_role):
    created_posts:list[tuple] = []

    def _build(role:str):
        post_service = get_service_by_role(role).posts_api
        payload = CreatePostBodyParams(content="B")

        post = post_service.create_post(payload)
        created_posts.append((role, post.id))
        return post.id
    yield _build  # тест получает функцию регистрации

    for role, post_id in reversed(created_posts):
        get_service_by_role(role).posts_api.delete_post(post_id)

@pytest.fixture()
def build_post_pin_remove(get_service_by_role):
    created_posts:list[tuple] = []

    def _build(role:str):
        post_service = get_service_by_role(role).posts_api
        payload = CreatePostBodyParams(content="B")

        post = post_service.create_post(payload)
        post_service.pin_post(post.id)
        created_posts.append((role, post.id))
        return post.id
    yield _build  # тест получает функцию регистрации

    for role, post_id in reversed(created_posts):
        get_service_by_role(role).posts_api.delete_post(post_id)

@pytest.fixture()
def get_removed_post(get_service_by_role):

    def _remove_post_by(role):
        post_service = get_service_by_role(role).posts_api
        payload = CreatePostBodyParams(content="B")

        post = post_service.create_post(payload)
        post_service.delete_post(post.id)
        return post.id

    yield _remove_post_by

@pytest.fixture()
def create_and_get_post(get_service_by_role):
    def _create(role:str):
        post_service = get_service_by_role(role).posts_api
        payload = CreatePostBodyParams(content="B")

        post = post_service.create_post(payload)
        return post.id
    yield _create

@pytest.fixture()
def create_comment_remove_after(request, get_service_by_role):
    case_info = request.param
    user = get_service_by_role(case_info["precondition_role"])
    post = user.posts_api.get_list_posts().items[0]
    comment = user.comments_api.create_comment(post_id=post.id,
                                               payload=data_helper().get_random_comment_payload())
    yield comment.id
    user.comments_api.delete_comment(comment.id)

@pytest.fixture()
def build_comment_remove(request, get_service_by_role):
    created_comments:list[tuple] = []

    def _build_comment(role:str):
        app_services:ServiceContainer = get_service_by_role(role)
        payload = CreateCommentBody(content="B")
        posts:list[dict] = _get_posts_list_for_user(app_services.posts_api)
        comment = app_services.comments_api.create_comment(post_id=random.choice(posts).id, payload=payload)
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
def like_post_only(request, get_service_by_role):
    user = get_service_by_role(request.param["create_by"])
    post = user.posts_api.get_list_posts().items[0]
    user.likes_api.like_post(post.id,payload={},)
    yield post.id

@pytest.fixture()
def bookmark_post_only(request, get_service_by_role):
    user = get_service_by_role(request.param["create_by"])
    post = user.posts_api.get_list_posts().items[0]
    user.bookmarks_api.bookmark_post(post.id)
    yield post.id





# @pytest.fixture()
# def R(get_service_by_role):
#     def _action_perform_by(role_alias:str):
#         user = get_service_by_role(role_alias)
#         post = user.posts_api.get_list_posts().items[0]
#         comment = user.comments_api.create_comment(post_id=post.id,
#                                                    payload=data_helper().get_random_comment_payload())
#         return comment.id
#     yield _action_perform_by


@pytest.fixture()
def get_liked_comment(get_service_by_role):
    def _action_perform_by(role_alias:str):
        user = get_service_by_role(role_alias)
        params = {"sort_by": "comments_count"}
        post = user.posts_api.get_list_posts(params=params).items[0]
        comments = user.comments_api.get_list_comments(post_id=post.id)
        for comment in comments:
            if not comment.is_liked:
                user.likes_api.like_comment(comment.id)
                return comment.id
        raise Exception("Fixture error: No comment without like")
    yield _action_perform_by





@pytest.fixture()
def like_post_before(get_service_by_role):
    def _action_perform_by(role_alias: str):
        user = get_service_by_role(role_alias)
        post = user.posts_api.get_list_posts().items[0]
        user.likes_api.like_post(post_id=post.id,
                                 payload={},
                                 expected_success=True)
        return post.id

    yield _action_perform_by

@pytest.fixture()
def get_post_with_comments(get_service_by_role):
    def _action_perform_by(role_alias: str):
        post_service = get_service_by_role(role_alias).posts_api
        params = GetPostsParams(sort_by="comments_count", page=1, per_page=5)

        posts_list_response = post_service.get_list_posts(params=params).items[0]
        return posts_list_response.id
    yield _action_perform_by


@pytest.fixture()
def get_comment_only(get_service_by_role):
    def _action_perform_by(role_alias: str):
        user = get_service_by_role(role_alias)
        params = {"sort_by": "comments_count"}
        post = user.posts_api.get_list_posts(params=params).items[0]
        comment = user.comments_api.get_list_comments(post_id=post.id).items[0]
        yield comment.id

    yield _action_perform_by

@pytest.fixture()
def like_post_and_remove_before(get_service_by_role):
    def _action_perform_by(role_alias: str):
        user = get_service_by_role(role_alias)
        post = user.posts_api.create_post(payload=data_helper().get_random_post_payload())
        user.likes_api.like_post(post_id=post.id,
                                 payload={},
                                 expected_success=True)
        user.posts_api.repost_post(post_id=post.id)
        return post.id

    yield _action_perform_by


@pytest.fixture()
def create_comment_and_remove_before(get_service_by_role):
    def _action_perform_by(role_alias: str):
        user = get_service_by_role(role_alias)
        params = {"sort_by": "comments_count"}
        post = user.posts_api.get_list_posts(params=params).items[0]
        comment = user.comments_api.create_comment(post_id=post.id,payload={data_helper().get_random_comment_payload()})
        user.comments_api.delete_comment(post_id=comment.id)
        return comment.id

    yield _action_perform_by


@pytest.fixture()
def get_not_liked_post_before(get_service_by_role):
    def _action_perform_by(role_alias: str):
        user = get_service_by_role(role_alias)
        posts = user.posts_api.get_list_posts()
        for post in posts:
            if not post.is_liked:
                return post.id
        raise Exception ("Fixture error: No posts without like")
    yield _action_perform_by

@pytest.fixture()
def get_liked_post_before(get_service_by_role):
    def _action_perform_by(role_alias: str):
        user = get_service_by_role(role_alias)
        params = {"sort_by": "comments_count"}
        posts = user.posts_api.get_list_posts(params=params).items
        if not posts[0].is_liked:
            user.likes_api.like_post(post_id=posts[0].id)
        return posts[0].id
    yield _action_perform_by

    @pytest.fixture()
    def get_comment_before(get_service_by_role):
        def _action_perform_by(role_alias: str):
            user = get_service_by_role(role_alias)
            params = {"sort_by": "comments_count"}
            post = user.posts_api.get_list_posts(params=params).items[0]
            comments = user.comments_api.get_list_comments(post_id=post.id)
            for comment in comments:
                if not comment.is_liked:
                    return comment.id
            raise Exception ("Fixture error: No posts without like")
        yield _action_perform_by


@pytest.fixture()
def get_liked_comment_before(get_service_by_role):
    def _action_perform_by(role_alias: str):
        user = get_service_by_role(role_alias)
        params = {"sort_by": "comments_count"}
        post = user.posts_api.get_list_posts(params=params).items[0]
        comments = user.comments_api.get_list_comments(post_id=post.id)
        if not comments[0].is_liked:
            user.likes_api.like_comment(comments[0].id)
        return comments[0].id
    yield _action_perform_by


@pytest.fixture()
def get_incorrect_post(request, get_service_by_role):
    case_info = request.param
    if  case_info["post_case"] == "not_own":
        user = get_service_by_role(case_info["create_by"])
        posts = user.posts_api.get_list_posts().items
        own_username = user.auth_api.get_me().username
        post_id = find_other_authors_post(posts, own_username)
        assert post_id is not None
        yield post_id
    elif case_info["post_case"] == "comment":
        user = get_service_by_role(case_info["precondition_role"])
        post = user.posts_api.get_list_posts().items[0]
        comment = user.comments_api.create_comment(post_id=post.id,
                                                   payload=data_helper().get_random_comment_payload(),
                                                   expected_success=True)
        yield comment.id
        user.comments_api.delete_comment(comment.id)
    elif case_info["post_case"] == "liked":
        user = get_service_by_role(case_info["precondition_role"])
        post = user.posts_api.get_list_posts().items[0]
        user.likes_api.like_post(post_id=post.id,
                                 payload={},
                                 expected_success=True)
        yield post.id
        user.likes_api.unlike_post(post.id)
    elif case_info["post_case"] == "not_liked":
        user = get_service_by_role(case_info["precondition_role"])
        post = user.posts_api.get_list_posts().items[1]
        yield post.id
    elif case_info["post_case"] == "bookmark":
        user = get_service_by_role(case_info["precondition_role"])
        post = user.posts_api.get_list_posts().items[0]
        user.bookmarks_api.bookmark_post(post.id)
        yield post.id
        user.bookmarks_api.remove_bookmark(post.id)
    elif case_info["post_case"] == "not_bookmark":
        user = get_service_by_role(case_info["precondition_role"])
        params = {"sort_by": "comments_count"}
        post = user.posts_api.get_list_posts(params=params).items[0]
        if post.is_bookmarked:
             user.bookmarks_api.remove_bookmark(post.id)
        yield post.id

@pytest.fixture()
def get_post_for_comment(request, get_service_by_role):
    case_info = request.param
    user = get_service_by_role(case_info["precondition_role"])
    params = {"sort_by": "comments_count"}
    post = user.posts_api.get_list_posts(params=params).items[0]
    yield post.id

@pytest.fixture()
def get_post_with_likes(request, get_service_by_role):
    user = get_service_by_role("admin")
    params = {"sort_by": "likes_count"}
    post = user.posts_api.get_list_posts(params=params).items[0]
    yield post.id

@pytest.fixture()
def get_comment_for_likes(request, get_service_by_role):
    case_info = request.param
    user = get_service_by_role(case_info["precondition_role"])
    params = {"sort_by": "comments_count"}
    post = user.posts_api.get_list_posts(params=params).items[0]
    comment = user.comments_api.get_list_comments(post_id=post.id).items[1]
    yield comment.id
    # user.likes_api.unlike_comment(comment_id=comment.id)

@pytest.fixture()
def like_comment_only(request, get_service_by_role):
    user = get_service_by_role(request.param["precondition_role"])
    params = {"sort_by": "comments_count"}
    post = user.posts_api.get_list_posts(params=params).items[0]
    comment = user.comments_api.get_list_comments(post_id=post.id).items[1]
    user.likes_api.like_comment(comment.id,payload={})
    yield comment.id

@pytest.fixture()
def create_comment_remove(request,  get_service_by_role):
    post_info = request.param
    user = get_service_by_role(post_info["precondition_role"])

    params = {"sort_by": "comments_count"}
    post = user.posts_api.get_list_posts(params=params).items[0]

    comment_body = data_helper().get_random_comment_payload()

    comment = user.comments_api.create_comment(post_id=post.id, payload=comment_body)


    yield comment.id
    user.comments_api.delete_comment(comment_id=comment.id)


@pytest.fixture()
def create_comment_only(request, get_service_by_role):
    user = get_service_by_role(request.param["precondition_role"])
    params = {"sort_by": "comments_count"}
    post = user.posts_api.get_list_posts(params=params).items[0]
    comment = user.comments_api.create_comment(post_id=post.id,
                                               payload=data_helper().get_random_comment_payload(),
                                               expected_success=True)
    yield comment.id

@pytest.fixture()
def get_incorrect_comment(request,  get_service_by_role):
    case_info = request.param
    if case_info["comment_case"] == "removed":
        user = get_service_by_role(case_info["precondition_role"])
        params = {"sort_by": "comments_count"}
        post = user.posts_api.get_list_posts(params=params).items[0]
        comment = user.comments_api.create_comment(post_id=post.id, payload=data_helper().get_random_comment_payload())
        user.comments_api.delete_comment(comment.id)
        yield comment.id
    elif case_info["comment_case"] == "not_existed":
        comment_id = fake.uuid4()
        yield comment_id
    elif case_info["comment_case"] == "invalid_uuid":
        yield "10AW000-0Z0-0Y0-0Y0-00a00000002"
    elif case_info["comment_case"] == "late":

        user = get_service_by_role(case_info["precondition_role"])
        params = {"sort_by": "comments_count"}
        post = user.posts_api.get_list_posts(params=params).items[0]

        own_username = user.auth_api.get_me().username

        comments = user.comments_api.get_list_comments(post_id=post.id).items
        comment_id = data_helper.find_not_recent_comment(comments, own_username)
        assert comment_id is not None
        yield comment_id
    elif case_info["comment_case"] == "not_own":
        user = get_service_by_role(case_info["precondition_role"])
        params = {"sort_by": "comments_count"}
        post = user.posts_api.get_list_posts(params=params).items[0]
        own_username = user.auth_api.get_me().username

        comments = user.comments_api.get_list_comments(post_id=post.id).items

        comment_id = data_helper.find_other_authors_comment(comments, own_username)
        assert comment_id is not None
        yield comment_id
    elif case_info["comment_case"] == "post":
        user = get_service_by_role(case_info["precondition_role"])
        post = user.posts_api.get_list_posts().items[0]
        yield post.id
    elif case_info["comment_case"] == "liked":
        user = get_service_by_role(case_info["precondition_role"])
        params = {"sort_by": "comments_count"}

        post = user.posts_api.get_list_posts(params=params).items[1]
        comment = user.comments_api.create_comment(post_id=post.id,
                                                   payload=data_helper().get_random_comment_payload(),
                                                   expected_success=True)
        user.likes_api.like_comment(comment_id=comment.id,
                                 payload={},
                                 expected_success=True)
        yield comment.id
        user.comments_api.delete_comment(comment.id)
    elif case_info["comment_case"] == "not_liked":
        user = get_service_by_role(case_info["precondition_role"])
        params = {"sort_by": "comments_count"}
        post = user.posts_api.get_list_posts(params=params).items[0]
        comment = user.comments_api.get_list_comments(post_id=post.id).items[1]
        yield comment.id

@pytest.fixture()
def create_reply_remove(request,  get_service_by_role):
    post_info = request.param
    user = get_service_by_role(post_info["precondition_role"])

    params = {"sort_by": "comments_count"}
    post = user.posts_api.get_list_posts(params=params).items[0]

    comment_body = data_helper().get_random_comment_payload()

    comment = user.comments_api.create_comment(post_id=post.id, payload=comment_body)


    yield comment.id
    user.comments_api.delete_comment(comment_id=comment.id)





@pytest.fixture()
def like_comment_cleaner(get_service_by_role):
    created_ids = []

    def register(comment_id, role="user_eve"):
        created_ids.append((comment_id, role))

    yield register  # тест получает функцию регистрации

    for comment_id, role in created_ids:  # cleanup всего что зарегистрировано
        get_service_by_role(role).likes_api.unlike_comment(comment_id)


@pytest.fixture()
def post_like_cleaner(get_service_by_role):
    created_ids = []

    def register(post_id, role="user_eve"):
        created_ids.append((post_id, role))

    yield register  # тест получает функцию регистрации

    for post_id, role in created_ids:  # cleanup всего что зарегистрировано
        get_service_by_role(role).likes_api.unlike_post(post_id)

@pytest.fixture()
def post_like_setter(get_service_by_role):
    created_ids = []

    def register(post_id, role="user_eve"):
        created_ids.append((post_id, role))

    yield register  # тест получает функцию регистрации

    for post_id, role in created_ids:  # cleanup всего что зарегистрировано
        get_service_by_role(role).likes_api.like_post(post_id)


@pytest.fixture()
def comment_like_setter(get_service_by_role):
    created_ids = []

    def register(comment_id, role="user_eve"):
        created_ids.append((comment_id, role))

    yield register  # тест получает функцию регистрации

    for comment_id, role in created_ids:  # cleanup всего что зарегистрировано
        get_service_by_role(role).likes_api.like_post(comment_id)