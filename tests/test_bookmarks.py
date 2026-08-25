import allure
import pytest

from config.base_test import BaseTest


@allure.epic("Bookmarks Service")
@allure.feature("Bookmarks")
@allure.parent_suite("Tests Bookmarks service API")
@allure.title("Tests Bookmarks service API")
class TestBookmarks(BaseTest):

    @allure.suite("Get user's bookmarks list")
    @allure.story("User can read added bookmarks")
    @allure.description("Get bookmarks list")
    @pytest.mark.parametrize("test_data", [
        pytest.param({"user": "user_eve", "params": {"page": 1, "per_page": 1}},
                     id="valid minimum boundaries"),
        pytest.param({"user": "moderator", "params": {"page": 2, "per_page": 100}},
                     id="valid maximum boundary"),
        pytest.param({"user": "admin", "params": {}},
                     id="empty query param"),
    ])
    def test_get_bookmarks_list(self, test_data):
        user = self.get_actor(test_data["user"])
        user.bookmarks_api.get_bookmarks(params=test_data["params"])

    @allure.suite("Get user's bookmarks list")
    @allure.story("User can read added bookmarks")
    @allure.description("Get bookmarks list - incorrect query params")
    @pytest.mark.parametrize("test_data", [
        pytest.param(
            {"user": "user_eve", "params": {"page": 0, "per_page": 10}, "expected_success": False, "status_code": 422},
            id="Invalid page below minimum boundary"),
        pytest.param(
            {"user": "user_eve", "params": {"page": 1, "per_page": 0}, "expected_success": False, "status_code": 422},
            id="Invalid per_page below minimum boundary"),
        pytest.param(
            {"user": "user_eve", "params": {"page": 3, "per_page": 101}, "expected_success": False, "status_code": 422},
            id="Invalid per_page above maximum boundary"),
    ])
    def test_get_bookmarks_list_incorrect_params(self, test_data):
        user = self.get_actor(test_data["user"])
        user.bookmarks_api.get_bookmarks(params=test_data["params"],
                                         expected_success=test_data["expected_success"],
                                         status_code=test_data["status_code"])

    @allure.suite("Bookmark post")
    @allure.story("User is able to bookmark existed post")
    @allure.description("Bookmark post")
    @pytest.mark.parametrize("create_remove_post_by_user, test_data", [
        pytest.param({"create_by": "admin"}, {"user": "admin"},
                     id="Bookmark post as admin"),
        pytest.param({"create_by": "user_eve"}, {"user": "user_eve"},
                     id="Bookmark post as user"),
        pytest.param({"create_by": "moderator"}, {"user": "moderator"},
                     id="Bookmark post as moderator"),
    ], indirect=["create_remove_post_by_user"])
    def test_bookmark_post(self, create_remove_post_by_user, test_data):
        user = self.get_actor(test_data["user"])
        prepared_post_id = create_remove_post_by_user
        user.bookmarks_api.bookmark_post(post_id=prepared_post_id)
        bookmarks = user.bookmarks_api.get_bookmarks(params={})
        assert any(prepared_post_id == bookmark.id and bookmark.is_bookmarked for bookmark in
                   bookmarks.items), "Bookmark list doesn't contain bookmark post"



    @allure.suite("Bookmark post")
    @allure.story("User is able to bookmark existed post")
    @allure.description("Bookmark post - incorrect post id")
    @pytest.mark.parametrize("get_incorrect_post, test_data", [
        pytest.param({"precondition_role": "user_eve", "post_case": "comment"},
                     {"user": "user_eve", "expected_success": False, "status_code": 404},
                     id="Comment instead of post"),
        pytest.param({"create_by": "user_eve", "post_case": "not_existed"},
                     {"user": "user_eve", "expected_success": False, "status_code": 404},
                     id="Post doesn't exist "),
        pytest.param({"create_by": "user_eve", "post_case": "removed"},
                     {"user": "user_eve", "expected_success": False, "status_code": 404},
                     id="Post is deleted"),
        pytest.param({"create_by": "user_eve", "post_case": "invalid_uuid"},
                     {"user": "user_eve", "expected_success": False, "status_code": 422},
                     id="Incorrect post id"),
        pytest.param({"precondition_role": "user_bob", "post_case": "bookmark"},
                     {"user": "user_bob", "expected_success": False, "status_code": 409},
                     id="Post is already in bookmarks"),
    ], indirect=["get_incorrect_post"])
    def test_bookmark_post_incorrect_post(self, get_incorrect_post, test_data):
        user = self.get_actor(test_data["user"])
        prepared_post_id = get_incorrect_post
        user.bookmarks_api.bookmark_post(post_id=prepared_post_id,
                                         expected_success=test_data["expected_success"],
                                         status_code=test_data["status_code"])





    @allure.suite("Unbookmark post")
    @allure.story("User is able to unbookmark post")
    @allure.description("Unbookmark post")
    @pytest.mark.parametrize("bookmark_post_only, test_data", [
        pytest.param({"create_by": "admin"}, {"user": "admin"},
                     id="Bookmark post as admin"),
        pytest.param({"create_by": "user_eve"}, {"user": "user_eve"},
                     id="Bookmark post as user"),
        pytest.param({"create_by": "moderator"}, {"user": "moderator"},
                     id="Bookmark post as moderator"),
    ], indirect=["bookmark_post_only"])
    def test_unbookmark_post(self, bookmark_post_only, test_data):
        user = self.get_actor(test_data["user"])
        prepared_post_id = bookmark_post_only
        user.bookmarks_api.remove_bookmark(post_id=prepared_post_id)
        bookmarks = user.bookmarks_api.get_bookmarks(params={})
        assert not any(prepared_post_id == bookmark.id for bookmark in bookmarks.items), "Post isn't removed from bookmark list"



    @allure.suite("Unbookmark post")
    @allure.story("User is able to unbookmark post")
    @allure.description("Unbookmark post - invalid post id")
    @pytest.mark.parametrize("get_incorrect_post, test_data", [
        pytest.param({"precondition_role": "user_eve", "post_case": "comment"},
                     {"user": "user_eve", "expected_success": False, "status_code": 404},
                     id="Comment instead of post"),
        pytest.param({"create_by": "user_eve", "post_case": "not_existed"},
                     {"user": "user_eve", "expected_success": False, "status_code": 404},
                     id="Post doesn't exist "),
        pytest.param({"create_by": "user_eve", "post_case": "removed"},
                     {"user": "user_eve", "expected_success": False, "status_code": 404},
                     id="Post is deleted"),
        pytest.param({"create_by": "user_eve", "post_case": "invalid_uuid"},
                     {"user": "user_eve", "expected_success": False, "status_code": 422},
                     id="Incorrect post id"),
        pytest.param({"precondition_role": "user_bob", "post_case": "not_bookmark"},
                     {"user": "user_bob", "expected_success": False, "status_code": 404},
                     id="Post is not in bookmarks"),
    ], indirect=["get_incorrect_post"])
    def test_unbookmark_post_incorrect_post(self, get_incorrect_post, test_data):
        user = self.get_actor(test_data["user"])
        prepared_post_id = get_incorrect_post
        user.bookmarks_api.remove_bookmark( post_id=prepared_post_id,
                                            expected_success=test_data["expected_success"],
                                            status_code=test_data["status_code"])
        