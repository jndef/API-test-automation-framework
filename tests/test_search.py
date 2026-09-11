import allure
import pytest

from config.base_test import BaseTest
from services.search.params import SearchUsersParamsByRoleTestCase, SearchUsersParams, SearchPostsParams, \
    SearchPostsParamsByRoleTestCase, SearchHashtagsParamsByRoleTestCase, SearchHashtagsParams, \
    SearchTrendingParamsByRoleTestCase, SearchTrendingParams


@allure.epic("Search Service")
@allure.parent_suite("Search service API")
@allure.title("Search service API")
@pytest.mark.search
class TestSearch(BaseTest):

    @allure.suite("Search")
    @allure.sub_suite("Search users")
    @allure.feature("Search users")
    @allure.story("User can search user")
    @allure.title("Search users with search_query, display name ({case.searched_user_alias})")
    @pytest.mark.smoke
    @pytest.mark.positive
    @pytest.mark.parametrize("case", [
        pytest.param(SearchUsersParamsByRoleTestCase(role="user_bob", searched_user_alias="user_eve",
                                                     params=SearchUsersParams(page=1, per_page=1)),
                     id="search user, full display name"),
    ])
    def test_search_users_by_display_name(self, case):
        search_service = self.get_actor(case.role).search_api
        user2_api = self.get_actor(case.searched_user_alias)
        user2_display_name = user2_api.auth_api.get_me().display_name.lower()
        response = search_service.search_users(params=case.params, search_query=user2_display_name)
        assert user2_display_name in response.items[
            0].display_name.lower(), f"ER:/AR: {user2_display_name} / {response.items[0].display_name}"

    @allure.suite("Search")
    @allure.sub_suite("Search users")
    @allure.feature("Search users")
    @allure.story("User can search user")
    @allure.title("Search users with search_query, username ({case.searched_user_alias})")
    @pytest.mark.regression
    @pytest.mark.positive
    @pytest.mark.parametrize("case", [
        pytest.param(SearchUsersParamsByRoleTestCase(role="user_bob", searched_user_alias="user_eve",
                                                     params=SearchUsersParams(page=1, per_page=1)),
                     id="search user, full user name"),
    ])
    def test_search_user_by_user_name(self, case):
        search_service = self.get_actor(case.role).search_api
        user2_api = self.get_actor(case.searched_user_alias)
        user2_username = user2_api.auth_api.get_me().username.lower()
        response = search_service.search_users(params=case.params, search_query=user2_username)
        assert user2_username in response.items[
            0].username.lower(), f"ER:/AR: {user2_username} / {response.items[0].username}"

    @allure.suite("Search")
    @allure.sub_suite("Search users")
    @allure.feature("Search users")
    @allure.story("User can search user")
    @allure.title("Search users with search_query, part display name ({case.searched_user_alias})")
    @pytest.mark.regression
    @pytest.mark.positive
    @pytest.mark.parametrize("case", [
        pytest.param(SearchUsersParamsByRoleTestCase(role="user_bob", searched_user_alias="user_eve",
                                                     params=SearchUsersParams(page=1, per_page=1)),
                     id="search user, part display name"),
    ])
    def test_search_user_part_display_name(self, case):
        search_service = self.get_actor(case.role).search_api
        user2_api = self.get_actor(case.searched_user_alias)
        user2_display_name: str = user2_api.auth_api.get_me().display_name.split(" ")[1].lower()
        response = search_service.search_users(params=case.params, search_query=user2_display_name)
        assert any(user2_display_name in user.display_name.lower() for user in
                   response.items), f"ER:/AR: {user2_display_name} / {response.items[0].display_name}"

    @allure.suite("Search")
    @allure.sub_suite("Search users")
    @allure.feature("Search users")
    @allure.story("User can search user")
    @allure.title("Search users with search_query - not existed")
    @pytest.mark.regression
    @pytest.mark.positive
    @pytest.mark.parametrize("case", [
        pytest.param(SearchUsersParamsByRoleTestCase(role="user_bob", searched_user_alias="test" * 3,
                                                     params=SearchUsersParams(page=1, per_page=1)),
                     id="search user, not existed"),
    ])
    def test_search_user_not_existed(self, case):
        search_service = self.get_actor(case.role).search_api
        search_response = search_service.search_users(params=case.params, search_query=case.searched_user_alias)
        assert search_response.total == 0 and len(search_response.items) == 0

    @allure.suite("Search")
    @allure.sub_suite("Search users")
    @allure.feature("Search users")
    @allure.story("User can search user")
    @allure.title("Search users with search_query - incorrect search query")
    @pytest.mark.regression
    @pytest.mark.negative
    @pytest.mark.parametrize("case", [
        pytest.param(SearchUsersParamsByRoleTestCase(role="user_bob", searched_user_alias="test" * 51,
                                                     params=SearchUsersParams(page=1, per_page=1)),
                     id="search user, too large query"),
        pytest.param(SearchUsersParamsByRoleTestCase(role="user_bob", searched_user_alias="",
                                                     params=SearchUsersParams(page=1, per_page=1)),
                     id="search user, empty query"),
    ])
    def test_search_user_not_allowed_query_length(self, case):
        search_service = self.get_actor(case.role).search_api
        search_service.search_users(params=case.params, search_query=case.searched_user_alias, expected_success=False,
                                    status_code=422)

    @allure.suite("Search")
    @allure.sub_suite("Search posts")
    @allure.feature("Search posts")
    @allure.story("User can search posts")
    @allure.title("Search posts with search_query - full post body, not long")
    @pytest.mark.smoke
    @pytest.mark.positive
    @pytest.mark.parametrize("case", [
        pytest.param(SearchPostsParamsByRoleTestCase(role="user_bob", searched_post_info="user_eve",
                                                     params=SearchPostsParams(page=1, per_page=10)),
                     id="search posts, full content"),
    ])
    def test_search_posts_full_content(self, case, build_post_remove):
        user_api = self.get_actor(case.role)
        post_id = build_post_remove(case.role)
        post_content: str = user_api.posts_api.get_post(post_id).content

        search_response = user_api.search_api.search_posts(params=case.params, search_query=post_content)
        assert post_content in search_response.items[
            0].content, f"ER:/AR: {search_response} / {search_response.items[0].content}"

    @allure.suite("Search")
    @allure.sub_suite("Search posts")
    @allure.feature("Search posts")
    @allure.story("User can search posts")
    @allure.title("Search posts with search_query - part post body")
    @pytest.mark.regression
    @pytest.mark.positive
    @pytest.mark.parametrize("case", [
        pytest.param(SearchPostsParamsByRoleTestCase(role="user_bob", searched_post_info="user_eve",
                                                     params=SearchPostsParams(page=1, per_page=10)),
                     id="search posts, part content"),
    ])
    def test_search_posts_part_content(self, case, build_post_remove):
        user_api = self.get_actor(case.role)
        post_id = build_post_remove(case.role)
        post_content_to_list: str = user_api.posts_api.get_post(post_id).content.split(" ")

        part_of_post_content_as_list = post_content_to_list[:2]
        part_of_post_content = " ".join(part_of_post_content_as_list)

        search_response = user_api.search_api.search_posts(params=case.params, search_query=part_of_post_content)
        assert part_of_post_content in search_response.items[
            0].content, f"ER:/AR: {search_response} / {search_response.items[0].content}"

    @allure.suite("Search")
    @allure.sub_suite("Search posts")
    @allure.feature("Search posts")
    @allure.story("User can search posts")
    @allure.title("Search posts with search_query - not existed post body")
    @pytest.mark.regression
    @pytest.mark.negative
    @pytest.mark.parametrize("case", [
        pytest.param(SearchPostsParamsByRoleTestCase(role="user_bob", searched_post_info="user_eve",
                                                     params=SearchPostsParams(page=1, per_page=10)),
                     id="search posts, not existed"),
    ])
    def test_search_posts_not_existed(self, case):
        user1_api = self.get_actor(case.role)
        post_content: str = self.data_helper.generate_text(50)

        search_response = user1_api.search_api.search_posts(params=case.params, search_query=post_content)
        assert search_response.total == 0 and len(search_response.items) == 0

    @allure.suite("Search")
    @allure.sub_suite("Search posts")
    @allure.feature("Search posts")
    @allure.story("User can search posts")
    @allure.title("Search posts - incorrect search query")
    @pytest.mark.regression
    @pytest.mark.negative
    @pytest.mark.parametrize("case", [
        pytest.param(SearchPostsParamsByRoleTestCase(role="user_bob", searched_post_info="test" * 51,
                                                     params=SearchPostsParams(page=1, per_page=1)),
                     id="search user, too large query"),
        pytest.param(SearchPostsParamsByRoleTestCase(role="user_bob", searched_post_info="",
                                                     params=SearchPostsParams(page=1, per_page=1)),
                     id="search posts, empty query"),
    ])
    def test_search_posts_not_allowed_query_length(self, case):
        search_service = self.get_actor(case.role).search_api
        search_service.search_posts(params=case.params, search_query=case.searched_post_info, expected_success=False,
                                    status_code=422)

    @allure.suite("Search")
    @allure.sub_suite("Search hashtags")
    @allure.feature("Search hashtags")
    @allure.story("User can search hashtags")
    @allure.title("Search hashtag")
    @pytest.mark.regression
    @pytest.mark.positive
    @pytest.mark.parametrize("case", [
        pytest.param(SearchHashtagsParamsByRoleTestCase(role="user_bob", searched_hashtag="dev",
                                                        params=SearchHashtagsParams(page=1, per_page=10)),
                     id="search hashtags, full text"),
        pytest.param(SearchHashtagsParamsByRoleTestCase(role="user_bob", searched_hashtag="cod",
                                                        params=SearchHashtagsParams(page=1, per_page=10)),
                     id="search hashtags, part text"),
    ])
    def test_search_hashtags(self, case):
        search_service = self.get_actor(case.role).search_api
        response = search_service.search_hashtags(search_query=case.searched_hashtag, params=case.params)
        assert case.searched_hashtag in response.items[
            0].name, f"ER:/AR: {case.searched_hashtag} / {response.items[0].name}"

    @allure.suite("Search")
    @allure.sub_suite("Search hashtags")
    @allure.feature("Search hashtags")
    @allure.story("User can search hashtags")
    @allure.title("Search hashtag - not existed")
    @pytest.mark.regression
    @pytest.mark.positive
    @pytest.mark.parametrize("case", [
        pytest.param(SearchHashtagsParamsByRoleTestCase(role="user_bob", searched_hashtag="est" * 5,
                                                        params=SearchHashtagsParams(page=1, per_page=10)),
                     id="search hashtags, not existed"),
    ])
    def test_search_hashtags(self, case):
        search_service = self.get_actor(case.role).search_api
        response = search_service.search_hashtags(search_query=case.searched_hashtag, params=case.params)
        assert len(response.items) == 0

    @allure.suite("Search")
    @allure.sub_suite("Search hashtags")
    @allure.feature("Search hashtags")
    @allure.story("User can search hashtags")
    @allure.title("Search hashtag - incorrect search query")
    @pytest.mark.regression
    @pytest.mark.negative
    @pytest.mark.parametrize("case", [
        pytest.param(SearchHashtagsParamsByRoleTestCase(role="user_bob", searched_hashtag="test" * 45,
                                                        params=SearchHashtagsParams(page=1, per_page=10)),
                     id="search hashtags, too long hashtag text"),
        pytest.param(SearchHashtagsParamsByRoleTestCase(role="user_bob", searched_hashtag="",
                                                        params=SearchHashtagsParams(page=1, per_page=10)),
                     id="search hashtags, empty string"),
    ])
    def test_search_hashtags_not_valid_search_query(self, case):
        search_service = self.get_actor(case.role).search_api
        search_service.search_hashtags(search_query=case.searched_hashtag, params=case.params, status_code=422,
                                       expected_success=False)

    @allure.suite("Search")
    @allure.sub_suite("Search hashtags trending")
    @allure.feature("Search hashtags trending")
    @allure.story("User can search hashtags trending")
    @allure.title("Search hashtags trending")
    @pytest.mark.regression
    @pytest.mark.positive
    @pytest.mark.parametrize("case", [
        pytest.param(SearchTrendingParamsByRoleTestCase(role="user_bob",
                                                        params=SearchTrendingParams(limit=1, period="week")),
                     id="min limit, week"),
        pytest.param(SearchTrendingParamsByRoleTestCase(role="user_bob",
                                                        params=SearchTrendingParams(limit=5, period="day")),
                     id="limit 5, day"),
        pytest.param(SearchTrendingParamsByRoleTestCase(role="user_bob",
                                                        params=SearchTrendingParams(limit=50)),
                     id="limit 50"),
        pytest.param(SearchTrendingParamsByRoleTestCase(role="user_bob",
                                                        params=SearchTrendingParams(period="week")),
                     id="week"),
        pytest.param(SearchTrendingParamsByRoleTestCase(role="user_bob",
                                                        params=SearchTrendingParams()),
                     id="no query params"),
    ])
    def test_search_trending(self, case):
        search_service = self.get_actor(case.role).search_api
        response = search_service.search_trending(params=case.params)
        if case.params.limit:
            assert len(response) <= case.params.limit, f"ER:/AR: {case.params.limit}/{len(response)}"

    @allure.suite("Search")
    @allure.sub_suite("Search hashtags trending")
    @allure.feature("Search hashtags trending")
    @allure.story("User can search hashtags trending")
    @allure.title("Search hashtags trending - incorrect query params")
    @pytest.mark.regression
    @pytest.mark.negative
    @pytest.mark.parametrize("case", [
        pytest.param(SearchTrendingParamsByRoleTestCase(role="user_bob",
                                                        params=SearchTrendingParams(limit=0)),
                     id="below min limit"),
        pytest.param(SearchTrendingParamsByRoleTestCase(role="user_bob",
                                                        params=SearchTrendingParams(period="month")),
                     id="not expected period"),
        pytest.param(SearchTrendingParamsByRoleTestCase(role="user_bob",
                                                        params=SearchTrendingParams(limit=-1)),
                     id="limit -1"),
        pytest.param(SearchTrendingParamsByRoleTestCase(role="user_bob",
                                                        params=SearchTrendingParams(limit=51)),
                     id="above max limit"),
        pytest.param(SearchTrendingParamsByRoleTestCase(role="user_bob",
                                                        params=SearchTrendingParams(limit=50 ** 9)),
                     id="large limit"),
    ])
    def test_search_trending_incorrect_query_params(self, case):
        search_service = self.get_actor(case.role).search_api
        search_service.search_trending(params=case.params, expected_success=False, status_code=422)
