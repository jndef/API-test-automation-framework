import allure
import pytest

from config.base_test import BaseTest
from services.admin.params import AdminGetAllUsersParams, AdminGetAllUsersParamsByRoleTestCase, \
    AdminGetAllPostsParamsByRoleTestCase, AdminGetAllPostsParams, AdminDeletePostParamsByRoleTestCase, \
    AdminDeletePostParams
from services.admin.payloads import UpdateUserByAdminPayloadByRoleTestCase, UpdateUserByAdminPayload


@allure.epic("Admin Service")
@allure.parent_suite("Tests Admin service API")
@allure.title("Tests Admin service API")
@pytest.mark.admin
class TestAdmin(BaseTest):

    @allure.feature("Get Stats")
    @allure.suite("Get Stats")
    @allure.sub_suite("Get Stats")
    @allure.story("Admin can see platform stats")
    @allure.title("Get Stats")
    @pytest.mark.parametrize("case ", [
        "admin",
        "moderator",
    ])
    @pytest.mark.smoke
    def test_get_stats(self, case):
        admin_service = self.get_actor(case).admin_api
        admin_service.get_stats()

    @allure.feature("Get Stats")
    @allure.suite("Get Stats")
    @allure.sub_suite("Get Stats")
    @allure.story("Admin can see platform stats")
    @allure.title("Get Stats - invalid role")
    @pytest.mark.parametrize("case ", [
        "user_bob",
    ])
    @pytest.mark.smoke
    def test_get_stats_invalid_role(self, case):
        admin_service = self.get_actor(case).admin_api
        admin_service.get_stats(status_code=403, expected_success=False)

    @allure.feature("Get Stats")
    @allure.suite("Get Stats")
    @allure.sub_suite("Get Stats")
    @allure.story("Admin can see platform stats")
    @allure.title("Get users with params ({case.params})")
    @pytest.mark.parametrize("case", [
        pytest.param(AdminGetAllUsersParamsByRoleTestCase(role="admin", search_query="admin",
                                                          params=AdminGetAllUsersParams(page=1, per_page=100,
                                                                                        sort_by="username",
                                                                                        sort_order="asc",
                                                                                        is_active=True, role="admin")),
                     id="max per_page, sort_by - username, sort_order - asc, min page, role - admin"),
        pytest.param(AdminGetAllUsersParamsByRoleTestCase(role="admin", search_query="user_bob",
                                                          params=AdminGetAllUsersParams(sort_by="email",
                                                                                        sort_order="desc",
                                                                                        is_active=False, role="user")),
                     id="sort_by - email, sort_order - desc, role - user"),
        pytest.param(AdminGetAllUsersParamsByRoleTestCase(role="admin", search_query="admin",
                                                          params=AdminGetAllUsersParams(sort_by="created_at",
                                                                                        is_active=False, role="admin")),
                     id="sort_by - created_at, is_active - False, role - admin"),
        pytest.param(AdminGetAllUsersParamsByRoleTestCase(role="admin", search_query="user_alice",
                                                          params=AdminGetAllUsersParams(is_active=True, role="user")),
                     id="is_active - True, role - user"),
        pytest.param(AdminGetAllUsersParamsByRoleTestCase(role="admin", search_query="moderator",
                                                          params=AdminGetAllUsersParams(is_active=True,
                                                                                        role="moderator", per_page=1)),
                     id="is_active - True, role - moderator, per_page - 1"),
    ])
    @pytest.mark.smoke
    def test_get_all_users(self, case):
        searched_user_api_client = self.get_actor(case.search_query)
        searched_user_username: str = searched_user_api_client.auth_api.get_me().username
        api_client = self.get_actor(case.role)
        api_client.admin_api.get_list_all_users(params=case.params, search_query=searched_user_username)

    @allure.feature("Get List All Users")
    @allure.suite("Get List All Users")
    @allure.sub_suite("Get List All Users")
    @allure.story("Admin can see existed users")
    @allure.title("Get List All Users with invalid params ({case.params})")
    @pytest.mark.parametrize("case", [
        pytest.param(AdminGetAllUsersParamsByRoleTestCase(role="admin", search_query="admin",
                                                          params=AdminGetAllUsersParams(per_page=0)),
                     id="per_page - 0"),
        pytest.param(AdminGetAllUsersParamsByRoleTestCase(role="admin", search_query="admin",
                                                          params=AdminGetAllUsersParams(per_page=101)),
                     id="per_page - 101"),
        pytest.param(AdminGetAllUsersParamsByRoleTestCase(role="admin", search_query="admin",
                                                          params=AdminGetAllUsersParams(per_page=-1)),
                     id="per_page - -1"),
        pytest.param(AdminGetAllUsersParamsByRoleTestCase(role="admin", search_query="admin",
                                                          params=AdminGetAllUsersParams(page=0)),
                     id="page - 0"),
        pytest.param(AdminGetAllUsersParamsByRoleTestCase(role="admin", search_query="admin",
                                                          params=AdminGetAllUsersParams(sort_by="test")),
                     id="sort_by - test"),
        pytest.param(AdminGetAllUsersParamsByRoleTestCase(role="admin", search_query="admin",
                                                          params=AdminGetAllUsersParams(sort_order="test")),
                     id="sort_order - test"),
    ])
    @pytest.mark.smoke
    def test_get_all_users_invalid_params(self, case):
        api_client = self.get_actor(case.role)
        api_client.admin_api.get_list_all_users(params=case.params, search_query=case.search_query,
                                                expected_success=False, status_code=422)

    @allure.feature("Get List All Users")
    @allure.suite("Get List All Users")
    @allure.sub_suite("Get List All Users")
    @allure.story("Admin can see existed users")
    @allure.title("Get List All Users by invalid user ({case})")
    @pytest.mark.parametrize("case ", [
        "user_bob",
    ])
    def test_get_all_users_invalid_role(self, case):
        admin_service = self.get_actor(case).admin_api
        admin_service.get_list_all_users(params=AdminGetAllUsersParams(), search_query=case, status_code=403,
                                         expected_success=False)

    @allure.feature("Update certain user by admin")
    @allure.suite("Update certain user by admin")
    @allure.sub_suite("Update certain user by admin")
    @allure.story("Admin can update user's profile data ")
    @allure.title("Update certain user by admin - is_verified ({case.payload.is_verified})")
    @pytest.mark.parametrize("case ", [
        pytest.param(UpdateUserByAdminPayloadByRoleTestCase(case_role="admin",
                                                            payload=UpdateUserByAdminPayload(is_verified=True),
                                                            updated_user="user_bob"),
                     id="Update user - is_verified - True"),
        pytest.param(UpdateUserByAdminPayloadByRoleTestCase(case_role="moderator",
                                                            payload=UpdateUserByAdminPayload(is_verified=False),
                                                            updated_user="user_bob"),
                     id="Update user - is_verified - False"),
    ])
    def test_admin_update_user_verified(self, case, get_me_of_certain_user):
        admin_service = self.get_actor(case.case_role).admin_api
        searched_user = get_me_of_certain_user(case.updated_user)
        updated_user = admin_service.update_user_by_admin(user_id=searched_user.user_id, payload=case.payload)
        assert updated_user.is_verified == case.payload.is_verified, f"is_verified isn't changed. ER/AR: {case.payload.is_verified}/{updated_user.is_verified}"
        # reset back
        admin_service.update_user_by_admin(user_id=searched_user.user_id,
                                           payload=UpdateUserByAdminPayload(is_verified=searched_user.is_verified,
                                                                            is_active=searched_user.is_active,
                                                                            role=searched_user.role))

    @allure.feature("Update certain user by admin")
    @allure.suite("Update certain user by admin")
    @allure.sub_suite("Update certain user by admin")
    @allure.story("Admin can update user's profile data")
    @allure.title("Attempt to Update certain user by user - is_verified ({case.payload.is_active})")
    @pytest.mark.parametrize("case_role ", [
        "user_bob",
    ])
    def test_admin_update_user_verified_no_rights(self, case_role, get_me_of_certain_user):
        admin_service = self.get_actor(case_role).admin_api
        searched_user = get_me_of_certain_user(case_role)
        payload = UpdateUserByAdminPayload(is_verified=False)
        admin_service.update_user_by_admin(user_id=searched_user.user_id, payload=payload, status_code=403,
                                           expected_success=False)

    @allure.feature("Update certain user by admin")
    @allure.suite("Update certain user by admin")
    @allure.sub_suite("Update certain user by admin")
    @allure.story("Admin can update user's profile data")
    @allure.title("Update certain user by admin - is_active ({case.payload.is_active})")
    @pytest.mark.parametrize("case ", [
        pytest.param(UpdateUserByAdminPayloadByRoleTestCase(case_role="admin",
                                                            payload=UpdateUserByAdminPayload(is_active=True),
                                                            updated_user="user_bob"),
                     id="Update user - is_active - True"),
        pytest.param(UpdateUserByAdminPayloadByRoleTestCase(case_role="admin",
                                                            payload=UpdateUserByAdminPayload(is_active=False),
                                                            updated_user="user_bob"),
                     id="Update user - is_active - False"),
    ])
    def test_admin_update_user_active(self, case, get_me_of_certain_user):
        admin_service = self.get_actor(case.case_role).admin_api
        searched_user = get_me_of_certain_user(case.updated_user)
        updated_user = admin_service.update_user_by_admin(user_id=searched_user.user_id, payload=case.payload)
        assert updated_user.is_active == case.payload.is_active, f"is_active isn't changed. ER/AR: {case.payload.is_active}/{updated_user.is_active}"
        # reset back
        admin_service.update_user_by_admin(user_id=searched_user.user_id,
                                           payload=UpdateUserByAdminPayload(is_verified=searched_user.is_verified,
                                                                            is_active=searched_user.is_active,
                                                                            role=searched_user.role))

    @allure.feature("Update certain user by admin")
    @allure.suite("Update certain user by admin")
    @allure.sub_suite("Update certain user by admin")
    @allure.story("Admin can update user's profile data")
    @allure.title("Attempt to Update certain user (is_active) by user ({case_role})")
    @pytest.mark.parametrize("case_role ", [
        "user_bob",
        "moderator",
    ])
    def test_admin_update_user_active_no_rights(self, case_role, get_me_of_certain_user):
        admin_service = self.get_actor(case_role).admin_api
        searched_user = get_me_of_certain_user(case_role)
        payload = UpdateUserByAdminPayload(is_active=False)
        admin_service.update_user_by_admin(user_id=searched_user.user_id, payload=payload, status_code=403,
                                           expected_success=False)

    @allure.feature("Update certain user by admin")
    @allure.suite("Update certain user by admin")
    @allure.sub_suite("Update certain user by admin")
    @allure.story("Admin can update user's profile data")
    @allure.title("Update certain user by admin - is_active ({case.payload.is_active})")
    @pytest.mark.parametrize("case ", [
        pytest.param(UpdateUserByAdminPayloadByRoleTestCase(case_role="admin",
                                                            payload=UpdateUserByAdminPayload(role="admin"),
                                                            updated_user="user_bob"),
                     id="admin, Update user's role for user (admin)"),
        pytest.param(UpdateUserByAdminPayloadByRoleTestCase(case_role="admin",
                                                            payload=UpdateUserByAdminPayload(role="moderator"),
                                                            updated_user="user_bob"),
                     id="admin, Update user's role for user (moderator)"),
        pytest.param(UpdateUserByAdminPayloadByRoleTestCase(case_role="admin",
                                                            payload=UpdateUserByAdminPayload(role="admin"),
                                                            updated_user="moderator"),
                     id="admin, Update user's role for moderator (admin)"),
        pytest.param(UpdateUserByAdminPayloadByRoleTestCase(case_role="admin",
                                                            payload=UpdateUserByAdminPayload(role="user"),
                                                            updated_user="moderator"),
                     id="admin, Update user's role for moderator (user)"),

    ])
    def test_admin_update_user_role(self, case, get_me_of_certain_user):
        admin_service = self.get_actor(case.case_role).admin_api
        searched_user = get_me_of_certain_user(case.updated_user)
        updated_user = admin_service.update_user_by_admin(user_id=searched_user.user_id, payload=case.payload)
        assert updated_user.role == case.payload.role, f"role isn't changed. ER/AR: {case.payload.role}/{updated_user.role}"
        # reset back
        admin_service.update_user_by_admin(user_id=searched_user.user_id,
                                           payload=UpdateUserByAdminPayload(is_verified=searched_user.is_verified,
                                                                            is_active=searched_user.is_active,
                                                                            role=searched_user.role))

    @allure.feature("Update certain user by admin")
    @allure.suite("Update certain user by admin")
    @allure.sub_suite("Update certain user by admin")
    @allure.story("Admin can update user's profile data")
    @allure.title("role {case_role}. Attempt to Update certain user ({updated_user}), set role: ({new_role})")
    @pytest.mark.parametrize("case_role, updated_user, new_role", [
        pytest.param("user_bob", "moderator", "admin",
                     id="user, Attempt to update user's role for moderator (-> user)"),
        pytest.param("user_bob", "moderator", "user",
                     id="user, Attempt to update user's role for moderator (-> user)"),
        pytest.param("user_bob", "admin", "user",
                     id="user, user, Attempt to update user's role for admin (-> user)"),
        pytest.param("user_bob", "admin", "moderator",
                     id="user, user, Attempt to update user's role for admin (-> moderator)"),
        pytest.param("user_bob", "user_eve", "moderator",
                     id="user, user, Attempt to update user's role for user (-> moderator)"),
        pytest.param("user_bob", "user_eve", "admin",
                     id="user, user, Attempt to update user's role for user (-> admin)"),
        pytest.param("moderator", "user_bob", "admin",
                     id="moderator, Attempt to update user's role for user (-> admin)"),
        pytest.param("moderator", "user_bob", "moderator",
                     id="moderator, Attempt to update user's role for user (-> moderator)"),
        pytest.param("moderator", "admin", "moderator",
                     id="moderator, Attempt to update user's role for admin (-> moderator)"),
        pytest.param("moderator", "admin", "user",
                     id="moderator, Attempt to update user's role for admin (-> user)"),
    ])
    def test_admin_update_user_role_no_rights(self, case_role, updated_user, new_role, get_me_of_certain_user):
        admin_service = self.get_actor(case_role).admin_api
        searched_user = get_me_of_certain_user(updated_user)
        payload = UpdateUserByAdminPayload(role=new_role)
        admin_service.update_user_by_admin(user_id=searched_user.user_id, payload=payload, status_code=403,
                                           expected_success=False)

    @allure.feature("Update certain user by admin")
    @allure.suite("Update certain user by admin")
    @allure.sub_suite("Update certain user by admin")
    @allure.story("Admin can update user's profile data")
    @allure.title("Attempt to Update certain user, not existed user")
    @pytest.mark.parametrize("case_role", [
        pytest.param("admin",
                     id="user, Attempt to update user's role for moderator (-> user)"),
    ])
    def test_admin_update_user_not_existed(self, case_role):
        admin_service = self.get_actor(case_role).admin_api
        searched_user = self.data_helper.get_not_existed_uuid()
        payload = UpdateUserByAdminPayload(is_verified=True)
        admin_service.update_user_by_admin(user_id=searched_user, payload=payload, status_code=404,
                                           expected_success=False)

    @allure.feature("Update certain user by admin")
    @allure.suite("Update certain user by admin")
    @allure.sub_suite("Update certain user by admin")
    @allure.story("Admin can update user's profile data")
    @allure.title("Attempt to Update certain user, not valid user id")
    @pytest.mark.parametrize("case_role", [
        pytest.param("admin",
                     id="user, Attempt to update user's role for moderator (-> user)"),
    ])
    def test_admin_update_user_not_valid_uuid(self, case_role):
        admin_service = self.get_actor(case_role).admin_api
        searched_user = self.data_helper.get_invalid_uuid()
        payload = UpdateUserByAdminPayload(is_verified=True)
        admin_service.update_user_by_admin(user_id=searched_user, payload=payload, status_code=422,
                                           expected_success=False)

    @allure.feature("Deactivate certain user by admin")
    @allure.suite("Deactivate certain user by admin")
    @allure.sub_suite("Deactivate certain user by admin")
    @allure.story("Admin can deactivate user account")
    @allure.title("Deactivate certain user")
    @pytest.mark.parametrize("case_role", [
        pytest.param("admin",
                     id="admin, deactivate user"),
    ])
    def test_deactivate_user(self, case_role, register_new_account):
        admin_service = self.get_actor(case_role).admin_api
        registered_user = register_new_account
        admin_service.deactivate_user_by_admin(user_id=registered_user.user_id)

    @allure.feature("Deactivate certain user by admin")
    @allure.suite("Deactivate certain user by admin")
    @allure.sub_suite("Deactivate certain user by admin")
    @allure.story("Admin can deactivate user account")
    @allure.title("Deactivate certain user")
    @pytest.mark.parametrize("case_role", [
        pytest.param("user_bob",
                     id="user, attempt to deactivate user"),
        pytest.param("moderator",
                     id="user, attempt to deactivate user"),
    ])
    def test_deactivate_user_by_non_admin(self, case_role, register_remove_new_account):
        admin_service = self.get_actor(case_role).admin_api
        registered_user = register_remove_new_account()
        admin_service.deactivate_user_by_admin(user_id=registered_user.user_id, expected_success=False, status_code=403)

    @allure.suite("Deactivate certain user by admin")
    @allure.sub_suite("Deactivate certain user by admin")
    @allure.story("Admin can deactivate user account")
    @allure.title("Deactivate certain user, not existed user id")
    @pytest.mark.parametrize("case_role", [
        pytest.param("admin",
                     id="attempt to deactivate user with not existed user id"),

    ])
    def test_deactivate_user_not_existed(self, case_role):
        admin_service = self.get_actor(case_role).admin_api
        registered_user = self.data_helper.get_not_existed_uuid()
        admin_service.deactivate_user_by_admin(user_id=registered_user, expected_success=False, status_code=404)

    @allure.suite("Deactivate certain user by admin")
    @allure.sub_suite("Deactivate certain user by admin")
    @allure.story("Admin can deactivate user account")
    @allure.title("Deactivate certain user, not valid user id")
    @pytest.mark.parametrize("case_role", [
        pytest.param("admin",
                     id="user, attempt to deactivate user"),

    ])
    def test_deactivate_user_not_valid_uuid(self, case_role):
        admin_service = self.get_actor(case_role).admin_api
        registered_user = self.data_helper.get_invalid_uuid()
        admin_service.deactivate_user_by_admin(user_id=registered_user, expected_success=False, status_code=422)

    @allure.feature("Get All Posts")
    @allure.suite("Get All Posts")
    @allure.sub_suite("Get All Posts")
    @allure.story("Admin can see all existed posts")
    @allure.title("Get All Posts with params ({case.params})")
    @pytest.mark.parametrize("case", [
        pytest.param(AdminGetAllPostsParamsByRoleTestCase(role="admin",
                                                          params=AdminGetAllPostsParams(per_page=1)),
                     id="min per_page"),
        pytest.param(AdminGetAllPostsParamsByRoleTestCase(role="admin",
                                                          params=AdminGetAllPostsParams(per_page=100)),
                     id="max per_page"),
        pytest.param(AdminGetAllPostsParamsByRoleTestCase(role="admin",
                                                          params=AdminGetAllPostsParams(page=1, per_page=10)),
                     id="page - min, per_page in allowed range"),
        pytest.param(AdminGetAllPostsParamsByRoleTestCase(role="admin",
                                                          params=AdminGetAllPostsParams(page=2, per_page=5)),
                     id="page - 2nd page, per_page in allowed range"),
    ])
    @pytest.mark.smoke
    def test_get_all_posts(self, case):

        api_client = self.get_actor(case.role)
        api_client.admin_api.get_list_all_posts(params=case.params)

    @allure.feature("Get All Posts")
    @allure.suite("Get All Posts")
    @allure.sub_suite("Get All Posts")
    @allure.story("Admin can see all existed posts")
    @allure.title("Get All Posts with filter is_deleted ({case.params.is_deleted})")
    @pytest.mark.parametrize("case", [
        pytest.param(AdminGetAllPostsParamsByRoleTestCase(role="admin",
                                                          params=AdminGetAllPostsParams(is_deleted=True)),
                     id="only deleted posts"),
        pytest.param(AdminGetAllPostsParamsByRoleTestCase(role="moderator",
                                                          params=AdminGetAllPostsParams(is_deleted=False)),
                     id="only deleted posts"),
    ])
    @pytest.mark.smoke
    def test_get_all_posts_with_filter(self, case):

        api_client = self.get_actor(case.role)
        all_posts = api_client.admin_api.get_list_all_posts(params=case.params)

        if case.params.is_deleted:
            assert all(post.is_deleted == True for post in all_posts.items)
        elif not case.params.is_deleted:
            assert all(post.is_deleted == False for post in all_posts.items)

    @allure.feature("Get All Posts")
    @allure.suite("Get All Posts")
    @allure.sub_suite("Get All Posts")
    @allure.story("Admin can see all existed posts")
    @allure.title("Request All Posts by non admin ({case.role})")
    @pytest.mark.parametrize("case", [
        pytest.param(AdminGetAllPostsParamsByRoleTestCase(role="user_bob",
                                                          params=AdminGetAllPostsParams()),
                     id="Attempt to request endpoint as user"),
    ])
    @pytest.mark.smoke
    def test_get_all_posts_by_non_admin(self, case):
        admin_service = self.get_actor(case.role).admin_api
        admin_service.get_list_all_posts(params=case.params, expected_success=False, status_code=403)

    @allure.feature("Remove existed posts by admin")
    @allure.suite("Remove existed posts by admin")
    @allure.sub_suite("Remove existed posts by admin")
    @allure.story("Admin can moderate/remove existed post")
    @allure.title("Moderate/remove existed post by ({case.role})")
    @pytest.mark.parametrize("case", [
        pytest.param(AdminDeletePostParamsByRoleTestCase(role="admin",
                                                         params=AdminDeletePostParams()),
                     id="Attempt to remove post by admin"),
        pytest.param(AdminDeletePostParamsByRoleTestCase(role="moderator",
                                                         params=AdminDeletePostParams()),
                     id="Attempt to remove post by moderator"),
    ])
    def test_admin_remove_post(self, case, create_and_get_post):
        api_client = self.get_actor(case.role)
        admin_service = api_client.admin_api
        post_service = api_client.posts_api
        prepared_post_id = create_and_get_post(case.role)
        admin_service.remove_post_by_admin(post_id=prepared_post_id, params=case.params)
        # check
        post_service.get_post(prepared_post_id, expected_success=False, status_code=404)
        removed_admin_posts_list = admin_service.get_list_all_posts(
            params=AdminGetAllPostsParams(is_deleted=True, page=1))

        post_at_response = next((post for post in removed_admin_posts_list.items if post.id == prepared_post_id), None)
        assert post_at_response is not None, f"Post with ID {prepared_post_id} not found in removed posts"
        assert post_at_response.is_deleted

    @allure.feature("Remove existed posts by admin")
    @allure.suite("Remove existed posts by admin")
    @allure.sub_suite("Remove existed posts by admin")
    @allure.story("Admin can moderate/remove existed post")
    @allure.title("Moderate/remove existed post by general user ({case.role})")
    @pytest.mark.parametrize("case", [
        pytest.param(AdminDeletePostParamsByRoleTestCase(role="user_bob",
                                                         params=AdminDeletePostParams()),
                     id="Attempt to remove post by regular user"),
    ])
    def test_admin_remove_post_by_regular_user(self, case, build_post_remove):
        admin_service = self.get_actor(case.role).admin_api
        prepared_post_id = build_post_remove(case.role)
        admin_service.remove_post_by_admin(post_id=prepared_post_id, params=case.params, expected_success=False,
                                           status_code=403)

    @allure.feature("Remove existed posts by admin")
    @allure.suite("Remove existed posts by admin")
    @allure.sub_suite("Remove existed posts by admin")
    @allure.story("Admin can moderate/remove existed post")
    @allure.title("Moderate/remove existed post - removed post")
    @pytest.mark.parametrize("case", [
        pytest.param(AdminDeletePostParamsByRoleTestCase(role="admin",
                                                         params=AdminDeletePostParams()),
                     id="Attempt to remove post already removed"),
    ])
    def test_admin_remove_post_removed_already(self, case, get_removed_post):
        admin_service = self.get_actor(case.role).admin_api
        prepared_post_id = get_removed_post(case.role)
        admin_service.remove_post_by_admin(post_id=prepared_post_id, params=case.params, expected_success=False,
                                           status_code=404)

    @allure.feature("Remove existed posts by admin")
    @allure.suite("Remove existed posts by admin")
    @allure.sub_suite("Remove existed posts by admin")
    @allure.story("Admin can moderate/remove post with non existed post")
    @allure.title("Moderate/remove existed post - removed post")
    @pytest.mark.parametrize("case", [
        pytest.param(AdminDeletePostParamsByRoleTestCase(role="admin",
                                                         params=AdminDeletePostParams()),
                     id="Attempt to remove post - not existed"),
    ])
    def test_admin_remove_post_not_existed(self, case):
        admin_service = self.get_actor(case.role).admin_api
        prepared_post_id = self.data_helper.get_not_existed_uuid()
        admin_service.remove_post_by_admin(post_id=prepared_post_id, params=case.params, expected_success=False,
                                           status_code=404)

    @allure.feature("Remove existed posts by admin")
    @allure.suite("Remove existed posts by admin")
    @allure.sub_suite("Remove existed posts by admin")
    @allure.story("Admin can moderate/remove post with non existed post")
    @allure.title("Moderate/remove existed post - not valid uuid")
    @pytest.mark.parametrize("case", [
        pytest.param(AdminDeletePostParamsByRoleTestCase(role="admin",
                                                         params=AdminDeletePostParams()),
                     id="Attempt to remove post - not valid id"),
    ])
    def test_admin_remove_post_not_valid_uuid(self, case):
        admin_service = self.get_actor(case.role).admin_api
        prepared_post_id = self.data_helper.get_invalid_uuid()
        admin_service.remove_post_by_admin(post_id=prepared_post_id, params=case.params, expected_success=False,
                                           status_code=422)
