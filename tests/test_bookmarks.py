import allure
import pytest

from config.base_test import BaseTest
from services.bookmarks.params import GetBookmarksQueryParamsTestCaseByRole, GetBookmarksQueryParams


@allure.epic("Bookmarks Service")
@allure.feature("Bookmarks")
@allure.parent_suite("Tests Bookmarks service API")
@allure.title("Tests Bookmarks service API")
@pytest.mark.bookmarks
class TestBookmarks(BaseTest):

    @allure.suite("Get user's bookmarks list")
    @allure.story("User can read added bookmarks")
    @allure.description("Get bookmarks list")
    @pytest.mark.parametrize("case", [
        pytest.param(
            GetBookmarksQueryParamsTestCaseByRole(role="user_eve", params=GetBookmarksQueryParams(page=1, per_page=1)),
            id="valid minimum boundaries"),
        pytest.param(GetBookmarksQueryParamsTestCaseByRole(role="moderator",
                                                           params=GetBookmarksQueryParams(page=1, per_page=100)),
                     id="valid maximum boundary"),
        pytest.param(GetBookmarksQueryParamsTestCaseByRole(role="admin", params=GetBookmarksQueryParams()),
                     id="empty query param"),
    ])
    def test_get_bookmarks_list(self, case):
        user = self.get_actor(case.role)
        user.bookmarks_api.get_bookmarks(params=case.params)

    @allure.suite("Get user's bookmarks list")
    @allure.story("User can read added bookmarks")
    @allure.description("Get bookmarks list - incorrect query params")
    @pytest.mark.parametrize("case", [
        pytest.param(
            GetBookmarksQueryParamsTestCaseByRole(role="user_eve", params=GetBookmarksQueryParams(page=0, per_page=10)),
            id="Invalid page below minimum boundary"),
        pytest.param(
            GetBookmarksQueryParamsTestCaseByRole(role="user_eve", params=GetBookmarksQueryParams(page=1, per_page=0)),
            id="Invalid per_page below minimum boundary"),
        pytest.param(
            GetBookmarksQueryParamsTestCaseByRole(role="user_eve",
                                                  params=GetBookmarksQueryParams(page=1, per_page=101)),
            id="Invalid per_page above maximum boundary"),
    ])
    def test_get_bookmarks_list_incorrect_params(self, case):
        user = self.get_actor(case.role)
        user.bookmarks_api.get_bookmarks(params=case.params,
                                         expected_success=False,
                                         status_code=422)

    @allure.suite("Bookmark post")
    @allure.story("User is able to bookmark existed post")
    @allure.description("Bookmark post")
    @pytest.mark.parametrize("case_role", [
        pytest.param("admin", id="Bookmark post as admin"),
        pytest.param("user_eve", id="Bookmark post as user"),
        pytest.param("moderator", id="Bookmark post as moderator"),
    ])
    def test_bookmark_post(self, build_post_remove, case_role):
        bookmark_service = self.get_actor(case_role).bookmarks_api
        prepared_post_id = build_post_remove(case_role)

        bookmark_service.bookmark_post(post_id=prepared_post_id)

        bookmarks = bookmark_service.get_bookmarks(params=GetBookmarksQueryParams())
        assert any(prepared_post_id == bookmark.id and bookmark.is_bookmarked for bookmark in
                   bookmarks.items), "Bookmark list doesn't contain bookmark post"

    @allure.suite("Bookmark post")
    @allure.story("User is able to bookmark existed post")
    @allure.description("Bookmark post - Comment instead of post")
    @pytest.mark.parametrize("case_role", [
        pytest.param("user_eve", id="Comment instead of post"),
    ])
    def test_bookmark_post_comment_in_use(self, build_comment_remove, case_role):
        user = self.get_actor(case_role)
        prepared_post_id = build_comment_remove(case_role)
        user.bookmarks_api.bookmark_post(post_id=prepared_post_id,
                                         expected_success=False,
                                         status_code=404)

    @allure.suite("Bookmark post")
    @allure.story("User is able to bookmark existed post")
    @allure.description("Bookmark post - Post doesn't exist")
    @pytest.mark.parametrize("case_role", [
        pytest.param("user_eve", id="Post doesn't exist"),
    ])
    def test_bookmark_post_not_existed(self, case_role):
        bookmark_service = self.get_actor(case_role).bookmarks_api
        prepared_post_id = self.data_helper.get_not_existed_uuid()
        bookmark_service.bookmark_post(post_id=prepared_post_id,
                                       expected_success=False,
                                       status_code=404)

    @allure.suite("Bookmark post")
    @allure.story("User is able to bookmark existed post")
    @allure.description("Bookmark post - Post is deleted")
    @pytest.mark.parametrize("case_role", [
        pytest.param("user_bob", id="Post is deleted"),
    ])
    def test_bookmark_post_removed(self, get_removed_post, case_role):
        prepared_post_id = get_removed_post(case_role)
        bookmark_service = self.get_actor(case_role).bookmarks_api
        bookmark_service.bookmark_post(post_id=prepared_post_id,
                                       expected_success=False,
                                       status_code=404)

    @allure.suite("Bookmark post")
    @allure.story("User is able to bookmark existed post")
    @allure.description("Bookmark post - invalid post id")
    @pytest.mark.parametrize("case_role", [
        pytest.param("user_eve", id="Invalid post id"),
    ])
    def test_bookmark_post_invalid_uuid(self, case_role):
        bookmark_service = self.get_actor(case_role).bookmarks_api
        prepared_post_id = self.data_helper.get_invalid_uuid()
        bookmark_service.bookmark_post(post_id=prepared_post_id,
                                       expected_success=False,
                                       status_code=422)

    @allure.suite("Bookmark post")
    @allure.story("User is able to bookmark existed post")
    @allure.description("Bookmark post - Post is already in bookmarks")
    @pytest.mark.parametrize("case_role", [
        pytest.param("user_eve", id="Post is already in bookmarks"),
    ])
    def test_bookmark_post_already_bookmarked(self, build_post_bookmark_remove, case_role):
        prepared_post_id = build_post_bookmark_remove(case_role)
        bookmark_service = self.get_actor(case_role).bookmarks_api
        bookmark_service.bookmark_post(post_id=prepared_post_id,
                                       expected_success=False,
                                       status_code=409)

    @allure.suite("Unbookmark post")
    @allure.story("User is able to unbookmark post")
    @allure.description("Unbookmark post")
    @pytest.mark.parametrize("case_role", [
        pytest.param("admin", id="Bookmark post as admin"),
        pytest.param("user_bob", id="Bookmark post as user"),
        pytest.param("moderator", id="Bookmark post as moderator"),
    ])
    def test_unbookmark_post(self, build_post_bookmark_remove, case_role):
        prepared_post_id = build_post_bookmark_remove(case_role)
        bookmark_service = self.get_actor(case_role).bookmarks_api
        bookmark_service.remove_bookmark(post_id=prepared_post_id)
        bookmarks = bookmark_service.get_bookmarks(params=GetBookmarksQueryParams())
        assert not any(
            prepared_post_id == bookmark.id for bookmark in bookmarks.items), "Post isn't removed from bookmark list"

    @allure.suite("Unbookmark post")
    @allure.story("User is able to unbookmark post")
    @allure.description("Unbookmark post - Comment instead of post")
    @pytest.mark.parametrize("case_role", [
        pytest.param("user_eve", id="Comment instead of post"),
    ])
    def test_unbookmark_post_comment_instead(self, build_comment_remove, case_role):
        prepared_post_id = build_comment_remove(case_role)
        bookmark_service = self.get_actor(case_role).bookmarks_api
        bookmark_service.remove_bookmark(post_id=prepared_post_id,
                                         expected_success=False,
                                         status_code=404)

    @allure.suite("Unbookmark post")
    @allure.story("User is able to unbookmark post")
    @allure.description("Unbookmark post - Post doesn't exist")
    @pytest.mark.parametrize("case_role", [
        pytest.param("user_eve", id="Post doesn't exist"),
    ])
    def test_unbookmark_post_not_existed(self, case_role):
        bookmark_service = self.get_actor(case_role).bookmarks_api
        prepared_post_id = self.data_helper.get_not_existed_uuid()
        bookmark_service.remove_bookmark(post_id=prepared_post_id,
                                         expected_success=False,
                                         status_code=404)

    @allure.suite("Unbookmark post")
    @allure.story("User is able to unbookmark post")
    @allure.description("Unbookmark post - bookmarked post is deleted")
    @pytest.mark.parametrize("case_role", [
        pytest.param("user_bob", id="Post is deleted"),
    ])
    def test_unbookmark_post_removed(self, case_role, get_removed_bookmarked_post):
        prepared_post_id = get_removed_bookmarked_post(case_role)
        bookmark_service = self.get_actor(case_role).bookmarks_api
        bookmark_service.remove_bookmark(post_id=prepared_post_id,
                                         expected_success=False,
                                         status_code=404)

    @allure.suite("Unbookmark post")
    @allure.story("User is able to unbookmark post")
    @allure.description("Unbookmark post - invalid post id")
    @pytest.mark.parametrize("case_role", [
        pytest.param("user_eve", id="Invalid post id"),
    ])
    def test_unbookmark_post_incorrect_uuid(self, case_role):
        bookmark_service = self.get_actor(case_role).bookmarks_api
        prepared_post_id = self.data_helper.get_invalid_uuid()
        bookmark_service.remove_bookmark(post_id=prepared_post_id,
                                         expected_success=False,
                                         status_code=422)

    @allure.suite("Unbookmark post")
    @allure.story("User is able to unbookmark post")
    @allure.description("Unbookmark post - invalid post id")
    @pytest.mark.parametrize("case_role", [
        pytest.param("user_eve", id="Post is already in bookmarks"),
    ])
    def test_unbookmark_post_not_bookmarked(self, build_post_remove, case_role):
        prepared_post_id = build_post_remove(case_role)
        bookmark_service = self.get_actor(case_role).bookmarks_api
        bookmark_service.remove_bookmark(post_id=prepared_post_id,
                                         expected_success=False,
                                         status_code=404)
