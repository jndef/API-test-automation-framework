import allure
import pytest

from config.base_test import BaseTest
from services.comments.params import GetCommentsByRoleTestCase, GetCommentsQueryParams, GetRepliesByRoleTestCase, \
    GetRepliesQueryParams
from services.comments.payloads import CreateCommentByRoleTestCase, CreateCommentBody, UpdateCommentBody, \
    UpdateCommentByRoleTestCase, UpdateCommentBodyQuery, CreateCommentBodyQuery


@allure.epic("Comments Service")
@allure.feature("Comments")
@allure.parent_suite("Tests Comments service API")
@allure.title("Tests Comments service API")
@pytest.mark.comments
class TestComments(BaseTest):

    @allure.suite("Get comments list")
    @allure.story("User can read existed comments to post")
    @allure.description("Get comment list")
    @pytest.mark.parametrize("case", [
        pytest.param(GetCommentsByRoleTestCase(role="user_eve",params=GetCommentsQueryParams(sort_by="created_at", sort_order="asc", page=1, per_page=1)),
            id="Get comment list - min boundaries with created_at asc sorting"),
        pytest.param(GetCommentsByRoleTestCase(role="moderator",params=GetCommentsQueryParams(sort_by="likes_count", sort_order="desc", page=2, per_page=10)),
            id="Get comment list - max per_page boundary with likes_count desc sorting"),
        pytest.param(GetCommentsByRoleTestCase(role="admin",params=GetCommentsQueryParams(sort_by="created_at")),
            id="Get comment list - with only sort by"),
        pytest.param(GetCommentsByRoleTestCase(role="user_eve",params=GetCommentsQueryParams()),
            id="Get comment list - with omitted optional params"),
    ])
    def test_get_comments_list(self, get_post_with_comments, case):
        comments_service = self.get_actor(case.role).comments_api
        prepared_post_id = get_post_with_comments(case.role)
        comments_service.get_list_comments(post_id=prepared_post_id, params=case.params)

    @allure.suite("Get comments list")
    @allure.story("User can read existed comments to post")
    @allure.description("Get posts list, incorrect - invalid payload")
    @pytest.mark.parametrize("case", [
        pytest.param(GetCommentsByRoleTestCase(role="user_eve",params=GetCommentsQueryParams(sort_by="sort_by")),
                     id="Get comment list - invalid payload, incorrect sort_by value"),
        pytest.param(GetCommentsByRoleTestCase(role="user_eve",params=GetCommentsQueryParams(sort_order="invalid_order")),
                     id="Get comment list - invalid payload, incorrect sort_order value"),
        pytest.param(GetCommentsByRoleTestCase(role="user_eve",params=GetCommentsQueryParams(page=0)),
                     id="Get comment list - invalid payload, page below minimum boundary"),
        pytest.param(GetCommentsByRoleTestCase(role="user_eve",params=GetCommentsQueryParams(per_page=0)),
                     id="Get comment list - invalid payload, per_page below minimum boundary"),
        pytest.param(GetCommentsByRoleTestCase(role="user_eve",params=GetCommentsQueryParams(per_page=101)),
                     id="Get comment list - invalid payload, er_page above maximum boundary"),
    ])
    def test_get_comments_list_invalid_payload(self, get_post_with_comments, case):
        comments_service = self.get_actor(case.role).comments_api
        prepared_post_id = get_post_with_comments(case.role)
        comments_service.get_list_comments(post_id=prepared_post_id,
                                            params=case.params,
                                            status_code=422,
                                            expected_success=False)

    @allure.suite("Get comments list")
    @allure.story("User can read existed comments to post")
    @allure.description("Get posts list, incorrect - Removed post")
    def test_get_comments_list_incorrect_not_existed(self, get_removed_post):
        comments_service = self.get_actor("user_eve").comments_api
        prepared_post_id = get_removed_post("user_eve")
        comments_service.get_list_comments(post_id=prepared_post_id)

    @allure.suite("Get comments list")
    @allure.story("User can read existed comments to post")
    @allure.description("Get posts list, incorrect  - not existed post id")
    def test_get_comments_list_incorrect_invalid_uuid(self):
        comments_service = self.get_actor("user_eve").comments_api
        prepared_post_id = self.data_helper.get_not_existed_uuid()
        comments_service.get_list_comments(post_id=prepared_post_id,
                                            status_code=404,
                                            expected_success=False)

    @allure.suite("Get comments list")
    @allure.story("User can read existed comments to post")
    @allure.description("Get posts list, incorrect - Invalid uuid")
    def test_get_comments_list_incorrect_removed_post(self):
        comments_service = self.get_actor("user_eve").comments_api
        prepared_post_id = self.data_helper.get_not_existed_uuid() + "yxz"
        comments_service.get_list_comments(post_id=prepared_post_id,
                                            status_code=422,
                                            expected_success=False)


    @allure.suite("Create new comment")
    @allure.story("User can create new comment to the post")
    @allure.description("Create comment to post")
    @pytest.mark.parametrize("case", [
        pytest.param(CreateCommentByRoleTestCase(role="user_eve",payload=CreateCommentBodyQuery(content="A")),
                     id="Valid minimal content boundary"),
        pytest.param(CreateCommentByRoleTestCase(role="user_eve",payload=CreateCommentBodyQuery(content="A"* 1000)),
                     id="Valid maximum content boundary"),
    ])
    def test_create_comment(self, case, build_post_remove, comment_cleaner):
        comments_service = self.get_actor(case.role).comments_api
        prepared_post_id = build_post_remove(case.role)
        comment = comments_service.create_comment(post_id=prepared_post_id, payload=case.payload)

        comment_cleaner(comment.id)  # регистрируем на удаление
        assert comment.content == case.payload.content, f"Created comment doesn't contain expected content.\nER: {case.payload.content}\nAR: {comment.content}"


    @allure.suite("Create new comment")
    @allure.story("User can create new comment to the post")
    @allure.description("Create comment to post, incorrect - invalid payload")
    @pytest.mark.parametrize("case", [
        pytest.param(CreateCommentByRoleTestCase(role="user_eve", payload=CreateCommentBodyQuery(content="")),
                     id="Invalid content below minimum boundary"),
        pytest.param(CreateCommentByRoleTestCase(role="user_bob", payload=CreateCommentBodyQuery(content="A"*1001)),
                     id="Invalid content above maximum boundary"),
        pytest.param(CreateCommentByRoleTestCase(role="user_eve", payload=CreateCommentBodyQuery()),
                     id="Missing required content field"),
    ])
    def test_create_comment_incorrect_invalid_payload(self,case, build_post_remove):
        comments_service = self.get_actor(case.role).comments_api
        prepared_post_id = build_post_remove(case.role)
        comments_service.create_comment(post_id=prepared_post_id,
                                         payload=case.payload,
                                         status_code=422,
                                         expected_success=False)

    @allure.suite("Create new comment")
    @allure.story("User can create new comment to the post")
    @pytest.mark.parametrize("case", [
        pytest.param(CreateCommentByRoleTestCase(role="user_bob", payload=CreateCommentBodyQuery(content="Valid comment"), expected_success=False, status_code=404),
                     id="Create comment to post - not existed post"),
    ])
    @allure.description("Create comment to post, incorrect - not existed post")
    def test_create_comment_incorrect_not_existed_post(self, case):
        comments_service = self.get_actor(case.role).comments_api
        prepared_post_id = self.data_helper.get_not_existed_uuid()
        comments_service.create_comment(post_id=prepared_post_id,
                                         payload=case.payload,
                                         status_code=case.status_code,
                                         expected_success=case.expected_success)

    @allure.suite("Create new comment")
    @allure.story("User can create new comment to the post")
    @allure.description("Create comment to post, incorrect - Removed post")
    @pytest.mark.parametrize("case", [
        pytest.param(CreateCommentByRoleTestCase(role="user_bob", payload=CreateCommentBodyQuery(content="Valid comment"), expected_success=False, status_code=404),
                     id="Create comment to post - Removed post"),
    ])
    def test_create_comment_removed_post(self, case, get_removed_post):
        comments_service = self.get_actor(case.role).comments_api
        prepared_post_id = get_removed_post(case.role)
        comments_service.create_comment(post_id=prepared_post_id,
                                         payload=case.payload,
                                         status_code=404,
                                         expected_success=False)

    @allure.suite("Create new comment")
    @allure.story("User can create new comment to the post")
    @pytest.mark.parametrize("case", [
        pytest.param(CreateCommentByRoleTestCase(role="user_bob", payload=CreateCommentBodyQuery(content="Valid comment"), expected_success=False, status_code=422),
                     id="Create comment to post - invalid post uuid")

    ])
    @allure.description("Create comment to post, incorrect - invalid post uuid")
    def test_create_comment_incorrect_invalid_uuid(self,case, get_incorrect_post):
        comments_service = self.get_actor(case.role).comments_api
        prepared_post_id = self.data_helper.get_not_existed_uuid()
        comments_service.create_comment(post_id=prepared_post_id,
                                         payload=case.payload,
                                         status_code=case.status_code,
                                         expected_success=case.expected_success)

    @allure.suite("Update existed comment")
    @allure.story("User can update existed comment")
    @allure.description("User can update existed comment - success")
    @pytest.mark.parametrize("case", [
        pytest.param(UpdateCommentByRoleTestCase(role="user_bob", payload=UpdateCommentBodyQuery(content="a")),
                     id="Update comment - Valid minimal content boundary"),
        pytest.param(UpdateCommentByRoleTestCase(role="user_bob", payload=UpdateCommentBodyQuery(content="A" * 1000)),
                     id="Update comment - Valid maximum content boundary"),
    ])
    def test_update_comment(self, build_comment_remove, case):
        comments_service = self.get_actor(case.role).comments_api
        prepared_comment_id = build_comment_remove(case.role)
        comment = comments_service.update_comment(comment_id=prepared_comment_id, payload=case.payload)
        assert comment.content == case.payload.content, f"Updated comment doesn't contain expected content.\nER: {case.payload.content}\nAR: {comment.content}"


    @allure.suite("Update existed comment")
    @allure.story("User can update existed comment")
    @allure.description("User can update existed comment, incorrect - negative payload")
    @pytest.mark.parametrize("case", [
        pytest.param(UpdateCommentByRoleTestCase(role="user_eve", payload=UpdateCommentBodyQuery(content="")),
                     id="Update comment - content below minimum boundary"),
        pytest.param(UpdateCommentByRoleTestCase(role="user_eve", payload=UpdateCommentBodyQuery(content="A" * 1001)),
                     id="Create comment - content above maximum boundary"),
        pytest.param(UpdateCommentByRoleTestCase(role="user_eve", payload=UpdateCommentBodyQuery()),
                     id="Create comment - content above maximum boundary"),
    ])
    def test_update_comment_invalid_payload_data(self,build_comment_remove, case):
        comments_service = self.get_actor(case.role).comments_api
        prepared_comment_id = build_comment_remove(case.role)
        comments_service.update_comment(comment_id=prepared_comment_id,
                                         payload=case.payload,
                                         status_code=422,
                                         expected_success=False)

    @allure.suite("Update existed comment")
    @allure.story("User can update existed comment")
    @allure.description("Attempt to edit comment - Invalid comment uuid")
    @pytest.mark.parametrize("case", [
        pytest.param(UpdateCommentByRoleTestCase(role="user_eve", payload=UpdateCommentBodyQuery(content="A")),
                     id="Attempt to edit comment with invalid uuid"),
                             ])
    def test_update_comment_invalid_uuid(self, case):
        comments_service = self.get_actor(case.role).comments_api
        prepared_comment_id = self.data_helper.get_invalid_uuid()
        comments_service.update_comment(comment_id=prepared_comment_id,
                                         payload=case.payload,
                                         status_code=422,
                                         expected_success=False)

    @allure.suite("Update existed comment")
    @allure.story("User can update existed comment")
    @allure.description("User can update existed comment - Comment is deleted")
    @pytest.mark.parametrize("case", [
        pytest.param(UpdateCommentByRoleTestCase(role="user_eve", payload=UpdateCommentBodyQuery(content="A")),
                     id="Attempt to edit removed comment"),
                             ])
    def test_update_comment_removed(self, case, get_removed_comment):
        comments_service = self.get_actor(case.role).comments_api
        prepared_comment_id = get_removed_comment(case.role)
        comments_service.update_comment(comment_id=prepared_comment_id,
                                         payload=case.payload,
                                         status_code=404,
                                         expected_success=False)

    @allure.suite("Update existed comment")
    @allure.story("User can update existed comment")
    @allure.description("Attempt tp edit comment created by another user")
    @pytest.mark.parametrize("comment_creator, case", [
        pytest.param("user_bob", UpdateCommentByRoleTestCase(role="user_eve", payload=UpdateCommentBodyQuery(content="A")),
                     id="Attempt to edit comment created by another user"),
                             ])
    def test_update_comment_created_by_another(self, comment_creator, case, build_comment_remove):
        prepared_comment_id = build_comment_remove(comment_creator)
        comments_service = self.get_actor(case.role).comments_api
        comments_service.update_comment(comment_id=prepared_comment_id,
                                         payload=case.payload,
                                         status_code=403,
                                         expected_success=False)

    @allure.suite("Update existed comment")
    @allure.story("User can update existed comment")
    @allure.description("User can update existed comment - not existed")
    @pytest.mark.parametrize("case", [
        pytest.param(UpdateCommentByRoleTestCase(role="user_eve", payload=UpdateCommentBodyQuery(content="A")),
                     id="Attempt to edit comment that doesn't exist"),
                             ])
    def test_update_comment_not_existed(self, case):
        comments_service = self.get_actor(case.role).comments_api
        prepared_comment_id = self.data_helper.get_not_existed_uuid()
        comments_service.update_comment(comment_id=prepared_comment_id,
                                         payload=case.payload,
                                         status_code=404,
                                         expected_success=False)

    @allure.suite("Delete existed comment")
    @allure.story("User can remove existed comment")
    @allure.description("User can remove published comment - success")
    @pytest.mark.parametrize("case_user", [pytest.param("user_eve",id="Attempt to remove comment by creator")])
    def test_remove_comment(self, case_user, create_and_get_comment):
        comments_service = self.get_actor(case_user).comments_api
        prepared_comment_id = create_and_get_comment(case_user)
        comments_service.delete_comment(comment_id=prepared_comment_id)


    @allure.suite("Delete existed comment")
    @allure.story("User can remove existed comment")
    @allure.description("Attempt to remove the comment created by another user with higher role")
    @pytest.mark.parametrize("comment_creator, case_user", [
        pytest.param("user_eve", "admin",id="Remove comment of another user as admin"),
        pytest.param("user_bob", "moderator",id="Remove comment of another user as moderator"),
                             ])
    def test_remove_comment_depends_on_role(self, create_and_get_comment,case_user, comment_creator):
        prepared_comment_id = create_and_get_comment(comment_creator)
        comments_service = self.get_actor(case_user).comments_api
        comments_service.delete_comment(comment_id=prepared_comment_id)


    @allure.suite("Delete existed comment")
    @allure.story("User can remove existed comment")
    @allure.description("As user try to remove the comment, created by another user")
    @pytest.mark.parametrize("comment_creator, case_user", [
        pytest.param("user_eve", "user_bob",id="Remove comment of another user as user"),
                             ])
    def test_remove_comment_by_role_incorrect(self, create_and_get_comment,case_user, comment_creator):
        prepared_comment_id = create_and_get_comment(comment_creator)
        comments_service = self.get_actor(case_user).comments_api
        comments_service.delete_comment(comment_id=prepared_comment_id,
                                         expected_success=False,
                                         status_code=403)


    @allure.suite("Get replies list")
    @allure.story("User can read existed replies to comment")
    @allure.description("Get replies list")
    @pytest.mark.parametrize("case", [
        pytest.param(GetRepliesByRoleTestCase(role="user_eve",params=GetRepliesQueryParams(page=1, per_page=1)),
            id="Valid minimal pagination boundaries"),
        pytest.param(GetRepliesByRoleTestCase(role="user_eve",params=GetRepliesQueryParams(page=2, per_page=100)),
            id="Valid maximum per_page boundary"),
        pytest.param(GetRepliesByRoleTestCase(role="admin",params=GetRepliesQueryParams()),
            id="Valid request with omitted optional params"),
        ])
    def test_get_replies(self, db_comment_with_replies, case):
        prepared_comment_id = db_comment_with_replies
        comments_service = self.get_actor(case.role).comments_api
        comments_service.get_list_replies(comment_id=prepared_comment_id, params=case.params)

    @allure.suite("Get replies list")
    @allure.story("User can read existed replies to comment")
    @allure.description("Get replies list, incorrect - invalid query param")
    @pytest.mark.parametrize("case", [
        pytest.param(GetRepliesByRoleTestCase(role="user_eve",params=GetRepliesQueryParams(page=0, per_page=10)),
            id="Get replies - page below minimum boundary"),
        pytest.param(GetRepliesByRoleTestCase(role="user_eve",params=GetRepliesQueryParams(page=1, per_page=0)),
            id="Get replies - per_page below minimum boundary"),
        pytest.param(GetRepliesByRoleTestCase(role="admin",params=GetRepliesQueryParams(page=3, per_page=101)),
            id="Get replies - per_page above maximum boundary"),
        ])
    def test_get_replies_incorrect_invalid_payload(self,db_comment_with_replies, case):
        prepared_comment_id = db_comment_with_replies
        comments_service = self.get_actor(case.role).comments_api
        comments_service.get_list_replies(comment_id=prepared_comment_id,
                                           params=case.params,
                                           expected_success=False,
                                           status_code=422)



    @allure.suite("Get replies list")
    @allure.story("User can read existed replies to comment")
    @allure.description("Get replies list, incorrect - Invalid comment uuid")
    def test_get_replies_invalid_comment_uuid(self):
        comments_service = self.get_actor("user_eve").comments_api
        prepared_comment_id = self.data_helper.get_invalid_uuid()
        comments_service.get_list_replies(comment_id=prepared_comment_id,
                                           expected_success=False,
                                           status_code=422)



    @allure.suite("Get replies list")
    @allure.story("User can read existed replies to comment")
    @allure.description("Get replies list - Comment is deleted")
    def test_get_replies_removed_comment(self, get_removed_comment):
        comments_service = self.get_actor("user_bob").comments_api
        prepared_comment_id = get_removed_comment("user_bob")
        comments_service.get_list_replies(comment_id=prepared_comment_id,
                                           expected_success=True,
                                           status_code=200)



    @allure.suite("Get replies list")
    @allure.story("User can read existed replies to comment")
    @allure.description("Get replies list, incorrect - Non-existing comment id")
    def test_get_replies_not_existed_comment(self):
        comments_service = self.get_actor("user_eve").comments_api
        prepared_comment_id = self.data_helper.get_not_existed_uuid()
        comments_service.get_list_replies(comment_id=prepared_comment_id,
                                           expected_success=False,
                                           status_code=404)



    @allure.suite("Create reply to comment")
    @allure.story("User can create a reply to existed comment")
    @allure.description("Create reply to comment")
    @pytest.mark.parametrize("case", [
        pytest.param(CreateCommentByRoleTestCase(role="user_eve", payload=CreateCommentBodyQuery(content="A")),
                     id="Valid minimal content boundary"),
        pytest.param(CreateCommentByRoleTestCase(role="user_bob", payload=CreateCommentBodyQuery(content="A"*1000)),
                     id="Valid maximum content boundary"),
    ])
    def test_create_reply(self, create_and_get_comment, case, comment_cleaner):
        comments_service = self.get_actor(case.role).comments_api
        prepared_comment_id = create_and_get_comment(case.role)
        reply = comments_service.create_reply(comment_id=prepared_comment_id, payload=case.payload)
        comment_cleaner(prepared_comment_id, role=case.role)
        comment_cleaner(reply.id, role=case.role)
        assert reply.post_id != reply.parent_comment_id and prepared_comment_id == reply.parent_comment_id




    @allure.suite("Create reply to comment")
    @allure.story("User can create a reply to existed comment")
    @allure.description("Create reply to comment, incorrect - Comment is removed")
    def test_create_reply_incorrect_removed(self, get_removed_comment):
        prepared_comment_id = get_removed_comment("user_bob")
        comments_service = self.get_actor("user_bob").comments_api
        comments_service.create_reply(comment_id=prepared_comment_id,
                                       payload=CreateCommentBodyQuery(content="Edited"),
                                       expected_success=False,
                                       status_code=404)


    @allure.suite("Create reply to comment")
    @allure.story("User can create a reply to existed comment")
    @allure.description("Create reply to comment, incorrect - Comment does not exist")
    def test_create_reply_incorrect_not_existed(self):
        user = self.get_actor("user_bob")
        prepared_comment_id = self.data_helper.get_not_existed_uuid()
        user.comments_api.create_reply(comment_id=prepared_comment_id,
                                       payload=CreateCommentBodyQuery(content="Edited"),
                                       expected_success=False,
                                       status_code=404)