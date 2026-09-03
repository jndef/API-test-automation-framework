import allure
import pytest

from config.base_test import BaseTest
from services.users.params import GetUsersParamsByRoleTestCase, GetUsersParams, GetUserPostsParamsByRoleTestCase, \
    GetUserPostsParams, GetFollowersParamsByRoleTestCase, GetFollowersParams, GetFollowingParamsByRoleTestCase, \
    GetFollowingParams
from services.users.payloads import UpdateMePayloadByRoleTestCase, UpdateMePayload, UpdateAvatarByRoleTestCase, \
    UpdateAvatarFilePayload


@allure.epic("Users")
@allure.parent_suite("Users")
class TestUsers(BaseTest):

    @allure.feature("List Users")
    @allure.suite("List Users")
    @allure.sub_suite("Get List Users")

    @allure.story("User can see existed users")
    @allure.title("Get List Users - with params ({case.params})")
    @pytest.mark.parametrize("case ", [
        pytest.param(GetUsersParamsByRoleTestCase(role="user_bob",
                                            params=GetUsersParams(page=1, per_page=1, search="eve", sort_by="username", sort_order="desc")), id="123"),
        pytest.param(GetUsersParamsByRoleTestCase(role="user_bob",
                                            params=GetUsersParams(page=1, per_page=100, sort_by="created_at", sort_order="asc"))),
        pytest.param(GetUsersParamsByRoleTestCase(role="user_bob",
                                            params=GetUsersParams(page=1, per_page=1, sort_by="display_name", sort_order="desc"))),
        pytest.param(GetUsersParamsByRoleTestCase(role="user_bob",
                                            params=GetUsersParams(page=1, search="eve", per_page=100, sort_by="created_at", sort_order="desc"))),
        pytest.param(GetUsersParamsByRoleTestCase(role="user_bob",
                                            params=GetUsersParams(page=1,  per_page=100, sort_by="username", sort_order="asc"))),
        pytest.param(GetUsersParamsByRoleTestCase(role="user_bob",
                                            params=GetUsersParams(page=1, search="eve",  per_page=100, sort_by="display_name", sort_order="asc"))),
        pytest.param(GetUsersParamsByRoleTestCase(role="user_bob",
                                            params=GetUsersParams(page=1, search="eve",  per_page=1, sort_by="display_name", sort_order="asc")))
    ])
    @pytest.mark.smoke
    def test_get_users(self, case):
        user_service = self.get_actor(case.role).users_api
        user_service.get_list_users(params=case.params)


    @allure.feature("List Users")
    @allure.suite("List Users")
    @allure.sub_suite("Get List Users")

    @allure.story("User can see existed users")
    @allure.title("Get List Users - with invalid params ({case.params})")
    @pytest.mark.parametrize("case", [
        pytest.param(GetUsersParamsByRoleTestCase(role="user_bob",
                                            params=GetUsersParams(page=0)), id="Page, below allowed minimum"),
        pytest.param(GetUsersParamsByRoleTestCase(role="user_bob",
                                            params=GetUsersParams(per_page=0)), id="Per page, below allowed minimum"),
        pytest.param(GetUsersParamsByRoleTestCase(role="user_bob",
                                            params=GetUsersParams(per_page=101)), id="Per page, above allowed maximum"),
        pytest.param(GetUsersParamsByRoleTestCase(role="user_bob",
                                            params=GetUsersParams(sort_by="test")), id="Sort by, unexpected value"),
        pytest.param(GetUsersParamsByRoleTestCase(role="user_bob",
                                            params=GetUsersParams(sort_order="test")), id="Sort order, unexpected value"),
        pytest.param(GetUsersParamsByRoleTestCase(role="user_bob",
                                            params=GetUsersParams(search="")), id="Search, empty string"),
        pytest.param(GetUsersParamsByRoleTestCase(role="user_bob",
                                            params=GetUsersParams(search="A"*200)), id="Search, too long search criteria")
    ])
    def test_get_users_invalid_params(self, case):
        user_service = self.get_actor(case.role).users_api
        user_service.get_list_users(params=case.params, expected_success=False, status_code=422)


    @allure.feature("Get user suggestions")
    @allure.suite("Get user suggestions")
    @allure.sub_suite("Get user suggestions")

    @allure.story("User can read user suggestions")
    @allure.title("Get user suggestions as - {case}")

    @allure.description("Return up to 5 active users that the current user does not follow yet.")
    @pytest.mark.parametrize("case", [
        pytest.param("admin", id="get suggestions as admin"),
        pytest.param("user_bob", id="get suggestions as user"),
        pytest.param("moderator", id="get suggestions as moderator"),
                             ])
    def test_get_user_suggestions(self, case):
        user_service = self.get_actor(case).users_api
        suggestions = user_service.get_user_suggestions()
        assert len(suggestions) <= 5, "Too many provided suggestions"


    @allure.feature("Get user profile")
    @allure.suite("Get user profile")
    @allure.sub_suite("Get user profile")

    @allure.title("Get user profile with provided username: {username}")
    @pytest.mark.parametrize("username", ["admin", "dave_quiet", "bob_photo"])
    def test_get_user_profile(self, username):
        user_service = self.get_actor("user_eve").users_api
        user_profile_info = user_service.get_user_profile(username=username)
        assert user_profile_info.username == username, f"AR: {user_profile_info.username} != {username}"

    @allure.feature("Get user profile")
    @allure.suite("Get user profile")
    @allure.sub_suite("Get user profile")

    @allure.title("Get user profile with provided incorrect username:")
    @pytest.mark.parametrize("case_role, username", [
        pytest.param("user_bob","", id="Empty string"),
        pytest.param("user_bob","A"*1000, id="Too long user_name"),
        pytest.param("user_bob","\\", id="Special character"),
        pytest.param("user_bob","enrico", id="Not existed user_name"),
    ])
    def test_get_user_profile_not_valid(self, case_role, username):
        user_service = self.get_actor(case_role).users_api
        user_service.get_user_profile(username=username, status_code=404, expected_success=False)

    @allure.feature("Update user profile")
    @allure.suite("Update user profile")
    @allure.sub_suite("Update user profile")

    @allure.title("Update me using payload ({case.payload})")
    @pytest.mark.parametrize("case", [
        pytest.param(UpdateMePayloadByRoleTestCase(role="user_bob",
                                            payload=UpdateMePayload(display_name="a")),
                     id="Min display name"),
        pytest.param(UpdateMePayloadByRoleTestCase(role="user_bob",
                                            payload=UpdateMePayload(display_name="a"*100)),
                     id="Max display name"),
        pytest.param(UpdateMePayloadByRoleTestCase(role="user_bob",
                                            payload=UpdateMePayload(bio="a"*500)),
                     id="Max bio"),
        pytest.param(UpdateMePayloadByRoleTestCase(role="user_bob",
                                                   payload=UpdateMePayload(bio=None)),
                     id="Clear bio"),
        pytest.param(UpdateMePayloadByRoleTestCase(role="user_bob",
                                                   payload=UpdateMePayload(is_private=True)),
                     id="is_private - true"),
        pytest.param(UpdateMePayloadByRoleTestCase(role="user_bob",
                                                   payload=UpdateMePayload(is_private=False)),
                     id="is_private - false"),

    ])
    @allure.description(f"Update user profile using provided data set")
    def test_update_profile(self, case):
        api_client = self.get_actor(case.role)
        auth_service = api_client.auth_api
        user_service = api_client.users_api

        with allure.step(f"Check user profile data before changes"):
            me_profile = auth_service.get_me()
            payload_before_get_me = UpdateMePayload(is_private=me_profile.is_private, display_name=me_profile.display_name, bio=me_profile.bio)
        updated_profile_response = user_service.update_profile(payload=case.payload)
        with allure.step(f"Check user profile data after changes"):
            me_profile_after = auth_service.get_me()
            payload_after_get_me = UpdateMePayload(is_private=me_profile_after.is_private, display_name=me_profile_after.display_name,
                                             bio=me_profile_after.bio)
            if case.payload.display_name:
                assert updated_profile_response.display_name == case.payload.display_name, "Error, Update profile: display_name info isn't matched expected"
                assert payload_after_get_me.display_name == case.payload.display_name, "Error, Get ME: display_name info isn't matched expected"
            if case.payload.bio:
                assert updated_profile_response.bio == case.payload.bio, "Error, Update profile: bio info isn't matched expected"
                assert payload_after_get_me.bio == case.payload.bio, "Error, Get ME: bio info isn't matched expected"
            if case.payload.is_private:
                assert updated_profile_response.is_private == case.payload.is_private, "Error, Update profile: is_private info isn't matched expected"
                assert payload_after_get_me.is_private == case.payload.is_private, "Error, Get ME: is_private info isn't matched expected"
        with allure.step(f"Reset changes after test case"):
            user_service.update_profile(payload=payload_before_get_me)


    @allure.feature("Upload Avatar")
    @allure.suite("Upload Avatar")
    @allure.sub_suite("Upload Avatar")

    @allure.title("Upload Avatar")
    @pytest.mark.parametrize("case", [
        pytest.param(UpdateAvatarByRoleTestCase(role="admin", file=UpdateAvatarFilePayload(file_name="image.jpg")),
                     id="Upload image, allowed - jpg"),
        pytest.param(UpdateAvatarByRoleTestCase(role="user_bob", file=UpdateAvatarFilePayload(file_name="image.png")),
                     id="Upload image, allowed - png"),
        pytest.param(UpdateAvatarByRoleTestCase(role="moderator", file=UpdateAvatarFilePayload(file_name="image.webp")),
                     id="Upload image, allowed - webp"),
        pytest.param(UpdateAvatarByRoleTestCase(role="user_eve", file=UpdateAvatarFilePayload(file_name="image.gif")),
                     id="Upload image, allowed - gif"),
        pytest.param(UpdateAvatarByRoleTestCase(role="user_eve", file=UpdateAvatarFilePayload(file_name="image.jpeg")),
                     id="Upload image, allowed - jpeg"),
        pytest.param(UpdateAvatarByRoleTestCase(role="user_eve", file=UpdateAvatarFilePayload(file_name="4.2-MB.jpg")),
                     id="Upload image, 4 MB < Size 5 Mb"),
    ])
    def test_upload_avatar(self, case):
        api_client = self.get_actor(case.role)
        user_service = api_client.users_api
        auth_service = api_client.auth_api

        with allure.step("Check current user's avatar"):
            current_profile = auth_service.get_me()
            current_avatar = current_profile.avatar_url

        updated_profile_response = user_service.update_profile_avatar(image_name=case.file.file_name)

        with allure.step("Check updated user's avatar"):
            updated_profile = auth_service.get_me()
            updated_avatar = updated_profile.avatar_url

            assert updated_profile.avatar_url != current_avatar, "Avatar isn't changed after update"
            assert updated_profile_response.avatar_url == updated_avatar, "New avatar at response and get me request aren't equal"


    @allure.feature("Upload Avatar")
    @allure.suite("Upload Avatar")
    @allure.sub_suite("Upload Avatar")

    @allure.title("Upload Avatar, incorrect file")
    @pytest.mark.parametrize("case", [
        pytest.param(UpdateAvatarByRoleTestCase(role="admin", file=UpdateAvatarFilePayload(file_name="test.txt")),
                     id="Upload image, not allowed - txt"),
        pytest.param(UpdateAvatarByRoleTestCase(role="admin", file=UpdateAvatarFilePayload(file_name="image.svg")),
                     id="Upload image, not allowed - svg"),
        pytest.param(UpdateAvatarByRoleTestCase(role="admin", file=UpdateAvatarFilePayload(file_name="image.exe")),
                     id="Upload image, not allowed - exe"),
        pytest.param(UpdateAvatarByRoleTestCase(role="admin", file=UpdateAvatarFilePayload(file_name="image.zip")),
                     id="Upload image, not allowed - zip"),
        pytest.param(UpdateAvatarByRoleTestCase(role="admin", file=UpdateAvatarFilePayload(file_name="image.png.jpg")),
                     id="Upload image, not allowed - .png.jpg"),
        pytest.param(UpdateAvatarByRoleTestCase(role="admin", file=UpdateAvatarFilePayload(file_name="7.2-MB.jpg")),
                     id="Upload image, too large > 5 Mb"),
    ])
    def test_upload_avatar_incorrect_file(self, case):
        user_service = self.get_actor(case.role).users_api
        user_service.update_profile_avatar(image_name=case.file.file_name, expected_success=False, status_code=400)


    @allure.feature("Delete  avatar")
    @allure.suite("Delete Avatar")
    @allure.sub_suite("Delete Avatar")

    @allure.title("Delete existed avatar")
    @pytest.mark.parametrize("case", ["user_bob"])
    def test_delete_avatar(self, case, add_avatar_to_profile):
        # Precondition - add avatar
        add_avatar_to_profile(case)

        api_client = self.get_actor(case)
        user_service = api_client.users_api
        auth_service = api_client.auth_api
        with allure.step("Check current user's avatar"):
            current_avatar = auth_service.get_me().avatar_url
        user_service.delete_profile_avatar()
        with allure.step("Compare new avatar with avatar before"):
            updated_avatar = auth_service.get_me().avatar_url
            assert current_avatar != updated_avatar


    @allure.feature("Delete  avatar")
    @allure.suite("Delete Avatar")
    @allure.sub_suite("Delete Avatar")

    @allure.title("Delete avatar - no avatar before")
    @pytest.mark.parametrize("case", ["user_bob"])
    def test_delete_avatar(self, case, add_avatar_to_profile):
        # Precondition - add avatar
        add_avatar_to_profile(case)

        api_client = self.get_actor(case)
        user_service = api_client.users_api
        auth_service = api_client.auth_api
        with allure.step("Check current user's avatar"):
            current_avatar = auth_service.get_me().avatar_url
        user_service.delete_profile_avatar()
        user_service.delete_profile_avatar()
        with allure.step("Compare new avatar with avatar before"):
            updated_avatar = auth_service.get_me().avatar_url
            assert current_avatar != updated_avatar


    @allure.feature("Get users post")
    @allure.suite("Get users post")
    @allure.sub_suite("Get users post")
    @allure.title("Get users post - with params ({case.params})")
    @pytest.mark.parametrize("case", [
        pytest.param(GetUserPostsParamsByRoleTestCase(role="user_bob", requested_user="admin",
                                            params=GetUserPostsParams(page=1, per_page=1)), id="per_page, min allowed value"),
        pytest.param(GetUserPostsParamsByRoleTestCase(role="moderator", requested_user="admin",
                                            params=GetUserPostsParams(page=1, per_page=100)), id="per_page, max allowed value"),
        pytest.param(GetUserPostsParamsByRoleTestCase(role="admin", requested_user="user_bob",
                                                      params=GetUserPostsParams(page=2, per_page=10)),id="2nd+ page of content"),
        pytest.param(GetUserPostsParamsByRoleTestCase(role="user_bob", requested_user="user_bob",
                                                      params=GetUserPostsParams(page=1, per_page=10)),id="request own pages"),

    ])
    def test_get_user_posts(self, case, db_get_username):
        requested_user_name = db_get_username(case.requested_user)
        user_service = self.get_actor(case.role).users_api
        user_service.get_user_posts(requested_user_name, params=case.params)

    @allure.feature("Get users post")
    @allure.suite("Get users post")
    @allure.sub_suite("Get users post")

    @allure.title("Get users post - with invalid params ({case.params})")
    @pytest.mark.parametrize("case", [
        pytest.param(GetUserPostsParamsByRoleTestCase(role="user_bob",params=GetUserPostsParams(page=0, per_page=10)),
                     id="page, below min allowed value"),
        pytest.param(GetUserPostsParamsByRoleTestCase(role="user_bob",params=GetUserPostsParams(page=1, per_page=0)),
                     id="per_page, below min allowed value"),
        pytest.param(GetUserPostsParamsByRoleTestCase(role="user_bob",params=GetUserPostsParams(page=1, per_page=101)),
                     id="per_page, above max allowed value"),
        pytest.param(GetUserPostsParamsByRoleTestCase(role="user_bob",params=GetUserPostsParams(page=1 * 10**200, per_page=10)),
                     id="page, too large value"),
    ])
    def test_get_user_posts_invalid_params(self, case):
        api_client = self.get_actor(case.role)
        user_service = api_client.users_api
        auth_service = api_client.auth_api

        profile_user_name = auth_service.get_me().username

        user_service.get_user_posts(profile_user_name, params=case.params, status_code=422, expected_success=False)

    @allure.feature("Get users post")
    @allure.suite("Get users post")
    @allure.sub_suite("Get users post")

    @allure.title("Get users post - not existed user_name ({case.params})")
    @pytest.mark.parametrize("case", [
        pytest.param(GetUserPostsParamsByRoleTestCase(role="user_bob", requested_user="testtesttest", params=GetUserPostsParams(page=1, per_page=10)),
                     id="request post of user with not existed user_name"),
    ])
    def test_get_user_posts_not_existed(self, case):
        user_service = self.get_actor(case.role).users_api
        user_service.get_user_posts(user_name=case.requested_user, params=case.params, status_code=404, expected_success=False)


    @allure.feature("Get user followers")
    @allure.suite("Get user followers")
    @allure.sub_suite("Get user followers")

    @allure.title("Return followers of user ({case.requested_user}) with query params ({case.params})")
    @pytest.mark.parametrize("case", [
        pytest.param(GetFollowersParamsByRoleTestCase(role="user_bob", requested_user="admin",
                                                      params=GetFollowersParams(page=1, per_page=1)),
                                                      id="per_page, min allowed value"),
        pytest.param(GetFollowersParamsByRoleTestCase(role="user_bob", requested_user="admin",
                                                      params=GetFollowersParams(page=1, per_page=100)),
                                                      id="per_page, max allowed value"),
        pytest.param(GetFollowersParamsByRoleTestCase(role="user_bob", requested_user="admin",
                                                      params=GetFollowersParams(page=2, per_page=10)),
                                                      id="2nd page of followers"),
        pytest.param(GetFollowersParamsByRoleTestCase(role="user_bob", requested_user="user_bob",
                                                      params=GetFollowersParams(page=2, per_page=10)),
                                                      id="request own followers list"),
    ])
    def test_get_user_followers(self,  case, db_get_username):
        requested_user_name = db_get_username(case.requested_user)
        user_service = self.get_actor(case.role).users_api

        user_service.get_user_followers(user_name=requested_user_name, params=case.params)


    @allure.feature("Get user followers")
    @allure.suite("Get user followers")
    @allure.sub_suite("Get user followers")
    @allure.title("Return followers with invalid params ({case.params})")
    @pytest.mark.parametrize("case", [
        pytest.param(GetFollowersParamsByRoleTestCase(role="user_bob", requested_user="admin",
                                                      params=GetFollowersParams(page=0)),
                                                      id="page, below min allowed value"),
        pytest.param(GetFollowersParamsByRoleTestCase(role="user_bob", requested_user="admin",
                                                      params=GetFollowersParams(per_page=0)),
                                                      id="per_page, below min allowed value"),
        pytest.param(GetFollowersParamsByRoleTestCase(role="user_bob", requested_user="admin",
                                                      params=GetFollowersParams(per_page=101)),
                                                      id="per_page, above max allowed value"),
        pytest.param(GetFollowersParamsByRoleTestCase(role="user_bob", requested_user="admin",
                                                      params=GetFollowersParams(page=1*10**100)),
                                                      id="page, too large value"),
        pytest.param(GetFollowersParamsByRoleTestCase(role="user_bob", requested_user="admin",
                                                      params=GetFollowersParams(per_page=1*10**100)),
                                                      id="per_page, too large value"),
    ])
    def test_get_user_followers_invalid_params(self, case):
        requested_user_name = case.requested_user
        user_service = self.get_actor(case.role).users_api
        user_service.get_user_followers(user_name=requested_user_name, params=case.params, expected_success=False, status_code=422)

    @allure.feature("Get user followers")
    @allure.suite("Get user followers")
    @allure.sub_suite("Get user followers")

    @allure.title("Return followers list of user with unexisted user_name ({case.requested_user})")
    @pytest.mark.parametrize("case", [
        pytest.param(GetFollowersParamsByRoleTestCase(role="user_bob", requested_user="testtesttest",
                                                      params=GetFollowersParams(page=1, per_page=10)),
                                                      id="followers list of not existed user"),
    ])
    def test_get_user_followers_not_existed(self, case):
        user_service = self.get_actor(case.role).users_api
        user_service.get_user_followers(user_name=case.requested_user, params=case.params, expected_success=False, status_code=404)



    @allure.title("Get user following, user: {username}")

    @allure.feature("Get user following list")
    @allure.suite("Get user following list")
    @allure.sub_suite("Get user following list")
    @allure.title("Return following list of user ({case.requested_user}) with query params ({case.params})")
    @pytest.mark.parametrize("case", [
        pytest.param(GetFollowingParamsByRoleTestCase(role="user_bob", requested_user="admin",
                                                      params=GetFollowingParams(page=1, per_page=1)),
                                                      id="per_page, min allowed value"),
        pytest.param(GetFollowingParamsByRoleTestCase(role="user_bob", requested_user="admin",
                                                      params=GetFollowingParams(page=1, per_page=100)),
                                                      id="per_page, max allowed value"),
        pytest.param(GetFollowingParamsByRoleTestCase(role="user_bob", requested_user="admin",
                                                      params=GetFollowingParams(page=2, per_page=10)),
                                                      id="2nd page of followers"),
        pytest.param(GetFollowingParamsByRoleTestCase(role="user_bob", requested_user="user_bob",
                                                      params=GetFollowingParams(page=2, per_page=10)),
                                                      id="request own followers list"),
    ])
    def test_get_user_following(self, case, db_get_username):
        requested_user_name = db_get_username(case.requested_user)
        user_service = self.get_actor(case.role).users_api
        user_service.get_user_following(requested_user_name, params=case.params)


    @allure.feature("Get user following list")
    @allure.suite("Get user following list")
    @allure.sub_suite("Get user following list")

    @allure.title("Return following with invalid params ({case.params})")
    @pytest.mark.parametrize("case", [
        pytest.param(GetFollowingParamsByRoleTestCase(role="user_bob", requested_user="admin",
                                                      params=GetFollowingParams(page=0)),
                                                      id="page, below min allowed value"),
        pytest.param(GetFollowingParamsByRoleTestCase(role="user_bob", requested_user="admin",
                                                      params=GetFollowingParams(per_page=0)),
                                                      id="per_page, below min allowed value"),
        pytest.param(GetFollowingParamsByRoleTestCase(role="user_bob", requested_user="admin",
                                                      params=GetFollowingParams(per_page=101)),
                                                      id="per_page, above max allowed value"),
        pytest.param(GetFollowingParamsByRoleTestCase(role="user_bob", requested_user="admin",
                                                      params=GetFollowingParams(page=1*10**100)),
                                                      id="page, too large value"),
        pytest.param(GetFollowingParamsByRoleTestCase(role="user_bob", requested_user="admin",
                                                      params=GetFollowingParams(per_page=1*10**100)),
                                                      id="per_page, too large value"),
    ])
    def test_get_user_following_invalid_params(self, case):
        requested_user_name = case.requested_user
        user_service = self.get_actor(case.role).users_api
        user_service.get_user_following(user_name=requested_user_name, params=case.params, expected_success=False, status_code=422)


    @allure.feature("Get user following list")
    @allure.suite("Get user following list")
    @allure.sub_suite("Get user following list")

    @allure.title("Return following list list of user with unexisted user_name ({case.requested_user})")
    @pytest.mark.parametrize("case", [
        pytest.param(GetFollowingParamsByRoleTestCase(role="user_bob", requested_user="testtesttest",
                                                      params=GetFollowingParams(page=1, per_page=10)),
                                                      id="followers list of not existed user"),
    ])
    def test_get_user_following_not_existed(self, case):
        user_service = self.get_actor(case.role).users_api
        user_service.get_user_following(user_name=case.requested_user, params=case.params, expected_success=False, status_code=404)