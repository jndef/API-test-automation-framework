import allure
import pytest

from config.base_test import BaseTest
from services.comments.payloads import CreateCommentPayload
from services.likes.payloads import LikePostPayload, LikeCommentPayload
from services.notifications.params import GetNotificationsParamsByRoleTestCase, GetNotificationsParams
from services.posts.payloads import CreatePostPayload, CreateRepostPayload


@allure.epic("Notification Service")
@allure.feature("Notification")
@allure.parent_suite("Notification service API")
@allure.title("Notification service API")
@pytest.mark.notifications
class TestNotification(BaseTest):


    @allure.suite("Notification list")
    @allure.sub_suite("Get user notifications list")

    @allure.title("Get user notifications list with params ({case.params})")
    @pytest.mark.parametrize("case", [
        pytest.param(GetNotificationsParamsByRoleTestCase(role="user_bob",
                                                      params=GetNotificationsParams(page=1, per_page=1)),
                                                      id="per_page, min allowed value"),
        pytest.param(GetNotificationsParamsByRoleTestCase(role="user_eve",
                                                      params=GetNotificationsParams(page=1, per_page=100)),
                                                      id="per_page, max allowed value"),
        pytest.param(GetNotificationsParamsByRoleTestCase(role="user_bob",
                                                      params=GetNotificationsParams(page=2, per_page=10)),
                                                      id="page, 2nd page of results"),
        pytest.param(GetNotificationsParamsByRoleTestCase(role="user_bob",
                                                      params=GetNotificationsParams(page=1, per_page=10, is_read=True)),
                                                      id="is_read, specified True"),
        pytest.param(GetNotificationsParamsByRoleTestCase(role="user_bob",
                                                      params=GetNotificationsParams(page=1, per_page=10, is_read=False)),
                                                      id="is_read, specified False"),
    ])
    def test_get_notification_list(self, case):
        notification_service = self.get_actor(case.role).notifications_api
        response = notification_service.get_notification_list(params=case.params)
        if case.params.is_read:
            assert all(notification.is_read is True for notification in response.items) or len(response.items) == 0
        elif not case.params.is_read is True:
            assert all(notification.is_read is False for notification in response.items) or len(response.items) == 0
        assert response.page == case.params.page, f"Error. Page value at response isn't matched to expected. ER/AR: {case.params.page}/{response.page}"
        assert response.per_page == case.params.per_page, f"Error. per_page value at response isn't matched to expected. ER/AR: {case.params.per_page}/{response.per_page}"


    @allure.suite("Notification creation")
    @allure.sub_suite("Notification creation - like type")

    @allure.title("Receive notification 'like' type (like post)")
    @pytest.mark.parametrize("case_user, support_user", [
        pytest.param("user_bob", "user_eve", id="get notification on post like"),
    ])
    def test_get_post_like_notification(self, case_user, support_user, post_cleaner):
        case_user_api = self.get_actor(case_user)
        support_user_api = self.get_actor(support_user)

        with allure.step(f"Create new post by case user ({case_user})"):
            created_post = case_user_api.posts_api.create_post(payload=CreatePostPayload(content=self.data_helper.generate_text(10)))

        # register post on clean after test
        post_cleaner(created_post.id, case_user)

        with allure.step(f"Add like to post ({created_post.id}) by support user ({support_user})"):
            support_user_api.likes_api.like_post(created_post.id, payload=LikePostPayload(reaction="angry"))

        supporter_user_id = self.get_user_info(support_user).user_id

        with allure.step(f"Check a new notification (post like)"):
            new_notification = case_user_api.notifications_api.get_notification_list().items[0]
            assert new_notification.type == "like", f"Error. Expected target_id isn't equal to actual target_id. ER/AR: like/{new_notification.type}"
            assert new_notification.target_type == "post", f"Error. Expected target_id isn't equal to actual target_id. ER/AR: post/{new_notification.target_type}"
            assert new_notification.target_id == created_post.id, f"Error. Expected target_id isn't equal to actual target_id. ER/AR: {created_post.id}/{new_notification.target_id}"
            assert new_notification.actor.id == supporter_user_id, f"Error. Target notification was created by unexpected user. ER/AR: {supporter_user_id}/{new_notification.actor.id}"    @allure.feature("Notification creation")
            assert new_notification.is_read is False, f"Error. Created notification is read by default"

    @allure.suite("Notification creation")
    @allure.sub_suite("Notification creation - comment type")
    @allure.title("Receive notification 'comment' type (comment to post)")
    @pytest.mark.parametrize("case_user, support_user", [
        pytest.param("user_eve", "user_bob", id="get notification on comment to post"),
    ])
    def test_get_post_comment_notification(self, case_user, support_user, post_cleaner, comment_cleaner):
        case_user_api = self.get_actor(case_user)
        support_user_api = self.get_actor(support_user)

        first_notification_in_list = case_user_api.notifications_api.get_notification_list().items[0].id

        with allure.step(f"Create new post by case user ({case_user})"):
            created_post = case_user_api.posts_api.create_post(payload=CreatePostPayload(content=self.data_helper.generate_text(10)))


        with allure.step(f"Drop comment to post ({created_post.id}) by support user ({support_user})"):
            created_comment = support_user_api.comments_api.create_comment(created_post.id, payload=CreateCommentPayload(content=self.data_helper.generate_text(10)))

        # register post/comment on clean after test
        post_cleaner(created_post.id, case_user)
        comment_cleaner(created_comment.id, support_user)

        supporter_user_id = self.get_user_info(support_user).user_id

        with allure.step(f"Check a new notification (comment to post)"):
            new_notification = case_user_api.notifications_api.get_notification_list().items[0]
            assert first_notification_in_list != new_notification.id, "Error. No new notifications"
            assert new_notification.type == "comment", f"Error. Expected target_id isn't equal to actual target_id. ER/AR: comment / {new_notification.type}"
            assert new_notification.target_type == "post", f"Error. Expected target_id isn't equal to actual target_id. ER/AR: post/{new_notification.target_type}"
            assert new_notification.target_id == created_post.id, f"Error. Expected target_id isn't equal to actual target_id. ER/AR: {created_post.id} / {new_notification.target_id}"
            assert new_notification.actor.id == supporter_user_id, f"Error. Target notification was created by unexpected user. ER/AR: {supporter_user_id} / {new_notification.actor.id}"
            assert new_notification.is_read is False, f"Error. Created notification is read by default"

    @allure.suite("Notification creation")
    @allure.sub_suite("Notification creation - repost type")
    @allure.title("Receive notification 'repost' type (repost post)")

    @pytest.mark.parametrize("case_user, support_user", [
        pytest.param("user_eve", "user_bob", id="get notification on post reposting"),
    ])
    def test_get_repost_post_notification(self, case_user, support_user, post_cleaner):
        case_user_api = self.get_actor(case_user)
        support_user_api = self.get_actor(support_user)

        first_notification_in_list = case_user_api.notifications_api.get_notification_list().items[0].id

        with allure.step(f"Create new post by case user ({case_user})"):
            created_post = case_user_api.posts_api.create_post(
                payload=CreatePostPayload(content=self.data_helper.generate_text(10)))

        with allure.step(f"Add repost of the post ({created_post.id}) by support user ({support_user})"):
            created_repost = support_user_api.posts_api.repost_post(created_post.id, payload=CreateRepostPayload(repost_type="repost", content=self.data_helper.generate_text(10)))

        # register post/comment on clean after test
        post_cleaner(created_post.id, case_user)

        supporter_user_id = self.get_user_info(support_user).user_id

        with allure.step(f"Check a new notification (comment to post)"):
            new_notification = case_user_api.notifications_api.get_notification_list().items[0]
            assert first_notification_in_list != new_notification.id, "Error. No new notifications"
            assert new_notification.type == "repost", f"Error. Expected target_id isn't equal to actual target_id. ER/AR: repost / {new_notification.type}"
            assert new_notification.target_type == "post", f"Error. Expected target_id isn't equal to actual target_id. ER/AR: post/{new_notification.target_type}"
            assert new_notification.target_id == created_post.id, f"Error. Expected target_id isn't equal to actual target_id. ER/AR: {created_post.id} / {new_notification.target_id}"
            assert new_notification.actor.id == supporter_user_id, f"Error. Target notification was created by unexpected user. ER/AR: {supporter_user_id} / {new_notification.actor.id}"
            assert new_notification.is_read is False, f"Error. Created notification is read by default"


    @allure.suite("Notification creation")
    @allure.sub_suite("Notification creation - follow type")
    @allure.title("Receive notification 'follow' type (follow public user)")
    @pytest.mark.parametrize("case_user, support_user", [
        pytest.param("user_eve", "user_bob", id="get notification on new follower"),
    ])
    def test_get_new_follower_notification(self, case_user, support_user, follow_request_cleaner):
        case_user_api = self.get_actor(case_user)
        support_user_api = self.get_actor(support_user)

        first_notification_in_list = case_user_api.notifications_api.get_notification_list().items[0].id



        with allure.step(f"Start follow '{case_user}' by another user ({support_user})"):
            case_user_name = case_user_api.auth_api.get_me().username
            support_user_api.follows_api.follow_user(case_user_name)

        # register unfollowing after test
        follow_request_cleaner(case_user_name, support_user)

        supporter_user_id = self.get_user_info(support_user).user_id

        with allure.step(f"Check a new notification (new follower)"):

            new_notification = case_user_api.notifications_api.get_notification_list().items[0]
            assert first_notification_in_list != new_notification.id, "Error. No new notifications"
            assert new_notification.type == "follow", f"Error. Expected target_id isn't equal to actual target_id. ER/AR: follow/{new_notification.type}"
            assert new_notification.target_type is None, f"Error. Expected target_id isn't equal to actual target_id. ER/AR: None /{new_notification.target_type}"
            assert new_notification.target_id is None, f"Error. Expected target_id isn't equal to actual target_id. ER/AR: None / {new_notification.target_id}"
            assert new_notification.actor.id == supporter_user_id, f"Error. Target notification was created by unexpected user. ER/AR: {supporter_user_id} / {new_notification.actor.id}"
            assert new_notification.is_read is False, f"Error. Created notification is read by default"


    @allure.suite("Notification creation")
    @allure.sub_suite("Notification creation - follow_request type")
    @allure.title("Receive notification 'follow_request' type (follow private user)")
    @pytest.mark.parametrize("case_user, support_user", [
        pytest.param("user_private", "user_bob", id="get notification on new follow request"),
    ])
    def test_get_new_follow_request_notification(self, case_user, support_user, follow_request_cleaner):
        case_user_api = self.get_actor(case_user)
        support_user_api = self.get_actor(support_user)

        first_notification_in_list = case_user_api.notifications_api.get_notification_list().items[0].id



        with allure.step(f"Start follow '{case_user}' by another user ({support_user})"):
            case_user_name = case_user_api.auth_api.get_me().username
            support_user_api.follows_api.follow_user(case_user_name)

        # register unfollowing after test
        follow_request_cleaner(case_user_name, support_user)

        supporter_user_id = self.get_user_info(support_user).user_id

        with allure.step(f"Check a new notification (new follow request)"):
            new_notification = case_user_api.notifications_api.get_notification_list().items[0]
            assert first_notification_in_list != new_notification.id, "Error. No new notifications"
            assert new_notification.type == "follow_request", f"Error. Expected target_id isn't equal to actual target_id. ER/AR: follow/{new_notification.type}"
            assert new_notification.target_type is None, f"Error. Expected target_id isn't equal to actual target_id. ER/AR: None /{new_notification.target_type}"
            assert new_notification.target_id is None, f"Error. Expected target_id isn't equal to actual target_id. ER/AR: None / {new_notification.target_id}"
            assert new_notification.actor.id == supporter_user_id, f"Error. Target notification was created by unexpected user. ER/AR: {supporter_user_id} / {new_notification.actor.id}"
            assert new_notification.is_read is False, f"Error. Created notification is read by default"



    @allure.suite("Read notification")
    @allure.sub_suite("Read notification")
    @allure.title("Read notification")
    @pytest.mark.parametrize("case_user, support_user", [
        pytest.param("user_eve", "user_bob", id="attempt to read notification"),
    ])
    def test_read_notification(self, case_user, support_user, follow_request_cleaner):
        case_user_api = self.get_actor(case_user)
        support_user_api = self.get_actor(support_user)

        first_notification_in_list = case_user_api.notifications_api.get_notification_list().items[0].id



        with allure.step(f"Create new notification follow type"):
            case_user_name = case_user_api.auth_api.get_me().username
            support_user_api.follows_api.follow_user(case_user_name)

        # register unfollowing after test
        follow_request_cleaner(case_user_name, support_user)

        supporter_user_id = self.get_user_info(support_user).user_id

        with allure.step(f"Check a new notification (new follower)"):

            new_notification = case_user_api.notifications_api.get_notification_list().items[0]
            assert first_notification_in_list != new_notification.id, "Error. No new notifications"
            assert new_notification.type == "follow", f"Error. Expected target_id isn't equal to actual target_id. ER/AR: follow/{new_notification.type}"
            assert new_notification.target_type is None, f"Error. Expected target_id isn't equal to actual target_id. ER/AR: None /{new_notification.target_type}"
            assert new_notification.target_id is None, f"Error. Expected target_id isn't equal to actual target_id. ER/AR: None / {new_notification.target_id}"
            assert new_notification.actor.id == supporter_user_id, f"Error. Target notification was created by unexpected user. ER/AR: {supporter_user_id} / {new_notification.actor.id}"
            assert new_notification.is_read is False, f"Error. Created notification is read by default"

        case_user_api.notifications_api.mark_read_notification(new_notification.id)

        with allure.step(f"Check notification after read"):
            read_new_notification = case_user_api.notifications_api.get_notification_list(params=GetNotificationsParams(is_read=True)).items[0]
            assert read_new_notification.is_read, f"Error. Created notification is not read"



    @allure.suite("Read notification")
    @allure.sub_suite("Read notification")

    @allure.title("Read notification - not existed")
    @pytest.mark.parametrize("case_user", [
        pytest.param("user_eve", id="attempt to read unexisted notification"),
    ])
    def test_read_notification_not_existed(self, case_user):
        case_user_api = self.get_actor(case_user)
        prepared_notification_id = self.data_helper.get_not_existed_uuid()
        case_user_api.notifications_api.mark_read_notification(prepared_notification_id, expected_success=False, status_code=404)

    @allure.suite("Read notification")
    @allure.sub_suite("Read notification")
    @allure.title("Read notification - not valid uuid")
    @pytest.mark.parametrize("case_user", [
        pytest.param("user_eve", id="attempt to read unexisted notification"),
    ])
    def test_read_notification_invalid_uuid(self, case_user):
        case_user_api = self.get_actor(case_user)
        prepared_notification_id = self.data_helper.get_invalid_uuid()
        case_user_api.notifications_api.mark_read_notification(prepared_notification_id, expected_success=False, status_code=422)

    @allure.suite("Read notification")
    @allure.sub_suite("Read notification")
    @allure.title("Read notification - already read")
    @pytest.mark.parametrize("case_user, support_user", [
        pytest.param("user_eve", "user_bob", id="attempt to read notification already read"),
    ])
    def test_read_notification_already_read(self,  case_user, support_user, follow_request_cleaner):
        case_user_api = self.get_actor(case_user)
        support_user_api = self.get_actor(support_user)

        with allure.step(f"Create new notification follow type"):
            case_user_name = case_user_api.auth_api.get_me().username
            support_user_api.follows_api.follow_user(case_user_name)

        # register unfollowing after test
        follow_request_cleaner(case_user_name, support_user)

        new_notification = case_user_api.notifications_api.get_notification_list(params=GetNotificationsParams(is_read=False)).items[0].id

        case_user_api.notifications_api.mark_read_notification(new_notification)
        case_user_api.notifications_api.mark_read_notification(notification_id=new_notification)



    @allure.suite("Read notification")
    @allure.sub_suite("Read notification")
    @allure.title("Read notification -  notification of another user")
    @pytest.mark.parametrize("case_user, support_user", [
        pytest.param("user_eve", "user_bob", id="attempt to read notification of another user"),
    ])
    def test_read_notification_of_another_user(self,  case_user, support_user, follow_request_cleaner):
        case_user_api = self.get_actor(case_user)
        support_user_api = self.get_actor(support_user)

        with allure.step(f"Create new notification follow type"):
            case_user_name = case_user_api.auth_api.get_me().username
            support_user_api.follows_api.follow_user(case_user_name)

        # register unfollowing after test
        follow_request_cleaner(case_user_name, support_user)

        new_notification = case_user_api.notifications_api.get_notification_list(params=GetNotificationsParams(is_read=False)).items[0].id

        support_user_api.notifications_api.mark_read_notification(new_notification, expected_success=False, status_code=403)


    @allure.suite("Read all notifications")
    @allure.sub_suite("Read all notifications")
    @allure.title("Read all notifications")
    @pytest.mark.parametrize("case_user, support_user", [
        pytest.param("user_eve","user_bob", id="attempt to read all notifications"),
    ])
    def test_read_all_notification_of_another_user(self,  case_user, support_user, follow_request_cleaner):
        case_user_api = self.get_actor(case_user)
        support_user_api = self.get_actor(support_user)

        with allure.step(f"Create new notification follow type"):
            case_user_name = case_user_api.auth_api.get_me().username
            support_user_api.follows_api.follow_user(case_user_name)

        # register unfollowing after test
        follow_request_cleaner(case_user_name, support_user)

        unread_count_before:int = len(case_user_api.notifications_api.get_notification_list(params=GetNotificationsParams(is_read=False)).items)

        case_user_api.notifications_api.mark_read_all_notifications()

        unread_count_after:int = len(case_user_api.notifications_api.get_notification_list(params=GetNotificationsParams(is_read=False)).items)
        assert unread_count_after == 0, f"Unread count should be 0. Was before {unread_count_before}. Now: {unread_count_after}"
