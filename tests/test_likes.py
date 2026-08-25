import allure
import faker
import pytest

from config.base_test import BaseTest


@allure.epic("Likes Service")
@allure.feature("Likes")
@allure.parent_suite("Tests Likes service API")
@allure.title("Tests Likes service API")
class TestLikes(BaseTest):


    @allure.suite("Like post")
    @allure.story("User can like existed post")
    @allure.description("Like post - valid")
    @pytest.mark.parametrize("create_remove_post_by_user, test_data", [
        pytest.param({"create_by": "admin"}, {"user":"admin", "payload":{'reaction': 'like'}},
                     id="Add reaction to post as admin"),
        # pytest.param({"create_by": "user_eve"}, {"user":"user_eve", "payload":{'reaction': 'love'}},
        #              id="Add reaction to post as user"),
        # pytest.param({"create_by": "user_eve"}, {"user":"user_eve", "payload":{'reaction': 'wow'}},
        #              id="Add reaction to post as user"),
        # pytest.param({"create_by": "user_eve"}, {"user":"user_eve", "payload":{'reaction': 'sad'}},
        #              id="Add reaction to post as user"),
        # pytest.param({"create_by": "user_eve"}, {"user":"user_eve", "payload":{'reaction': 'love'}},
        #              id="Add reaction to post as user"),
        # pytest.param({"create_by": "moderator"}, {"user":"moderator", "payload":{'reaction': 'angry'}},
        #              id="Add reaction to post as moderator"),
        ], indirect=["create_remove_post_by_user"])
    def test_like_post(self, create_remove_post_by_user, test_data):
        prepared_post_id = create_remove_post_by_user
        user = self.get_actor(test_data["user"])
        post_before = user.posts_api.get_post(post_id=prepared_post_id)
        like = user.likes_api.like_post(post_id=prepared_post_id, payload=test_data["payload"])
        assert like.reaction == test_data["payload"]["reaction"]
        post_after = user.posts_api.get_post(post_id=prepared_post_id)
        assert post_before.likes_count == post_after.likes_count - 1



    @allure.suite("Like post")
    @allure.story("User can like existed post")
    @allure.description("Like post - invalid payload")
    @pytest.mark.parametrize("test_data", [
        pytest.param({"user":"user_eve", "payload":{'reaction': 'busy'}, "expected_success": False, "status_code": 422,},
                     id="Add not allowed reaction to post"),
        pytest.param({"user":"user_eve", "payload":{'reaction': ''}, "expected_success": False, "status_code": 422},
                     id="Add empty string as reaction to post"),
        pytest.param({"user":"user_eve", "payload":{}, "expected_success": False, "status_code": 422},
                     id="Unexpected Empty payload"),
        ])
    def test_like_post_invalid_reaction(self, test_data):
        prepared_post_id = self.data_helper.get_not_existed_uuid()
        user = self.get_actor(test_data["user"])
        user.likes_api.like_post(post_id=prepared_post_id,
                                 payload=test_data["payload"],
                                 status_code=test_data["status_code"],
                                 expected_success=test_data["expected_success"])



    @allure.suite("Like post")
    @allure.story("User can like existed post")
    @allure.description("Like post - invalid post_id, Post doesn't exist")
    def test_like_post_incorrect_not_existed(self):
        """Attempt to like post with not existed uuid"""
        prepared_post_id = self.data_helper.get_not_existed_uuid()
        user = self.get_actor("user_eve")
        user.likes_api.like_post(post_id=prepared_post_id,
                                 status_code=404,
                                 payload={},
                                 expected_success=False)


    @allure.suite("Like post")
    @allure.story("User can like existed post")
    @allure.description("Like post - Incorrect post id")
    def test_like_post_incorrect_invalid_uuid(self):
        """Attempt to like post with Incorrect uuid"""
        prepared_post_id = self.data_helper.get_invalid_uuid()
        user = self.get_actor("user_eve")
        user.likes_api.like_post(post_id=prepared_post_id,
                                 status_code=422,
                                 payload={},
                                 expected_success=False)


    @allure.suite("Like post")
    @allure.story("User can like existed post")
    @allure.description("Like post, incorrect -  Post is deleted")
    def test_like_post_removed(self, get_removed_post):
        """Attempt to like deleted post (is_deleted is True)"""
        user = self.get_actor("user_eve")
        prepared_post_id = get_removed_post("user_eve")
        user.likes_api.like_post(post_id=prepared_post_id,
                                 status_code=404,
                                 payload={},
                                 expected_success=False)



    @allure.suite("Like post")
    @allure.story("User can like existed post")
    @allure.description("Like post - invalid post_id")
    def test_like_post_incorrect_comment_in_use(self, create_comment_before, comment_cleaner):
        """Attempt to like post with id of existed comment"""
        prepared_post_id = create_comment_before("user_eve")
        user = self.get_actor("user_eve")
        comment_cleaner(prepared_post_id, "user_eve")
        user.likes_api.like_post(post_id=prepared_post_id,
                                 status_code=404,
                                 payload={},
                                 expected_success=False)


    @allure.suite("Like post")
    @allure.story("User can like existed post")
    @allure.description("Like post - invalid post_id, already liked")
    def test_like_post_already_liked(self, like_post_before, post_like_cleaner):
        """Attempt to like post, that already liked"""
        prepared_post_id = like_post_before("user_bob")
        user = self.get_actor("user_bob")
        post_like_cleaner(prepared_post_id, "user_bob")
        user.likes_api.like_post(post_id=prepared_post_id,
                                 status_code=409,
                                 payload={},
                                 expected_success=False)


    @allure.suite("Unlike post")
    @allure.story("User can unlike existed post")
    @allure.description("Unlike post - valid")
    @pytest.mark.parametrize("test_data", [
        pytest.param({"user":"admin"},id="Remove reaction from post as admin"),
        pytest.param({"user":"user_eve"},id="Remove reaction from post as user"),
        pytest.param({"user":"moderator"},id="Remove reaction from post as moderator"),
        ])
    def test_unlike_post(self, like_post_before, test_data, post_like_setter):
        prepared_post_id = like_post_before(test_data["user"])
        user = self.get_actor(test_data["user"])

        post_like_setter(prepared_post_id, test_data["user"])
        post_before = user.posts_api.get_post(post_id=prepared_post_id)

        user.likes_api.unlike_post(post_id=prepared_post_id)

        post_after = user.posts_api.get_post(post_id=prepared_post_id)
        assert post_before.likes_count == post_after.likes_count + 1



    @allure.suite("Unlike post")
    @allure.story("User can unlike existed post")
    @allure.description("Unlike post - invalid post id")
    def test_unlike_post_incorrect_comment_in_use(self, get_liked_comment, comment_like_setter):
        """Attempt to like comment instead of post"""
        prepared_post_id = get_liked_comment
        user = self.get_actor("user_eve")
        comment_like_setter(prepared_post_id, "user_eve")
        user.likes_api.unlike_post(post_id=prepared_post_id,expected_success=False,status_code=404)



    @allure.suite("Unlike post")
    @allure.story("User can unlike existed post")
    @allure.description("Unlike post - not existing post")
    def test_unlike_post_incorrect_not_existed(self):
        """Attempt to unlike not existing post"""
        prepared_post_id = self.data_helper.get_not_existed_uuid()
        user = self.get_actor("user_eve")
        user.likes_api.unlike_post(post_id=prepared_post_id, expected_success=False, status_code=404)



    @allure.suite("Unlike post")
    @allure.story("User can unlike existed post")
    @allure.description("Unlike post - invalid post id")
    def test_unlike_post_incorrect_post_removed(self, get_not_liked_post_before):
        """Attempt to unlike the liked removed post, invalid post id"""
        prepared_post_id = get_not_liked_post_before("user_bob")
        user = self.get_actor("user_bob")
        user.likes_api.unlike_post(post_id=prepared_post_id, expected_success=False, status_code=404)






    @allure.suite("Get post likes")
    @allure.story("User can see existed post reactions")
    @allure.description("Get post likes")
    @pytest.mark.parametrize("test_data", [
        pytest.param({"user":"user_eve", "params": {"page": 1, "per_page": 1}},
                     id="valid minimum boundaries"),
        pytest.param({"user":"moderator","params": {"page": 2, "per_page": 100}},
                     id="valid maximum boundary"),
        pytest.param({"user":"admin","params": {}},
                     id="empty query param"),
    ])
    def test_get_post_reactions(self, get_post_with_likes, test_data):
        """Get post with likes and reactions depends on roles"""
        prepared_post_id = get_post_with_likes(test_data["user"])
        user = self.get_actor(test_data["user"])
        user.likes_api.get_post_likes(post_id=prepared_post_id,params=test_data["params"])



    @allure.suite("Get post likes")
    @allure.story("User can see existed post reactions")
    @allure.description("Get post likes - incorrect query param")
    @pytest.mark.parametrize("test_data", [
        pytest.param({"user": "user_eve", "params": {"page": 0, "per_page": 10}, "expected_success": False, "status_code": 422},
                     id="Invalid page below minimum boundary"),
        pytest.param({"user": "user_eve", "params": {"page": 1, "per_page": 0}, "expected_success": False, "status_code": 422},
                     id="Invalid per_page below minimum boundary"),
        pytest.param({"user": "user_eve", "params": {"page": 3, "per_page": 101}, "expected_success": False, "status_code": 422},
                     id="Invalid per_page above maximum boundary"),
    ])
    def test_get_post_reactions_invalid_params(self, test_data):
        """Get post with likes - incorrect query param"""

        prepared_post_id = faker.Faker().uuid4()
        user = self.get_actor(test_data["user"])
        user.likes_api.get_post_likes(post_id=prepared_post_id,
                                      params=test_data["params"],
                                      expected_success=test_data["expected_success"],
                                      status_code=test_data["status_code"]
)



    @allure.suite("Get post likes")
    @allure.story("User can see existed post reactions")
    @allure.description("Get post likes - incorrect post id, Comment instead of post")
    def test_get_post_reactions_incorrect_post_comment_in_use(self, get_comment_only):
        """Attempt to get post likes, when comment id is used"""
        prepared_post_id = get_comment_only("user_eve")
        user = self.get_actor("user_eve")
        user.likes_api.get_post_likes(post_id=prepared_post_id,params={},expected_success=True,status_code=200)



    @allure.suite("Get post likes")
    @allure.story("User can see existed post reactions")
    @allure.description("Get post likes - incorrect post id, Post doesn't exist ")
    def test_get_post_reactions_incorrect_not_exist(self):
        """Attempt to get reactions list, when  post id doesn't exist"""
        prepared_post_id = self.data_helper.get_not_existed_uuid
        user = self.get_actor("user_eve")
        user.likes_api.get_post_likes(post_id=prepared_post_id,params={},expected_success=True,status_code=200)



    @allure.suite("Get post likes")
    @allure.story("User can see existed post reactions")
    @allure.description("Get post likes - post is deleted")
    def test_get_post_reactions_incorrect_removed(self, get_removed_post):
        """Attempt to get reactions list when post is deleted"""
        prepared_post_id = get_removed_post("user_eve")
        user = self.get_actor("user_eve")
        user.likes_api.get_post_likes(post_id=prepared_post_id,params={},expected_success=True,status_code=200)



    @allure.suite("Get post likes")
    @allure.story("User can see existed post reactions")
    @allure.description("Get post likes - incorrect post id")
    def test_get_post_reactions_incorrect_incorrect_uuid(self, get_incorrect_post):
        """Attempt to get reactions list when post id is incorrect"""
        prepared_post_id = self.data_helper.get_invalid_uuid()
        user = self.get_actor("user_eve")
        user.likes_api.get_post_likes(post_id=prepared_post_id,params={},expected_success=False,status_code=422)



    @allure.suite("Like comment")
    @allure.story("User can like existed comment")
    @allure.description("Like comment")
    @pytest.mark.parametrize("test_data", [
        pytest.param( {"user":"admin", "payload":{'reaction': 'like'}},
                     id="Add reaction to post as admin"),
        pytest.param({"user":"user_eve", "payload":{'reaction': 'love'}},
                     id="Add reaction to post as user"),
        pytest.param( {"user":"moderator", "payload":{'reaction': 'angry'}},
                     id="Add reaction to post as moderator"),
        ])
    def test_like_comment(self, get_comment_only, test_data, like_comment_cleaner):
        """Attempt to like comment depends on role"""

        prepared_comment_id = get_comment_only(test_data["user"])
        user = self.get_actor(test_data["user"])

        like_comment_cleaner(comment_id=prepared_comment_id, role=test_data["user"])

        like = user.likes_api.like_comment(comment_id=prepared_comment_id, payload=test_data["payload"])
        assert like.reaction == test_data["payload"]["reaction"]




    @allure.suite("Like comment")
    @allure.story("User can like existed comment")
    @allure.description("Like comment - invalid payload")
    @pytest.mark.parametrize("test_data", [
        pytest.param({"payload":{'reaction': 'busy'}, "expected_success": False, "status_code": 422,},
                     id="Add not allowed reaction to post"),
        pytest.param({"payload":{'reaction': ''}, "expected_success": True, "status_code": 201},
                     id="Add empty string as reaction to post"),
        pytest.param({"payload":{}, "expected_success": True, "status_code": 201},
                     id="Unexpected Empty payload"),
        ])
    def test_like_comment_invalid_payload(self, get_comment_only, test_data,like_comment_cleaner):
        """Attempt to like comment depends on role"""

        prepared_comment_id = get_comment_only("user_eve")
        user = self.get_actor("user_eve")
        if test_data["status_code"] == 201:
            like_comment_cleaner(comment_id=prepared_comment_id, role="user_eve")
        user.likes_api.like_comment(comment_id=prepared_comment_id,
                                 payload=test_data["payload"],
                                 status_code=test_data["status_code"],
                                 expected_success=test_data["expected_success"])



    @allure.suite("Like comment")
    @allure.story("User can like existed comment")
    @allure.description("Like comment, incorrect -  Post id in use")
    def test_like_comment_incorrect_post_in_use(self, get_post_only):
        """Attempt to like comment, when id is post id"""
        prepared_comment_id = get_post_only("user_eve")
        user = self.get_actor("user_eve")
        user.likes_api.like_comment(comment_id=prepared_comment_id,status_code=404,payload={},expected_success=False)




    @allure.suite("Like comment")
    @allure.story("User can like existed comment")
    @allure.description("Like comment, incorrect -  Comment doesn't exist")
    def test_like_comment_incorrect_not_exists(self, get_incorrect_comment):
        """Attempt to like comment, comment doesn't exist"""
        prepared_comment_id = self.data_helper.get_not_existed_uuid()
        user = self.get_actor("user_eve")
        user.likes_api.like_comment(comment_id=prepared_comment_id,
                                 status_code=404,
                                 payload={},
                                 expected_success=False)



    @allure.suite("Like comment")
    @allure.story("User can like existed comment")
    @allure.description("Like comment - invalid comment, Comment is deleted")
    def test_like_comment_incorrect_removed(self, create_comment_and_remove_before):
        """Attempt to like comment, Comment is deleted"""
        prepared_comment_id = create_comment_and_remove_before("user_eve")
        user = self.get_actor("user_eve")
        user.likes_api.like_comment(comment_id=prepared_comment_id,
                                 status_code=404,
                                 payload={},
                                 expected_success=False)


    @allure.suite("Like comment")
    @allure.story("User can like existed comment")
    @allure.description("Like comment - invalid comment, Incorrect Comment id")
    def test_like_comment_incorrect_invalid_uuid(self, get_incorrect_comment):
        """Attempt to like comment,Incorrect Comment id"""
        prepared_comment_id = self.data_helper.get_invalid_uuid()
        user = self.get_actor("user_eve")
        user.likes_api.like_comment(comment_id=prepared_comment_id,
                                 status_code=422,
                                 payload={},
                                 expected_success=False)

    @allure.suite("Like comment")
    @allure.story("User can like existed comment")
    @allure.description("Like comment - invalid comment, Comment is already liked")
    def test_like_comment_incorrect_already_liked(self, get_liked_comment_before, test_data, like_comment_cleaner):
        """Attempt to like comment, Comment is already liked"""
        prepared_comment_id = get_liked_comment_before("user_eve")
        user = self.get_actor(test_data["user"])
        user.likes_api.like_comment(comment_id=prepared_comment_id,
                                 status_code=409,
                                 payload={},
                                 expected_success=False)
        like_comment_cleaner(prepared_comment_id)



    @allure.suite("Unlike comment")
    @allure.story("User can unlike existed comment")
    @allure.description("Unike comment - valid")
    @pytest.mark.parametrize("test_data", [
        pytest.param({"user":"admin"},
                     id="Remove reaction from post as admin"),
        pytest.param({"user":"user_eve"},
                     id="Remove reaction from post as user"),
        pytest.param({"user":"moderator"},
                     id="Remove reaction from post as moderator"),
        ])
    def test_unlike_comment(self, get_liked_comment_before,comment_like_setter, test_data):
        """Unike comment"""

        prepared_post_id = get_liked_comment_before(test_data["user"])
        user = self.get_actor(test_data["user"])
        user.likes_api.unlike_comment(comment_id=prepared_post_id)
        comment_like_setter(prepared_post_id, test_data["user"])



    @allure.suite("Unlike comment")
    @allure.story("User can unlike existed comment")
    @allure.description("Unike comment, incorrect - Comment instead of post")
    def test_unlike_comment_incorrect_post_in_use(self, get_liked_post_before):
        """Unike comment - invalid comment id, Post instead of comment"""

        prepared_post_id = get_liked_post_before
        user = self.get_actor("user_eve")
        user.likes_api.unlike_comment(comment_id=prepared_post_id,expected_success=False,status_code=404)



    @allure.suite("Unlike comment")
    @allure.story("User can unlike existed comment")
    @allure.description("Unike comment, incorrect - Post doesn't exist")
    def test_unlike_comment_incorrect_not_exist(self, get_incorrect_comment):
        """Unike comment - invalid comment id, Post doesn't exist"""

        prepared_post_id = self.data_helper.get_not_existed_uuid()
        user = self.get_actor("user_eve")
        user.likes_api.unlike_comment(comment_id=prepared_post_id,expected_success=False,status_code=404)





    @allure.suite("Unlike comment")
    @allure.story("User can unlike existed comment")
    @allure.description("Unike comment, incorrect - Incorrect comment id")
    def test_unlike_comment_incorrect_invalid_uuid(self):
        """Unike comment - Incorrect comment id"""

        prepared_comment_id = self.data_helper.get_invalid_uuid()
        user = self.get_actor("user_eve")
        user.likes_api.unlike_comment(comment_id=prepared_comment_id,
                                   expected_success=False,
                                   status_code=422
                                   )




    @allure.suite("Unlike comment")
    @allure.story("User can unlike existed comment")
    @allure.description("Unike comment, incorrect - Comment is deleted")
    def test_unlike_comment_incorrect_removed(self, create_comment_and_remove_before):
        """Unike comment - Comment is deleted"""

        prepared_comment_id = create_comment_and_remove_before("user_eve")
        user = self.get_actor("user_eve")
        user.likes_api.unlike_comment(comment_id=prepared_comment_id,expected_success=False,status_code=404)




    @allure.suite("Unlike comment")
    @allure.story("User can unlike existed comment")
    @allure.description("Unike comment, incorrect - invalid comment id")
    def test_unlike_comment_incorrect_post_in_use(self, get_comment_only):
        """Unike comment - Comment is deleted"""

        prepared_comment_id = get_comment_only("user_bob")
        user = self.get_actor("user_bob")
        user.likes_api.unlike_comment(comment_id=prepared_comment_id,expected_success=False,status_code=404)



