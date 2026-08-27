import allure
import pytest

from config.base_test import BaseTest
from services.posts.params import GetPostsParams, GetPostsByRoleTestCase, \
    GetFeedParams, GetFeedByRoleTestCase, DeletePostParams, DeletePostByRoleTestCase
from services.posts.payloads import CreatePostPayload, CreatePostByRoleTestCase, \
    UpdatePostPayload, UpdatePostByRoleTestCase, CreateRepostByRoleTestCase, CreateRepostPayload


@allure.epic("Posts Service")
@allure.feature("Posts")
@allure.parent_suite("Tests Posts service API")
@allure.title("Tests Posts service API")
@pytest.mark.feed
class TestPosts(BaseTest):

    @allure.suite("Get posts list")
    @allure.story("User can read existed posts at platform")
    @allure.description("Get posts list - valid payload")
    @pytest.mark.smoke
    @pytest.mark.parametrize("case", [
        pytest.param(GetPostsByRoleTestCase(role="user_bob",
            params=GetPostsParams(hashtag="coding", author_id="00000000-0000-0000-0000-000000000003",
                                  sort_by="created_at", page=1, per_page=1)),
            id="fully valid request with minimum boundaries"),
        pytest.param(GetPostsByRoleTestCase(role="user_eve",
            params=GetPostsParams(hashtag="devlife", author_id="00000000-0000-0000-0000-000000000002",
                                  sort_by="likes_count", page=2, per_page=100, sort_order="desc")),
            id="valid max boundary + different enum values"),
        pytest.param(GetPostsByRoleTestCase(role="user_bob",
            params=GetPostsParams(hashtag="unknown_tag", page=1, per_page=10)),
            id="non-existing hashtag"),
        pytest.param(GetPostsByRoleTestCase(role="user_eve",
            params=GetPostsParams(author_id="00000000-0000-0000-0000-999999999999", page=1, per_page=10)),
            id="non-existing author"),
    ])
    def test_get_posts(self, case):
        post_service = self.get_actor(case.role).posts_api
        post_service.get_list_posts(params=case.params)

    @allure.suite("Get posts list")
    @allure.story("User can read existed posts at platform")
    @allure.description("Get posts list - depending on role {role}")
    @pytest.mark.parametrize("case", [
        pytest.param(GetPostsByRoleTestCase(params=GetPostsParams(), role="admin"), id="Request posts list as admin"),
        pytest.param(GetPostsByRoleTestCase(params=GetPostsParams(),role="moderator"), id="Request posts list as moderator"),
        pytest.param(GetPostsByRoleTestCase(params=GetPostsParams(), role="user_bob"), id="Request posts list as user"),
    ])
    def test_get_posts_depends_on_role(self, case):
        post_service = self.get_actor(case.role).posts_api
        post_service.get_list_posts()

    @allure.suite("Get posts list")
    @allure.story("User can read existed posts at platform")
    @allure.description("Get posts list - invalid queries")
    @pytest.mark.parametrize("case", [
        pytest.param(GetPostsByRoleTestCase(role="user_bob",
            params=GetPostsParams(sort_by="comments_count", sort_order="asc", page=0, per_page=10)),
            id="invalid page below minimum"),
        pytest.param(GetPostsByRoleTestCase(role="user_bob",
            params=GetPostsParams(hashtag="coding", page=1, per_page=0)),
            id="invalid per_page below minimum"),
        pytest.param(GetPostsByRoleTestCase(role="user_bob",
            params=GetPostsParams(author_id="00000000-0000-0000-0000-000000000003", page=3, per_page=101)),
            id="invalid per_page above maximum"),
        pytest.param(GetPostsByRoleTestCase(role="user_bob",
            params=GetPostsParams(sort_by="views_count", sort_order="asc", per_page=10, page=1)),
            id="invalid sort_by enum"),
        pytest.param(GetPostsByRoleTestCase(role="user_bob",
            params=GetPostsParams(sort_by="created_at", sort_order="up", per_page=10, page=1)),
            id="invalid sort_order enum"),
    ])
    def test_get_posts_invalid_queries(self, case):
        post_service = self.get_actor(case.role).posts_api
        post_service.get_list_posts(params=case.params,
                                               status_code=422,
                                               expected_success=False)

    @allure.suite("Create post")
    @allure.story("User can create post at platform")
    @allure.description("Create post - valid payload")
    @pytest.mark.parametrize("case", [
        pytest.param(CreatePostByRoleTestCase(role="user_bob",
            payload=CreatePostPayload(content="A", visibility="public")),
            id="Valid minimal boundary + default visibility and image None"),
        pytest.param(CreatePostByRoleTestCase(role="user_eve",
            payload=CreatePostPayload(content="A" * 2000, visibility="public")),
            id="valid max boundary + image"),
        pytest.param(CreatePostByRoleTestCase(role="user_bob",
            payload=CreatePostPayload(content=f"Another valid post", visibility="followers_only")),
            id="valid followers_only without image"),
        pytest.param(CreatePostByRoleTestCase(role="user_eve",
            payload=CreatePostPayload(content=f"Image post", visibility="public", image_url="/test_data/image.jpg")),
            id="valid public with image"),
        pytest.param(CreatePostByRoleTestCase(role="user_bob",
            payload=CreatePostPayload(content=f"Default visibility post", visibility="public")),
            id="optional image_url omitted + default visibility"),
    ])
    def test_create_post(self, case, post_cleaner):
        posts_service = self.get_actor(case.role).posts_api
        new_post = posts_service.create_post(payload=case.payload)

        post_cleaner(new_post.id, case.role)  # регистрируем на удаление
        assert new_post.content == case.payload.content
        assert new_post.visibility == case.payload.visibility
        if case.payload.image_url:
            assert new_post.image_url == case.payload.image_url

    @allure.suite("Create post")
    @allure.story("User can create post at platform")
    @allure.description("Create post - depending on role {role}")
    @pytest.mark.parametrize("case", [
        pytest.param(CreatePostByRoleTestCase(role="admin", payload=CreatePostPayload(content="B")),
                     id="Create post as admin"),
        pytest.param(CreatePostByRoleTestCase(role="moderator", payload=CreatePostPayload(content="C")),
                     id="Create post as moderator"),
        pytest.param(CreatePostByRoleTestCase(role="user_bob", payload=CreatePostPayload(content="D")),
                     id="Create post as user"),
    ])
    def test_create_posts_depends_on_role(self, case, post_cleaner):
        posts_service = self.get_actor(case.role).posts_api
        new_post = posts_service.create_post(payload=case.payload)
        post_cleaner(new_post.id, case.role)  # регистрируем на удаление
        assert new_post.content == case.payload.content
        assert new_post.visibility == case.payload.visibility

    @allure.suite("Create post")
    @allure.story("User can create post at platform")
    @allure.description("Create post -  invalid payload")
    @pytest.mark.parametrize("case", [
        pytest.param(CreatePostByRoleTestCase(role="admin",
            payload=CreatePostPayload(content="", visibility="public")),
            id="invalid content, below min boundary"),
        pytest.param(CreatePostByRoleTestCase(role="admin",
            payload=CreatePostPayload(content="A" * 2001, visibility="public")),
            id="invalid content, above max boundary"),
        pytest.param(CreatePostByRoleTestCase(role="admin",
            payload=CreatePostPayload(content="Valid post content", visibility="private")),
            id="valid followers_only without image"),
    ])
    def test_create_post_invalid_payload(self, case):
        post_service = self.get_actor(case.role).posts_api
        post_service.create_post(payload=case.payload,
                                            status_code=422,
                                            expected_success=False)

    @allure.suite("Get posts feed")
    @allure.story("User can read existed posts feed at platform")
    @allure.description("Get posts feed")
    @pytest.mark.parametrize("case", [
        pytest.param(GetFeedByRoleTestCase(role="user_eve", params=GetFeedParams(page=1, per_page=1)), id="valid minimum boundaries"),
        pytest.param(GetFeedByRoleTestCase(role="user_eve", params=GetFeedParams(page=2, per_page=100)), id="valid maximum boundary"),
        pytest.param(GetFeedByRoleTestCase(role="user_eve", params=GetFeedParams(page=None, per_page=None)), id="empty query param"),
    ])
    def test_get_posts_feed(self, case):
        post_service = self.get_actor(case.role).posts_api
        post_service.get_posts_feed(params=case.params)

    @allure.suite("Get posts feed")
    @allure.story("User can read existed posts feed at platform")
    @allure.description("Get posts feed depending on user role -  {role}")
    @pytest.mark.parametrize("case", [
        pytest.param(GetFeedByRoleTestCase(role="admin", params=GetFeedParams()), id="Create post as admin"),
        pytest.param(GetFeedByRoleTestCase(role="moderator", params=GetFeedParams()), id="Create post as moderator"),
        pytest.param(GetFeedByRoleTestCase(role="user_bob", params=GetFeedParams()), id="Create post as user"),
    ])
    def test_get_posts_feed_depends_on_role(self, case):
        post_service = self.get_actor(case.role).posts_api
        post_service.get_posts_feed()

    @allure.suite("Get posts feed")
    @allure.story("User can read existed posts feed at platform")
    @allure.description("Get posts feed - invalid query params")
    @pytest.mark.parametrize("case", [
        pytest.param(GetFeedByRoleTestCase(role="user_bob", params=GetFeedParams(page=0, per_page=10)),id="invalid page below minimum"),
        pytest.param(GetFeedByRoleTestCase(role="user_bob", params=GetFeedParams(page=1, per_page=0)),id="invalid per_page below minimum"),
        pytest.param(GetFeedByRoleTestCase(role="user_bob", params=GetFeedParams(page=3, per_page=101)),id="invalid per_page above maximum"),
    ])
    def test_get_posts_feed_invalid_payload(self, case):
        post_service = self.get_actor(case.role).posts_api
        post_service.get_posts_feed(params=case.params,
                                               status_code=422,
                                               expected_success=False)

    @allure.suite("Get certain post")
    @allure.story("User can read existed post at platform")
    @allure.description("Get certain post - get post depending on role")
    @pytest.mark.positive
    @pytest.mark.parametrize("builder_role, user_role", [
        pytest.param("admin", "user_bob",id="As user get public post created by admin"),
        pytest.param("user_eve", "moderator",id="As moderator get the post (followers only) created by user"),
        pytest.param("moderator", "admin",id="As admin get public post created by moderator"),
    ])
    def test_get_post_depends_on_role(self, builder_role, build_post_remove, user_role):
        prepared_post_id = build_post_remove(role=builder_role)
        post_service = self.get_actor(user_role).posts_api
        post_service.get_post(post_id=prepared_post_id)


    @allure.suite("Get certain post")
    @allure.story("User can read existed post at platform")
    @allure.description("Get certain post - removed post")
    @pytest.mark.parametrize("case_role", [
        pytest.param("user_bob",id="Try to get removed post")
    ])
    def test_get_post_removed_post(self, get_removed_post, case_role):
        prepared_post_id = get_removed_post(case_role)
        post_service = self.get_actor(case_role).posts_api
        post_service.get_post(post_id=prepared_post_id,
                                expected_success=False,
                                status_code=404)

    @allure.suite("Get certain post")
    @allure.story("User can read existed post at platform")
    @allure.description("Get certain post - not existed post_id")
    @pytest.mark.parametrize("case_user", [pytest.param("user_bob",id="Try to get not existed post")
    ])
    def test_get_post_not_existed_post(self, case_user):
        prepared_post_id = self.data_helper.get_not_existed_uuid()
        post_service = self.get_actor(case_user).posts_api
        post_service.get_post(post_id=prepared_post_id,
                                expected_success=False,
                                status_code=404)

    @allure.suite("Update post")
    @allure.feature("User can update created post")
    @allure.story("As a post creator i can update it after publishing")
    @allure.description("Update post as author")
    @pytest.mark.parametrize("case", [
        pytest.param(UpdatePostByRoleTestCase(role="user_eve",payload=UpdatePostPayload(content="A")),
                     id="Update post created by author - Valid minimal boundary"),
        pytest.param(UpdatePostByRoleTestCase(role="user_bob",payload=UpdatePostPayload(content="A" * 2000)),
                     id="Update post created by author - Valid maximal boundary"),
    ])
    def test_update_post(self, build_post_remove, case):
        post_service = self.get_actor(case.role).posts_api

        prepared_post_id = build_post_remove(case.role)
        prepared_post = post_service.get_post(post_id=prepared_post_id)

        updated_post = post_service.update_post(post_id=prepared_post_id, payload=case.payload)
        update_time_before = prepared_post.updated_at

        assert updated_post.updated_at > update_time_before, (updated_post.updated_at, update_time_before)
        assert prepared_post.content != updated_post.content, "Content does not updated after PATCH"
        if "image_url" in case.payload:
            assert prepared_post.image_url != updated_post.image_url, f"Image url does not updated after PATCH - {updated_post.image_url}"
        if "visibility" in case.payload:
            assert prepared_post.visibility != updated_post.visibility, f"Visibility does not updated after PATCH - {updated_post.visibility}"

    @allure.suite("Update post")
    @allure.feature("User can update created post")
    @allure.story("As a user i can update only own post in valid time range")
    @allure.description("Attempt to update the post removed before")
    @pytest.mark.parametrize("case", [
        pytest.param(UpdatePostByRoleTestCase(role="user_bob", payload=UpdatePostPayload(content="A"), status_code=404, expected_success=False),
                     id="Try to update post, that was removed"),
    ])
    def test_update_removed_post(self, get_removed_post, case):
        prepared_post_id = get_removed_post(case.role)
        post_service = self.get_actor(case.role).posts_api
        post_service.update_post(post_id=prepared_post_id,
                                            payload=case.payload,
                                            expected_success=case.expected_success,
                                            status_code=case.status_code)

    @allure.suite("Update post")
    @allure.feature("User can update created post")
    @allure.story("As a user i can update only own post in valid time range")
    @allure.description("Attempt to update the post if allowed period to edit is expired")
    @pytest.mark.parametrize("case", [
        pytest.param(UpdatePostByRoleTestCase(role="user_eve", payload=UpdatePostPayload(content="A-edited"),
                                              status_code=400, expected_success=False),
                     id="As author update the post, that older than 15 minutes"),
    ])
    def test_update_post_expired_to_edit(self, get_expired_to_edit_post, case):
        post_service = self.get_actor(case.role).posts_api
        prepared_post_id = get_expired_to_edit_post(case.role)
        post_service.update_post(post_id=prepared_post_id,
                                            payload=case.payload,
                                            expected_success=case.expected_success,
                                            status_code=case.status_code)

    @allure.suite("Update post")
    @allure.feature("User can update created post")
    @allure.story("As a user i can update only own post in valid time range")
    @allure.description("Attempt to update the post created by another user")
    @pytest.mark.parametrize("post_builder_user, case", [
        pytest.param("user_bob",
                     UpdatePostByRoleTestCase(role="user_eve", payload=UpdatePostPayload(content="A-edited"), status_code=403, expected_success=False),
                     id="Attempt to update the post created by another user"),
    ])
    def test_update_post_created_by_another_user(self, post_builder_user, build_post_remove, case):
        post_service = self.get_actor(case.role).posts_api
        prepared_post_id = build_post_remove(post_builder_user)
        post_service.update_post(post_id=prepared_post_id,
                                            payload=case.payload,
                                            expected_success=case.expected_success,
                                            status_code=case.status_code)

    @allure.suite("Update post")
    @allure.feature("User can update created post")
    @allure.story("As a user i can update only own post in valid time range")
    @allure.description("Test attempt to update post, that doesn't exist")
    @pytest.mark.parametrize("case", [
        pytest.param(UpdatePostByRoleTestCase(role="user_eve", payload=UpdatePostPayload(content="A-edited"), status_code=404, expected_success=False),
                     id="Attempt to update post, that doesn't exist"),
    ])
    def test_update_post_not_existed(self, case):
        post_service = self.get_actor(case.role).posts_api
        prepared_post_id = self.data_helper.get_not_existed_uuid()
        post_service.update_post(post_id=prepared_post_id,
                                            payload=case.payload,
                                            expected_success=case.expected_success,
                                            status_code=case.status_code)

    @allure.suite("Update post")
    @allure.story("User can update created post")
    @allure.description("Attempt to edit post using invalid payload")
    @pytest.mark.parametrize("case", [
        pytest.param(UpdatePostByRoleTestCase(role="user_eve", payload=UpdatePostPayload(content="")),
                     id="Update post - content, below min boundary"),
        pytest.param(UpdatePostByRoleTestCase(role="user_eve", payload=UpdatePostPayload(content="A" * 2001)),
                     id="Update post - content, above max boundary"),
        pytest.param(UpdatePostByRoleTestCase(role="user_eve", payload=UpdatePostPayload(content=2001)),
                     id="Update post - content, Integer type of value"),
    ])
    def test_update_post_invalid_payload(self, build_post_remove, case):
        prepared_post_id = build_post_remove(case.role)
        post_service = self.get_actor(case.role).posts_api
        post_service.update_post(post_id=prepared_post_id,
                                   payload=case.payload,
                                   expected_success=False,
                                   status_code=422)


    @allure.suite("Remove post")
    @allure.story("User can remove created post")
    @allure.description("Precondition: post created before test")
    @pytest.mark.parametrize("case", [
        pytest.param(DeletePostByRoleTestCase(role="user_eve", params=DeletePostParams()),
                     id="Remove post- its author"),
        pytest.param(DeletePostByRoleTestCase(role="user_eve", params=DeletePostParams(reason="Delete it immediately")),
                     id="Remove post - its author and with provided 'reason'"),
    ])
    def test_delete_post(self, create_and_get_post, case):
        prepared_post_id = create_and_get_post(case.role)
        post_service = self.get_actor(case.role).posts_api

        if case.params is not None:
            post_service.delete_post(post_id=prepared_post_id, params=case.params)
        else:
            post_service.delete_post(post_id=prepared_post_id)

        #check
        post_service.get_post(post_id=prepared_post_id,
                                status_code=404,
                                expected_success=False)

    @allure.suite("Remove post")
    @allure.story("User can remove created post")
    @allure.description("Attempt to remove the post depends on user's role (admin, moderator)")
    @pytest.mark.parametrize("case", [
        pytest.param(DeletePostByRoleTestCase(role="admin", params=DeletePostParams()),
                     id="Remove post - by admin"),
        pytest.param(DeletePostByRoleTestCase(role="moderator", params=DeletePostParams()),
                     id="Remove post - by moderator"),
    ])
    def test_delete_post_by_role(self, create_and_get_post, case):
        post_service = self.get_actor(case.role).posts_api
        prepared_post_id = create_and_get_post(case.role)

        post_service.delete_post(post_id=prepared_post_id)

        #check
        post_service.get_post(post_id=prepared_post_id,
                                status_code=404,
                                expected_success=False)

    @allure.suite("Remove post")
    @allure.story("User can remove created post")
    @allure.description("As user attempt to remove the post of another user")
    @pytest.mark.parametrize("post_builder_user, case", [
        pytest.param("user_bob",DeletePostByRoleTestCase(role="user_eve", params=DeletePostParams(),
                                 expected_success=False,status_code=403),
                     id="Remove post of another user"),
    ])
    def test_delete_post_as_user(self, post_builder_user, build_post_remove, case):
        prepared_post_id = build_post_remove(role=post_builder_user)
        post_service = self.get_actor(case.role).posts_api
        post_service.delete_post(post_id=prepared_post_id,
                                   expected_success=case.expected_success,
                                   status_code=case.status_code)

    @allure.suite("Remove post")
    @allure.story("User can remove created post")
    @allure.description("Attempt to remove the post - invalid post id")
    @pytest.mark.parametrize("case", [
        pytest.param(DeletePostByRoleTestCase(role="user_eve", params=DeletePostParams(), expected_success=False,
                                              status_code=404), id="Remove post that doesn't exist"),
    ])
    def test_delete_post_invalid(self, case):
        prepared_post_id = self.data_helper.get_not_existed_uuid()
        post_service = self.get_actor(case.role).posts_api
        post_service.delete_post(post_id=prepared_post_id,
                                   expected_success=case.expected_success,
                                   status_code=case.status_code)

    @allure.suite("Repost post")
    @allure.story("User can repost existed post")
    @allure.description("Create valid repost post")
    @pytest.mark.parametrize("build_post_by_user, case", [
        pytest.param("user_bob", CreateRepostByRoleTestCase(role="user_eve", payload=CreateRepostPayload(repost_type="repost")),
                     id="Repost post - repost type and without content"),
        pytest.param("user_bob", CreateRepostByRoleTestCase(role="user_eve", payload=CreateRepostPayload(repost_type="quote", content="A" * 2000)),
                     id="Repost post - quote type and  max content boundary"),
        pytest.param("user_bob",CreateRepostByRoleTestCase(role="user_eve", payload=CreateRepostPayload(content="Content only")),
                     id="Repost post - without defined repost type"),
    ])
    def test_repost_post(self, case,build_post_by_user, build_post_remove):
        prepared_post_id = build_post_remove(build_post_by_user)
        post_service = self.get_actor(case.role).posts_api
        reposted_post_before = post_service.get_post(post_id=prepared_post_id)
        reposted_post_after = post_service.repost_post(payload=case.payload,
                                                         post_id=prepared_post_id)

        assert reposted_post_before.repost_type != reposted_post_after.repost_type, f"Repost_type isn't changed after repost. AR: {reposted_post_after.repost_type}"
        if case.payload.repost_type:
            assert reposted_post_after.repost_type == case.payload.repost_type, f"Repost_type isn't matched expected one. AR: {reposted_post_after.repost_type}"
        else:
            assert reposted_post_after.repost_type == "repost", f"Repost_type isn't matched expected one. AR: {reposted_post_after.repost_type}"

    @allure.suite("Repost post")
    @allure.story("User can repost existed post")
    @allure.description("Attempt to create repost with invalid payload")
    @pytest.mark.parametrize("build_post_by_user, case", [
        pytest.param("user_bob", CreateRepostByRoleTestCase(role="user_eve", payload=CreateRepostPayload(
            repost_type="quote", content="A" * 2001)),
                     id="Invalid request payload - content, content above max boundary"),
        pytest.param("user_bob", CreateRepostByRoleTestCase(role="user_eve", payload=CreateRepostPayload(
            repost_type="invalid_type", content="A" * 2)),
                     id="Invalid request payload - Invalid repost type enum"),
    ])
    def test_repost_post_invalid_payload(self,  case, build_post_by_user, build_post_remove):
        prepared_post_id = build_post_remove(build_post_by_user)
        post_service = self.get_actor(case.role).posts_api
        post_service.repost_post(payload=case.payload,
                                   post_id=prepared_post_id,
                                   expected_success=False,
                                   status_code=422)

    @allure.suite("Repost post")
    @allure.story("User can repost existed post")
    @allure.description("Attempt to create repost, when post id is incorrect")
    @pytest.mark.parametrize("case", [
        pytest.param(CreateRepostByRoleTestCase(role="user_bob",payload=CreateRepostPayload(repost_type="repost",content="A" * 2)),
                     id="Non-existing post id"),
    ])
    def test_repost_post_not_existed(self, case):
        prepared_post_id = self.data_helper.get_not_existed_uuid()
        post_service = self.get_actor(case.role).posts_api
        post_service.repost_post(payload=case.payload,
                                   post_id=prepared_post_id,
                                   expected_success=False,
                                   status_code=404)

    @allure.suite("Repost post")
    @allure.story("User can repost existed post")
    @allure.description("Attempt to create repost, when post id is incorrect")
    @pytest.mark.parametrize("case", [
        pytest.param(CreateRepostByRoleTestCase(role="user_bob",payload=CreateRepostPayload(repost_type="repost",content="A" * 2)),
                     id="Attempt to repost removed post"),
    ])
    def test_repost_post_removed(self, case, get_removed_post):
        prepared_post_id = get_removed_post(case.role)
        post_service = self.get_actor(case.role).posts_api
        post_service.repost_post(payload=case.payload,
                                   post_id=prepared_post_id,
                                   expected_success=False,
                                   status_code=404)

    @allure.suite("Pin/unpin post")
    @allure.story("User can pin existed post")
    @allure.description("Precondition: post created before test and remove after")
    @pytest.mark.parametrize("case_user", [
        pytest.param("user_eve", id="Pin the post as author"),
    ])
    def test_pin_post(self, build_post_remove, case_user):
        prepared_post_id = build_post_remove(case_user)
        post_service = self.get_actor(case_user).posts_api

        post_before = post_service.get_post(post_id=prepared_post_id)
        post_service.pin_post(post_id=prepared_post_id)

        pin_post_after = post_service.get_post(post_id=prepared_post_id)
        assert post_before.is_pinned == pin_post_after.is_pinned if post_before.is_pinned is True else post_before.is_pinned != pin_post_after.is_pinned

    @allure.suite("Pin/unpin post")
    @allure.story("User can pin existed post")
    @allure.description("Unpin the post")
    @pytest.mark.parametrize("case_user", [
        pytest.param("user_eve", id="Post already pinned"),
    ])
    def test_pin_post(self, build_post_pin_remove, case_user):
        prepared_post_id = build_post_pin_remove(case_user)
        post_service = self.get_actor(case_user).posts_api

        post_before = post_service.get_post(post_id=prepared_post_id)

        post_service.unpin_post(post_id=prepared_post_id)

        pinned_post_after = post_service.get_post(post_id=prepared_post_id)
        assert post_before.is_pinned == pinned_post_after.is_pinned if post_before.is_pinned is True else post_before.is_pinned != pinned_post_after.is_pinned

    @allure.suite("Pin/unpin post")
    @allure.story("User can pin existed post")
    @allure.description("Attempt to pin post of another user by user with different roles: {test_data['user]}")
    @pytest.mark.parametrize("post_creator, case_user", [
        pytest.param("user_eve", "admin",
                     id="Pin the post of another user as admin"),
        pytest.param("user_eve","moderator",
                     id="Pin the post of another user as moderator"),
        pytest.param("user_eve","user_bob",
                     id="Pin the post of another user as user")
    ])
    def test_pin_post_by_another_user(self, post_creator, build_post_remove, case_user):
        prepared_post_id = build_post_remove(post_creator)
        post_service = self.get_actor(case_user).posts_api
        post_service.pin_post(post_id=prepared_post_id,
                                expected_success=False,
                                status_code=403)

    @allure.suite("Pin/unpin post")
    @allure.story("User can pin existed post")
    @allure.description("Attempt to pin the post, when post doesn't exist")
    @pytest.mark.parametrize("case_user", [
        pytest.param("user_eve",id="Pin the post that doesn't exist"),])
    def test_pin_post_not_existed(self, case_user):
        prepared_post_id = self.data_helper.get_not_existed_uuid()
        post_service = self.get_actor(case_user).posts_api
        post_service.pin_post(post_id=prepared_post_id,
                                expected_success=False,
                                status_code=404)

    @allure.suite("Pin/unpin post")
    @allure.story("User can pin existed post")
    @allure.description("Attempt to pin the post, when post removed")
    @pytest.mark.parametrize("case_user", [
        pytest.param("user_eve",
                     id="Post id existed, but post is deleted"),
    ])
    def test_pin_post_removed(self, get_removed_post, case_user):
        prepared_post_id = get_removed_post(case_user)
        post_service = self.get_actor(case_user).posts_api
        post_service.pin_post(post_id=prepared_post_id,
                                expected_success=False,
                                status_code=404)

    @allure.suite("Pin/unpin post")
    @allure.story("User can UNpin own post already pinned")
    @allure.description("Attempt to pin post of another user by user with different roles: {test_data['user]}")
    @pytest.mark.parametrize("create_and_pin_by_user, case_user", [
        pytest.param("user_eve", "admin",
                     id="UnPin the post of another user as admin"),
        pytest.param("user_eve", "moderator",
                     id="UnPin the post of another user as moderator"),
        pytest.param("user_eve", "user_bob",
                     id="UnPin the post of another user as user")
    ])
    def test_unpin_post_by_another_user(self, build_post_pin_remove, create_and_pin_by_user, case_user):
        prepared_post_id = build_post_pin_remove(create_and_pin_by_user)
        post_service = self.get_actor(case_user).posts_api
        post_service.unpin_post(post_id=prepared_post_id,
                                  expected_success=False,
                                  status_code=403)

    @allure.suite("Pin/unpin post")
    @allure.story("User can UNpin own post already pinned")
    @allure.description("Attempt to pin the post, that doesn't exist")
    @pytest.mark.parametrize("case_user", [
        pytest.param("user_eve",id="Pin the post that doesn't exist"),
    ])
    def test_unpin_post_not_existed(self, case_user):
        prepared_post_id = self.data_helper.get_not_existed_uuid()
        post_service = self.get_actor(case_user).posts_api
        post_service.unpin_post(post_id=prepared_post_id,
                                  expected_success=False,
                                  status_code=404)

    @allure.suite("Pin/unpin post")
    @allure.story("User can UNpin own post already pinned")
    @allure.description("Attempt to pin the post, when post is deleted")
    @pytest.mark.parametrize("case_user", [
        pytest.param("user_eve",
                     id="Post id existed, but post is deleted"),
    ])
    def test_unpin_post_removed(self, get_removed_post, case_user):
        prepared_post_id = get_removed_post(case_user)
        post_service = self.get_actor(case_user).posts_api
        post_service.unpin_post(post_id=prepared_post_id,
                                  expected_success=False,
                                  status_code=404)
