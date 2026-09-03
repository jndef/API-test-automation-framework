import allure
import pytest

from config.base_test import BaseTest
from services.follows.params import GetFollowRequestsParamsByRoleTestCase, GetFollowRequestsParams
from services.users.params import GetFollowersParams


@allure.epic("Follows")
@allure.feature("Follows")
@allure.parent_suite("Follows")
@pytest.mark.follows
class TestFollows(BaseTest):

    @allure.feature("Follow requests")
    @allure.suite("Follow requests")
    @allure.sub_suite("Get Follow requests")
    @allure.title("Get Follow requests with params ({case.params})")
    @pytest.mark.parametrize("case_user", [
        pytest.param(GetFollowRequestsParamsByRoleTestCase(role="user_private", params=GetFollowRequestsParams(page=1, per_page=1)),
            id="valid minimum boundaries"),
        pytest.param(GetFollowRequestsParamsByRoleTestCase(role="user_private",params=GetFollowRequestsParams(page=1, per_page=100)),
                     id="valid maximum boundary"),
        pytest.param(GetFollowRequestsParamsByRoleTestCase(role="user_private", params=GetFollowRequestsParams()),
                     id="empty query param"),
    ])
    def test_get_follow_requests(self, case_user):
        follow_service = self.get_actor(case_user.role).follows_api
        follow_service.get_follow_requests(params=case_user.params)

    @allure.feature("Follow requests")
    @allure.suite("Follow requests")
    @allure.sub_suite("Get Follow requests")

    @allure.title("Get Follow requests with  invalid params ({case.params})")
    @pytest.mark.parametrize("case_user", [
    pytest.param(GetFollowRequestsParamsByRoleTestCase(role="user_private", params=GetFollowRequestsParams(page=0)),
                 id="page, below min allowed value"),
    pytest.param(GetFollowRequestsParamsByRoleTestCase(role="user_private", params=GetFollowRequestsParams(per_page=0)),
                 id="per_page, below min allowed value"),
    pytest.param(GetFollowRequestsParamsByRoleTestCase(role="user_private", params=GetFollowRequestsParams(per_page=101)),
                 id="per_page, above max allowed value"),
    pytest.param(GetFollowRequestsParamsByRoleTestCase(role="user_private", params=GetFollowRequestsParams(page=1 * 10 ** 100)),
                 id="page, too large value"),
    pytest.param(GetFollowRequestsParamsByRoleTestCase(role="user_private", params=GetFollowRequestsParams(per_page=1 * 10 ** 100)),
                 id="per_page, too large value"),
    ])
    def test_get_follow_requests_invalid_params(self, case_user):
        follow_service = self.get_actor(case_user.role).follows_api
        follow_service.get_follow_requests(params=case_user.params, status_code=422, expected_success=False)


    @allure.feature("Follow requests")
    @allure.suite("Follow requests")
    @allure.sub_suite("Create Follow requests")
    @allure.title("Create follow request to user ({private_user}) by {case_user}")

    @pytest.mark.parametrize("case_user, private_user", [
        pytest.param("user_eve", "user_private",id="create follow request by user"),
        pytest.param("admin", "user_private",id="create follow request by admin"),
        pytest.param("moderator", "user_private",id="create follow request by moderator"),
    ])
    def test_create_follow_request(self, case_user, private_user, follow_request_cleaner):
        api_client_private_user = self.get_actor(private_user)
        auth_service_private_user = api_client_private_user.auth_api
        follow_service_private_user = api_client_private_user.follows_api

        api_client = self.get_actor(case_user)
        auth_service = api_client.auth_api
        follow_service = api_client.follows_api

        with allure.step("Get username of user performed follow request for validation"):
            case_user_username = auth_service.get_me().username

        with allure.step("Get username of user for create follow request"):
            private_user_username = auth_service_private_user.get_me().username
        # register unfollowing after test
        follow_request_cleaner(role=case_user, user_name=private_user_username)

        follow_request = follow_service.follow_user(private_user_username)

        with allure.step("Check response data of the follow request"):
            assert follow_request.follower.username == case_user_username, f"Validation error. Response of follow request has unexpected follower info. AR: {follow_request.follower}"
            assert follow_request.following.username == private_user_username, f"Validation error. Response of follow request has unexpected following info. AR: {follow_request.following}"
            assert follow_request.status == 'pending', f"Validation error. Follow request status should be pending. AR: {follow_request.status}"


        with allure.step('Check user at follower request list'):
            followers_requests_list = follow_service_private_user.get_follow_requests(params=GetFollowRequestsParams()).items
            assert any([case_user_username == follower_request.follower.username for follower_request in followers_requests_list])



    @allure.feature("Follow requests")
    @allure.suite("Follow requests")
    @allure.sub_suite("Create Follow requests")

    @allure.title("Create follow request to user - not valid username")
    @pytest.mark.parametrize("case_user, private_user", [
        pytest.param("user_eve", "testtesttest",id="create follow request to user with not existed username"),
        pytest.param("user_private", "user_private", id="create follow request to himself"),
    ])
    def test_create_follow_request_not_existed_name(self, case_user, private_user):
        follow_service = self.get_actor(case_user).follows_api
        follow_service.follow_user(private_user, expected_success=False, status_code=404)

    @allure.feature("Follow requests")
    @allure.suite("Follow requests")
    @allure.sub_suite("Create Follow requests")

    @allure.title("Create follow request to user - already followed")
    @pytest.mark.parametrize("case_user, private_user", [
        pytest.param("user_eve", "user_private", id="attempt to repeat follow request"),
    ])
    def test_create_follow_request_repeat_request(self, case_user, private_user, db_get_username, follow_request_cleaner):
        private_user_name = db_get_username(private_user)
        follow_request_cleaner(role=case_user, user_name=private_user_name)
        follow_service = self.get_actor(case_user).follows_api
        follow_service.follow_user(private_user_name)
        follow_service.follow_user(private_user_name, expected_success=False, status_code=409)

    @allure.feature("Follow requests")
    @allure.suite("Follow requests")
    @allure.sub_suite("Remove Follow requests")

    @allure.title("Remove follow request to user")
    @pytest.mark.parametrize("case_user, private_user", [
        pytest.param("user_eve", "user_private", id="unfollow existed follow request"),
    ])
    def test_remove_follow_request(self, case_user, private_user, get_follow_request, db_get_username):
        api_client_private_user = self.get_actor(private_user)
        follow_service_private_user = api_client_private_user.follows_api
        auth_service_private_user = api_client_private_user.auth_api

        api_client = self.get_actor(case_user)
        auth_service = api_client.auth_api
        follow_service = api_client.follows_api

        with allure.step("Get username of user for create follow request"):
            private_user_name = auth_service_private_user.get_me().username
        with allure.step("Get username of user performed follow request for validation"):
            case_user_username = auth_service.get_me().username

        get_follow_request(case_user, private_user_name)


        follow_service.unfollow_user(private_user_name)

        with allure.step('Check user at follower request list'):
            followers_requests_list = follow_service_private_user.get_follow_requests(params=GetFollowRequestsParams()).items
            assert all([case_user_username != follower_request.follower.username for follower_request in followers_requests_list])


    @allure.feature("Follow requests")
    @allure.suite("Follow requests")
    @allure.sub_suite("Remove Follow requests")

    @allure.title("Remove follow request to user with not existed username")
    @pytest.mark.parametrize("case_user, private_user", [
        pytest.param("user_eve", "testtesttest", id="unfollow using not existed username"),
    ])
    def test_remove_follow_request_not_existed(self, case_user, private_user):
        follow_service = self.get_actor(case_user).follows_api
        follow_service.unfollow_user(private_user, status_code=404, expected_success=False)


    @allure.feature("Follow requests")
    @allure.suite("Follow requests")
    @allure.sub_suite("Remove Follow requests - no follow request before ")

    @allure.title("Remove follow request to user with not existed username")
    @pytest.mark.parametrize("case_user, private_user", [
        pytest.param("user_eve", "admin", id="remove follow request, no request before"),
    ])
    def test_remove_follow_request_no_request_before(self, case_user, private_user):
        follow_service = self.get_actor(case_user).follows_api
        follow_service.unfollow_user(private_user, status_code=404, expected_success=False)

    @allure.feature("Follow requests")
    @allure.suite("Follow requests")
    @allure.sub_suite("Accept Follow requests")
    @allure.title("Accept follow request of the user ({case})")

    @pytest.mark.parametrize("case_user, private_user", [
        pytest.param("user_eve", "user_private",id="accept follow request by user"),
    ])
    def test_accept_follow_request(self, case_user, private_user, follow_request_cleaner):
        # case user services
        api_client = self.get_actor(case_user)
        auth_service = api_client.auth_api
        follow_service = api_client.follows_api

        #private user services
        api_client_private_user = self.get_actor(private_user)
        auth_service_private_user = api_client_private_user.auth_api
        follow_service_private_user = api_client_private_user.follows_api
        users_service_private_user = api_client_private_user.users_api
        with allure.step("Get username of user performed follow request for validation"):
            case_user_username = auth_service.get_me().username

        with allure.step("Get username of user for create follow request"):
            private_user_username = auth_service_private_user.get_me().username

        # register unfollowing after test
        follow_request_cleaner(role=case_user, user_name=private_user_username)

        follow_request = follow_service.follow_user(private_user_username)

        accepted_request = follow_service_private_user.accept_follow_request(follow_request.id)

        with allure.step("Check response data of the follow request"):
            assert accepted_request.follower.username == case_user_username, f"Validation error. Response of follow request has unexpected follower info. AR: {follow_request.follower}"
            assert accepted_request.following.username == private_user_username, f"Validation error. Response of follow request has unexpected following info. AR: {follow_request.following}"
            assert accepted_request.status == 'accepted', f"Validation error. Follow request status should be pending. AR: {follow_request.status}"


        with allure.step('Check user at followers list'):
            followers_list = users_service_private_user.get_user_followers(user_name=private_user_username, params=GetFollowersParams()).items
            assert any([case_user_username == follower.username for follower in followers_list])

    @allure.feature("Follow requests")
    @allure.suite("Follow requests")
    @allure.sub_suite("Accept Follow requests")
    @allure.title("Accept follow request - not existed request")
    @pytest.mark.parametrize("private_user", [
        pytest.param("user_private",id="attempt to accept not existed request"),
    ])
    def test_accept_follow_request_not_existed(self, private_user):
        #private user services
        api_client_private_user = self.get_actor(private_user)
        follow_service_private_user = api_client_private_user.follows_api

        follow_request = self.data_helper.get_not_existed_uuid()
        follow_service_private_user.accept_follow_request(follow_request, expected_success=False, status_code=404)

    @allure.feature("Follow requests")
    @allure.suite("Follow requests")
    @allure.sub_suite("Accept Follow requests")
    @allure.title("Accept follow request - not valid request id")
    @pytest.mark.parametrize("private_user", [
        pytest.param( "user_private",id="attempt to accept not existed request"),
    ])
    def test_accept_follow_request_invalid_id(self, private_user):
        #private user services
        api_client_private_user = self.get_actor(private_user)
        follow_service_private_user = api_client_private_user.follows_api

        follow_request = self.data_helper.get_invalid_uuid()
        follow_service_private_user.accept_follow_request(follow_request, expected_success=False, status_code=422)

    @allure.feature("Follow requests")
    @allure.suite("Follow requests")
    @allure.sub_suite("Accept Follow requests")
    @allure.title("Accept follow request - attempt accept own request to private user")
    @pytest.mark.parametrize("case_user, private_user", [
        pytest.param( "user_bob", "user_private",id="attempt accept own request to private user"),
    ])
    def test_accept_follow_request_accept_own(self, case_user, private_user, follow_request_cleaner):
        # case user services
        api_client = self.get_actor(case_user)
        follow_service = api_client.follows_api

        #private user services
        api_client_private_user = self.get_actor(private_user)
        auth_service_private_user = api_client_private_user.auth_api


        with allure.step("Get username of user for create follow request"):
            private_user_username = auth_service_private_user.get_me().username

        # register unfollowing after test
        follow_request_cleaner(role=case_user, user_name=private_user_username)

        follow_request = follow_service.follow_user(private_user_username)

        follow_service.accept_follow_request(follow_request.id, expected_success=False, status_code=403)




    @allure.feature("Follow requests")
    @allure.suite("Follow requests")
    @allure.sub_suite("Accept Follow requests")
    @allure.title("Accept follow request - attempt to accept request twice")
    @pytest.mark.parametrize("case_user, private_user", [
        pytest.param( "user_bob", "user_private",id="attempt to accept request twice"),
    ])
    def test_accept_follow_request_accept_twice(self, case_user, private_user, follow_request_cleaner):
        # case user services
        api_client = self.get_actor(case_user)
        follow_service = api_client.follows_api

        #private user services
        api_client_private_user = self.get_actor(private_user)
        auth_service_private_user = api_client_private_user.auth_api
        follow_service_private_user = api_client_private_user.follows_api


        with allure.step("Get username of user for create follow request"):
            private_user_username = auth_service_private_user.get_me().username

        # register unfollowing after test
        follow_request_cleaner(role=case_user, user_name=private_user_username)

        follow_request = follow_service.follow_user(private_user_username)

        follow_service_private_user.accept_follow_request(follow_request.id)
        follow_service_private_user.accept_follow_request(follow_request.id, expected_success=False, status_code=400)


    @allure.feature("Follow requests")
    @allure.suite("Follow requests")
    @allure.sub_suite("Reject follow requests")
    @allure.title("Reject follow request of the user ({case})")
    @pytest.mark.parametrize("case_user, private_user", [
        pytest.param("user_eve", "user_private", id="reject follow request by user"),
    ])
    def test_reject_follow_request(self, case_user, private_user, follow_request_cleaner):
        # case user services
        api_client = self.get_actor(case_user)
        auth_service = api_client.auth_api
        follow_service = api_client.follows_api

        # private user services
        api_client_private_user = self.get_actor(private_user)
        auth_service_private_user = api_client_private_user.auth_api
        follow_service_private_user = api_client_private_user.follows_api
        users_service_private_user = api_client_private_user.users_api

        with allure.step("Get username of user performed follow request for validation"):
            case_user_username = auth_service.get_me().username

        with allure.step("Get username of user for create follow request"):
            private_user_username = auth_service_private_user.get_me().username

        # register unfollowing after test
        follow_request_cleaner(role=case_user, user_name=private_user_username)

        follow_request = follow_service.follow_user(private_user_username)

        follow_service_private_user.reject_follow_request(follow_request.id)

        with allure.step('Check user is not at followers list'):
            followers_list = users_service_private_user.get_user_followers(user_name=private_user_username,
                                                                           params=GetFollowersParams()).items
            assert all([case_user_username != follower.username for follower in followers_list])

        with allure.step('Check user is not at follower requests list'):
            followers_requests_list = follow_service_private_user.get_follow_requests(params=GetFollowersParams()).items
            assert all([case_user_username != follower_request.follower.username for follower_request in followers_requests_list])

    @allure.feature("Follow requests")
    @allure.suite("Follow requests")
    @allure.sub_suite("Reject follow requests")
    @allure.title("Reject follow request - not existed request")
    @pytest.mark.parametrize("private_user", [
        pytest.param("user_private", id="attempt to reject not existed request"),
    ])
    def test_reject_follow_request_not_existed(self, private_user):
        # private user services
        api_client_private_user = self.get_actor(private_user)
        follow_service_private_user = api_client_private_user.follows_api

        follow_request = self.data_helper.get_not_existed_uuid()
        follow_service_private_user.reject_follow_request(follow_request, expected_success=False, status_code=404)

    @allure.feature("Follow requests")
    @allure.suite("Follow requests")
    @allure.sub_suite("Reject follow requests")

    @allure.title("Reject follow request - not valid request id")
    @pytest.mark.parametrize("private_user", [
        pytest.param("user_private", id="attempt to reject not existed request"),
    ])
    def test_reject_follow_request_invalid_id(self, private_user):
        # private user services
        api_client_private_user = self.get_actor(private_user)
        follow_service_private_user = api_client_private_user.follows_api

        follow_request = self.data_helper.get_invalid_uuid()
        follow_service_private_user.reject_follow_request(follow_request, expected_success=False, status_code=422)

    @allure.feature("Follow requests")
    @allure.suite("Follow requests")
    @allure.sub_suite("Reject follow requests")
    @allure.title("Reject follow request - attempt to reject own request to private user")
    @pytest.mark.parametrize("case_user, private_user", [
        pytest.param("user_bob", "user_private", id="attempt reject own request to private user"),
    ])
    def test_reject_follow_request_reject_own(self, case_user, private_user, follow_request_cleaner):
        # case user services
        api_client = self.get_actor(case_user)
        follow_service = api_client.follows_api

        # private user services
        api_client_private_user = self.get_actor(private_user)
        auth_service_private_user = api_client_private_user.auth_api

        with allure.step("Get username of user for create follow request"):
            private_user_username = auth_service_private_user.get_me().username

        # register unfollowing after test
        follow_request_cleaner(role=case_user, user_name=private_user_username)

        follow_request = follow_service.follow_user(private_user_username)

        follow_service.reject_follow_request(follow_request.id, expected_success=False, status_code=403)

    @allure.feature("Follow requests")
    @allure.suite("Follow requests")
    @allure.sub_suite("Reject follow requests")
    @pytest.mark.testing
    @allure.title("Reject follow request - attempt to reject twice request")
    @pytest.mark.parametrize("case_user, private_user", [
        pytest.param("user_bob", "user_private", id="Attempt to reject twice request"),
    ])
    def test_reject_follow_request_reject_twice(self, case_user, private_user, follow_request_cleaner):
        # case user services
        api_client = self.get_actor(case_user)
        follow_service = api_client.follows_api

        # private user services
        api_client_private_user = self.get_actor(private_user)
        auth_service_private_user = api_client_private_user.auth_api
        follow_service_private_user = api_client_private_user.follows_api

        with allure.step("Get username of user for create follow request"):
            private_user_username = auth_service_private_user.get_me().username

        # register unfollowing after test
        follow_request_cleaner(role=case_user, user_name=private_user_username)

        follow_request = follow_service.follow_user(private_user_username)

        follow_service_private_user.reject_follow_request(follow_request.id)
        follow_service_private_user.reject_follow_request(follow_request.id, expected_success=False,
                                                          status_code=400)