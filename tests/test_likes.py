import allure
import pytest

from config.base_test import BaseTest
from services.likes.params import GetPostLikesByRoleTestCase, GetPostLikesParams
from services.likes.payloads import LikePostByRoleTestCase, LikePostPayload, LikeCommentByRoleTestCase, \
    LikeCommentPayload


@allure.epic("Likes Service")
@allure.feature("Likes")
@allure.parent_suite("Tests Likes service API")
@allure.title("Tests Likes service API")
@pytest.mark.likes
class TestLikes(BaseTest):

    @allure.suite("Like post")
    @allure.story("User can like existed post")
    @allure.description("Like post")
    @pytest.mark.parametrize("case", [
        pytest.param(LikePostByRoleTestCase(role="admin", payload=LikePostPayload(reaction="like")),
                     id="Add reaction to post as admin - like"),
        pytest.param(LikePostByRoleTestCase(role="user_eve", payload=LikePostPayload(reaction="love")),
                     id="Add reaction to post as user - love"),
        pytest.param(LikePostByRoleTestCase(role="user_eve", payload=LikePostPayload(reaction="sad")),
                     id="Add reaction to post as user - sad"),
        pytest.param(LikePostByRoleTestCase(role="user_bob", payload=LikePostPayload(reaction="wow")),
                     id="Add reaction to post as user - wow"),
        pytest.param(LikePostByRoleTestCase(role="user_bob", payload=LikePostPayload(reaction="love")),
                     id="Add reaction to post as user - love"),
        pytest.param(LikePostByRoleTestCase(role="moderator", payload=LikePostPayload(reaction="angry")),
                     id="Add reaction to post as user - angry"),
    ])
    def test_like_post(self, build_post_remove, case):
        prepared_post_id = build_post_remove(case.role)
        app_services = self.get_actor(case.role)
        post_service = app_services.posts_api
        like_service = app_services.likes_api

        post_before = post_service.get_post(post_id=prepared_post_id)

        like_post = like_service.like_post(post_id=prepared_post_id, payload=case.payload)

        assert like_post.reaction == case.payload.reaction
        post_after = post_service.get_post(post_id=prepared_post_id)
        assert post_before.likes_count == post_after.likes_count - 1

    @allure.suite("Like post")
    @allure.story("User can like existed post")
    @allure.description("Like post - invalid payload")
    @pytest.mark.parametrize("case", [
        pytest.param(LikePostByRoleTestCase(role="admin", payload=LikePostPayload(reaction="busy")),
                     id="Add not allowed reaction to post"),
        pytest.param(LikePostByRoleTestCase(role="admin", payload=LikePostPayload(reaction="")),
                     id="Add empty string as reaction to post"),
        pytest.param(LikePostByRoleTestCase(role="admin", payload=LikePostPayload()),
                     id="Unexpected Empty payload"),
    ])
    def test_like_post_invalid_reaction(self, case, build_post_remove):
        like_service = self.get_actor(case.role).likes_api
        prepared_post_id = build_post_remove(case.role)

        like_service.like_post(post_id=prepared_post_id,
                               payload=case.payload,
                               status_code=422,
                               expected_success=False)

    @allure.suite("Like post")
    @allure.story("User can like existed post")
    @allure.description("Like post - Post removed")
    @pytest.mark.parametrize("case", [
        pytest.param(LikePostByRoleTestCase(role="admin", payload=LikePostPayload(reaction="like")),
                     id="Attempt to add reaction - Post removed"),
    ])
    def test_like_post_removed(self, case, get_removed_post):
        """Attempt to like post with not existed uuid"""
        like_service = self.get_actor(case.role).likes_api
        prepared_post_id = get_removed_post(case.role)

        like_service.like_post(post_id=prepared_post_id,
                               status_code=404,
                               payload=case.payload,
                               expected_success=False)

    @allure.suite("Like post")
    @allure.story("User can like existed post")
    @allure.description("Like post - Post doesn't exist")
    @pytest.mark.parametrize("case", [
        pytest.param(LikePostByRoleTestCase(role="admin", payload=LikePostPayload(reaction="like")),
                     id="Attempt to add reaction - not existed post"),
    ])
    def test_like_post_not_existed(self, case):
        """Attempt to like post with not existed uuid"""
        prepared_post_id = self.data_helper.get_not_existed_uuid()
        like_service = self.get_actor(case.role).likes_api
        like_service.like_post(post_id=prepared_post_id,
                               status_code=404,
                               payload=case.payload,
                               expected_success=False)

    @allure.suite("Like post")
    @allure.story("User can like existed post")
    @allure.description("Like post - Incorrect post id")
    @pytest.mark.parametrize("case", [
        pytest.param(LikePostByRoleTestCase(role="admin", payload=LikePostPayload(reaction="like")),
                     id="Attempt to add reaction - not existed post"),
    ])
    def test_like_post_invalid_uuid(self, case):
        """Attempt to like post with Incorrect uuid"""
        prepared_post_id = self.data_helper.get_invalid_uuid()
        like_service = self.get_actor(case.role).likes_api

        like_service.like_post(post_id=prepared_post_id,
                               status_code=422,
                               payload=case.payload,
                               expected_success=False)

    @allure.suite("Like post")
    @allure.story("User can like existed post")
    @allure.description("Like post - comment_id instead of post_id")
    @pytest.mark.parametrize("case", [
        pytest.param(LikePostByRoleTestCase(role="admin", payload=LikePostPayload(reaction="like")),
                     id="Attempt to add reaction - not existed post"),
    ])
    def test_like_post_incorrect_comment_in_use(self, case, build_comment_remove):
        """Attempt to like post with id of existed comment"""
        prepared_post_id = build_comment_remove(case.role)
        like_service = self.get_actor(case.role).likes_api

        like_service.like_post(post_id=prepared_post_id,
                               status_code=404,
                               payload=case.payload,
                               expected_success=False)

    @allure.suite("Like post")
    @allure.story("User can like existed post")
    @pytest.mark.testing
    @allure.description("Like post - reaction already liked")
    @pytest.mark.parametrize("case", [
        pytest.param(LikePostByRoleTestCase(role="user_bob", payload=LikePostPayload(reaction="like")),
                     id="Attempt to add reaction - reaction already added"),
    ])
    def test_like_post_already_liked(self, build_post_like_remove, case):
        """Attempt to like post, that already liked"""
        prepared_post_id = build_post_like_remove(case.role, reaction=case.payload.reaction)
        like_service = self.get_actor(case.role).likes_api

        like_service.like_post(post_id=prepared_post_id,
                               status_code=409,
                               payload=case.payload,
                               expected_success=False)

    @allure.suite("Like post")
    @allure.story("User can like existed post")
    @allure.description("Like post - reaction already added, add new reaction")
    @pytest.mark.parametrize("case", [
        pytest.param(LikePostByRoleTestCase(role="user_bob", payload=LikePostPayload(reaction="like")),
                     id="Attempt to add reaction - reaction already added, add new reaction"),
    ])
    def test_like_post_already_liked(self, build_post_like_remove, case):
        """Attempt to like post, that already liked"""
        prepared_post_id = build_post_like_remove(case.role, reaction="love")
        like_service = self.get_actor(case.role).likes_api

        like_service.like_post(post_id=prepared_post_id,
                               status_code=409,
                               payload=case.payload,
                               expected_success=False)

    @allure.suite("Unlike post")
    @allure.story("User can unlike existed post")
    @allure.description("Unlike post - valid")
    @pytest.mark.parametrize("case_user", [
        pytest.param("admin", id="Remove reaction from post - admin"),
        pytest.param("user_eve", id="Remove reaction from post - user"),
        pytest.param("moderator", id="Remove reaction from post - moderator")
    ])
    def test_unlike_post(self, build_post_like_remove, case_user):
        prepared_post_id = build_post_like_remove(case_user)
        app_services = self.get_actor(case_user)
        post_service = app_services.posts_api
        like_service = app_services.likes_api

        post_before = post_service.get_post(post_id=prepared_post_id)

        like_service.unlike_post(post_id=prepared_post_id)

        post_after = post_service.get_post(post_id=prepared_post_id)
        assert post_before.likes_count == post_after.likes_count + 1

    @allure.suite("Unlike post")
    @allure.story("User can unlike existed post")
    @allure.description("Unlike post - invalid post id")
    @pytest.mark.parametrize("case_user", [
        pytest.param("user_bob", id="Remove reaction from post  - invalid post id"),
    ])
    def test_unlike_post_invalid_id(self, case_user):
        """Attempt to like comment instead of post"""
        prepared_post_id = self.data_helper.get_invalid_uuid()
        like_service = self.get_actor(case_user).likes_api

        like_service.unlike_post(post_id=prepared_post_id,
                                 status_code=422,
                                 expected_success=False)

    @allure.suite("Unlike post")
    @allure.story("User can unlike existed post")
    @allure.description("Unlike post - not existed post")
    @pytest.mark.parametrize("case_user", [
        pytest.param("user_bob", id="Remove reaction from post  - not existing post"),
    ])
    def test_unlike_post_not_existed(self, case_user):
        """Attempt to unlike not existing post"""
        prepared_post_id = self.data_helper.get_not_existed_uuid()
        like_service = self.get_actor(case_user).likes_api

        like_service.unlike_post(post_id=prepared_post_id,
                                 status_code=404,
                                 expected_success=False)

    @allure.suite("Unlike post")
    @allure.story("User can unlike existed post")
    @allure.description("Unlike post - removed post")
    @pytest.mark.parametrize("case_user", [
        pytest.param("user_bob", id="Remove reaction from post  - not existed post"),
    ])
    def test_unlike_post_removed(self, case_user, get_removed_post):
        """Attempt to unlike the liked removed post, invalid post id"""
        prepared_post_id = get_removed_post(case_user)
        like_service = self.get_actor(case_user).likes_api
        like_service.unlike_post(post_id=prepared_post_id, expected_success=False, status_code=404)

    @allure.suite("Unlike post")
    @allure.story("User can unlike existed post")
    @allure.description("Unlike post - not liked post")
    @pytest.mark.parametrize("case_user", [
        pytest.param("user_bob", id="Remove reaction from post  - not liked post"),
    ])
    def test_unlike_post_not_liked(self, case_user, build_post_remove):
        """Attempt to unlike the liked removed post, invalid post id"""
        prepared_post_id = build_post_remove(case_user)
        like_service = self.get_actor(case_user).likes_api
        like_service.unlike_post(post_id=prepared_post_id, expected_success=False, status_code=404)

    @allure.suite("Get post likes")
    @allure.story("User can see existed post reactions")
    @allure.description("Get post likes")
    @pytest.mark.testing
    @pytest.mark.not_checked
    @pytest.mark.parametrize("case", [
        pytest.param(GetPostLikesByRoleTestCase(role="user_eve", params=GetPostLikesParams(page=1, per_page=1)),
                     id=" per_page - valid minimum boundary"),
        pytest.param(GetPostLikesByRoleTestCase(role="moderator", params=GetPostLikesParams(page=2, per_page=100)),
                     id="per_page - valid maximum boundary"),
        pytest.param(GetPostLikesByRoleTestCase(role="admin", params=GetPostLikesParams()),
                     id="empty query param"),
    ])
    def test_get_post_reactions(self, get_post_with_likes, case):
        """Get post with likes and reactions depends on roles"""
        api_services = self.get_actor(case.role)
        like_service = api_services.likes_api
        prepared_post_id = get_post_with_likes(api_services.posts_api)
        like_service.get_post_likes(post_id=prepared_post_id, params=case.params)

    @allure.suite("Get post likes")
    @allure.story("User can see existed post reactions")
    @allure.description("Get post likes - incorrect query param")
    @pytest.mark.testing
    @pytest.mark.not_checked
    @pytest.mark.parametrize("case", [
        pytest.param(GetPostLikesByRoleTestCase(role="user_eve", params=GetPostLikesParams(page=0, per_page=10)),
                     id=" Invalid page below minimum boundary"),
        pytest.param(GetPostLikesByRoleTestCase(role="user_bob", params=GetPostLikesParams(page=1, per_page=0)),
                     id="Invalid per_page below minimum boundary"),
        pytest.param(GetPostLikesByRoleTestCase(role="admin", params=GetPostLikesParams(page=1, per_page=101)),
                     id="Invalid per_page above maximum boundary"),
    ])
    def test_get_post_reactions_invalid_params(self, get_post_with_likes, case):
        """Get post with likes - incorrect query param"""
        api_services = self.get_actor(case.role)
        like_service = api_services.likes_api
        prepared_post_id = get_post_with_likes(api_services.posts_api)
        like_service.get_post_likes(post_id=prepared_post_id,
                                    params=case.params,
                                    expected_success=False,
                                    status_code=422
                                    )

    @allure.suite("Get post likes")
    @allure.story("User can see existed post reactions")
    @pytest.mark.testing
    @pytest.mark.not_checked
    @allure.description("Get post likes - incorrect post id, Comment instead of post")
    def test_get_post_reactions_comment_in_use(self, build_comment_remove):
        """Attempt to get post likes, when comment id is used"""
        prepared_post_id = build_comment_remove("user_eve")
        like_service = self.get_actor("user_eve").likes_api
        like_service.get_post_likes(post_id=prepared_post_id, params=GetPostLikesParams(), expected_success=True,
                                    status_code=200)

    @allure.suite("Get post likes")
    @allure.story("User can see existed post reactions")
    @allure.description("Get post likes - Post doesn't exist ")
    @pytest.mark.testing
    @pytest.mark.not_checked
    def test_get_post_reactions_not_exist(self):
        """Attempt to get reactions list, when  post id doesn't exist"""
        prepared_post_id = self.data_helper.get_not_existed_uuid()
        like_service = self.get_actor("user_eve").likes_api
        like_service.get_post_likes(post_id=prepared_post_id, params=GetPostLikesParams(), expected_success=True,
                                    status_code=200)

    @allure.suite("Get post likes")
    @allure.story("User can see existed post reactions")
    @allure.description("Get post likes - post is deleted")
    @pytest.mark.testing
    @pytest.mark.not_checked
    def test_get_post_reactions_removed_post(self, get_removed_post):
        """Attempt to get reactions list when post is deleted"""
        prepared_post_id = get_removed_post("user_eve")
        like_service = self.get_actor("user_eve").likes_api
        like_service.get_post_likes(post_id=prepared_post_id, params=GetPostLikesParams(), expected_success=False,
                                    status_code=422)

    @allure.suite("Get post likes")
    @allure.story("User can see existed post reactions")
    @pytest.mark.testing
    @pytest.mark.not_checked
    @allure.description("Get post likes - incorrect post id")
    def test_get_post_reactions_incorrect_post_uuid(self):
        """Attempt to get reactions list when post id is incorrect"""
        prepared_post_id = self.data_helper.get_invalid_uuid()
        like_service = self.get_actor("user_eve").likes_api
        like_service.get_post_likes(post_id=prepared_post_id, params=GetPostLikesParams(), expected_success=False,
                                    status_code=422)

    @allure.suite("Like comment")
    @allure.story("User can like existed comment")
    @allure.description("Like comment depends on role")
    @pytest.mark.testing
    @pytest.mark.not_checked
    @pytest.mark.parametrize("case", [
        pytest.param(LikeCommentByRoleTestCase(role="admin", payload=LikeCommentPayload(reaction="like")),
                     id="Add reaction to post as admin - like"),
        pytest.param(LikeCommentByRoleTestCase(role="user_eve", payload=LikeCommentPayload(reaction="love")),
                     id="Add reaction to post as user - love"),
        pytest.param(LikeCommentByRoleTestCase(role="user_eve", payload=LikeCommentPayload(reaction="sad")),
                     id="Add reaction to post as user - sad"),
        pytest.param(LikeCommentByRoleTestCase(role="user_bob", payload=LikeCommentPayload(reaction="wow")),
                     id="Add reaction to post as user - wow"),
        pytest.param(LikeCommentByRoleTestCase(role="user_bob", payload=LikeCommentPayload(reaction="love")),
                     id="Add reaction to post as user - love"),
        pytest.param(LikeCommentByRoleTestCase(role="moderator", payload=LikeCommentPayload(reaction="angry")),
                     id="Add reaction to post as user - angry"),
    ])
    def test_like_comment(self, build_comment_remove, case):
        """Attempt to like comment depends on role"""
        prepared_comment_id = build_comment_remove(case.role)
        like_service = self.get_actor(case.role).likes_api

        like = like_service.like_comment(comment_id=prepared_comment_id, payload=case.payload)
        assert like.reaction == case.payload.reaction

    @allure.suite("Like comment")
    @allure.story("User can like existed comment")
    @allure.description("Like comment - invalid payload")
    @pytest.mark.testing
    @pytest.mark.not_checked
    @pytest.mark.parametrize("case", [
        pytest.param(LikeCommentByRoleTestCase(role="admin", payload=LikeCommentPayload(reaction="busy")),
                     id="Add not allowed reaction to comment"),
        pytest.param(LikeCommentByRoleTestCase(role="user_bob", payload=LikeCommentPayload(reaction="")),
                     id="Add empty string as reaction to post"),
        pytest.param(LikeCommentByRoleTestCase(role="user_eve", payload=LikeCommentPayload()),
                     id="Unexpected Empty payload")
    ])
    def test_like_comment_invalid_payload(self, case, build_comment_remove):
        """Attempt to like comment depends on role"""

        prepared_comment_id = build_comment_remove(case.role)
        like_service = self.get_actor("user_eve").likes_api

        like_service.like_comment(comment_id=prepared_comment_id,
                                  payload=case.payload,
                                  status_code=422,
                                  expected_success=False)

    @allure.suite("Like comment")
    @allure.story("User can like existed comment")
    @pytest.mark.testing
    @pytest.mark.not_checked
    @allure.description("Like comment, incorrect -  Post id in use")
    def test_like_comment_incorrect_post_in_use(self, build_post_remove):
        """Attempt to like comment, when id is post id"""
        prepared_comment_id = build_post_remove("user_eve")
        like_service = self.get_actor("user_eve").likes_api
        like_service.like_comment(comment_id=prepared_comment_id, payload=LikeCommentPayload(), status_code=404,
                                  expected_success=False)

    @allure.suite("Like comment")
    @allure.story("User can like existed comment")
    @allure.description("Like comment -  Comment doesn't exist")
    def test_like_comment_not_existed(self):
        """Attempt to like comment, comment doesn't exist"""
        prepared_comment_id = self.data_helper.get_not_existed_uuid()
        like_service = self.get_actor("user_eve").likes_api
        like_service.like_comment(comment_id=prepared_comment_id,
                                  payload=LikeCommentPayload(),
                                  status_code=404,
                                  expected_success=False)

    @allure.suite("Like comment")
    @allure.story("User can like existed comment")
    @pytest.mark.testing
    @pytest.mark.not_checked
    @allure.description("Like comment - Comment is deleted")
    def test_like_comment_removed(self, get_removed_comment):
        """Attempt to like comment, Comment is deleted"""
        prepared_comment_id = get_removed_comment("user_eve")
        like_service = self.get_actor("user_eve").likes_api
        like_service.like_comment(comment_id=prepared_comment_id,
                                  payload=LikeCommentPayload(),
                                  status_code=404,
                                  expected_success=False)

    @allure.suite("Like comment")
    @allure.story("User can like existed comment")
    @pytest.mark.testing
    @pytest.mark.not_checked
    @allure.description("Like comment - Incorrect Comment id")
    def test_like_comment_invalid_uuid(self):
        """Attempt to like comment,Incorrect Comment id"""
        prepared_comment_id = self.data_helper.get_invalid_uuid()
        like_service = self.get_actor("user_eve").likes_api
        like_service.like_comment(comment_id=prepared_comment_id,
                                  payload=LikeCommentPayload(),
                                  status_code=422,
                                  expected_success=False)

    @allure.suite("Like comment")
    @allure.story("User can like existed comment")
    @allure.description("Like comment - Comment is already liked")
    def test_like_comment_already_liked(self, build_comment_like_remove):
        """Attempt to like comment, Comment is already liked"""
        prepared_comment_id = build_comment_like_remove("user_eve")
        like_service = self.get_actor("user_eve").likes_api
        like_service.like_comment(comment_id=prepared_comment_id,
                                  payload=LikeCommentPayload(),
                                  status_code=409,
                                  expected_success=False)

    @allure.suite("Unlike comment")
    @allure.story("User can unlike existed comment")
    @allure.description("Unike comment - valid")
    @pytest.mark.testing
    @pytest.mark.not_checked
    @pytest.mark.parametrize("case", [
        pytest.param("admin", id="Remove reaction from post as admin"),
        pytest.param("user_eve", id="Remove reaction from post as user"),
        pytest.param("moderator", id="Remove reaction from post as moderator"),
    ])
    def test_unlike_comment(self, build_comment_like_remove, case):
        """Unike comment"""
        like_service = self.get_actor(case).likes_api
        prepared_post_id = build_comment_like_remove(case)
        like_service.unlike_comment(comment_id=prepared_post_id)

    @allure.suite("Unlike comment")
    @allure.story("User can unlike existed comment")
    @pytest.mark.testing
    @pytest.mark.not_checked
    @allure.description("Unike comment, incorrect - Comment instead of post")
    def test_unlike_comment_post_in_use(self, build_post_like_remove):
        """Unike comment - invalid comment id, Post instead of comment"""

        prepared_post_id = build_post_like_remove("user_eve")
        like_service = self.get_actor("user_eve").likes_api
        like_service.unlike_comment(comment_id=prepared_post_id, expected_success=False, status_code=404)

    @allure.suite("Unlike comment")
    @allure.story("User can unlike existed comment")
    @pytest.mark.testing
    @pytest.mark.not_checked
    @allure.description("Unike comment, incorrect - Post doesn't exist")
    def test_unlike_comment_not_existed(self):
        """Unike comment - invalid comment id, Post doesn't exist"""

        prepared_post_id = self.data_helper.get_not_existed_uuid()
        like_service = self.get_actor("user_eve").likes_api
        like_service.unlike_comment(comment_id=prepared_post_id, expected_success=False, status_code=404)

    @allure.suite("Unlike comment")
    @allure.story("User can unlike existed comment")
    @allure.description("Unike comment, incorrect - Incorrect comment id")
    def test_unlike_comment_invalid_uuid(self):
        """Unike comment - Incorrect comment id"""

        prepared_comment_id = self.data_helper.get_invalid_uuid()
        like_service = self.get_actor("user_eve").likes_api
        like_service.unlike_comment(comment_id=prepared_comment_id,
                                              expected_success=False,
                                              status_code=422
                                              )

    @allure.suite("Unlike comment")
    @allure.story("User can unlike existed comment")
    @allure.description("Unike comment, incorrect - Comment is deleted")
    def test_unlike_comment_removed(self, get_removed_comment):
        """Unike comment - Comment is deleted"""

        prepared_comment_id = get_removed_comment("user_eve")
        like_service = self.get_actor("user_eve").likes_api
        like_service.unlike_comment(comment_id=prepared_comment_id, expected_success=False, status_code=404)
