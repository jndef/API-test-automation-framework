import allure
import pytest

from config.base_test import BaseTest
from services.messages.params import GetConversationsListParamsByRoleTestCase, GetConversationsListParams, \
    GetConversationMessagesListParams
from services.messages.payloads import CreateConversationPayload, CreateConversationByRoleTestCase, \
    CreateMessagePayload, CreateMessageByRoleTestCase


@allure.epic("Messages Service")
@allure.feature("Messages")
@allure.parent_suite("Tests Messages service API")
@allure.title("Tests Messages service API")
@pytest.mark.messages
class TestMessages(BaseTest):

    @allure.suite("Get conversations list")
    @allure.story("User can see existed conversations")
    @allure.description("Get conversations list")
    @pytest.mark.parametrize("test_case", [
        pytest.param(GetConversationsListParamsByRoleTestCase(role="user_bob",
                                                              params=GetConversationsListParams(page=1, per_page=1)),
                     id="valid minimum boundaries"),
        pytest.param(GetConversationsListParamsByRoleTestCase(role="user_eve",
                                                              params=GetConversationsListParams(page=2, per_page=100)),
                     id=" per_page - valid maximum boundary"),
        pytest.param(GetConversationsListParamsByRoleTestCase(role="user_bob",
                                                              params=GetConversationsListParams()),
                     id="empty query param"),
    ])
    def test_get_conversation_list(self, test_case):
        messages_service = self.get_actor(test_case.role).messages_api
        messages_service.get_conversations_list(params=test_case.params)

    @allure.suite("Get conversations list")
    @allure.story("User can see existed conversations")
    @allure.description("Get conversations list - incorrect query params")
    @pytest.mark.parametrize("test_case", [
        pytest.param(GetConversationsListParamsByRoleTestCase(role="user_bob",
                                                              params=GetConversationsListParams(page=0, per_page=10)),
                     id="Invalid page below minimum boundary"),
        pytest.param(GetConversationsListParamsByRoleTestCase(role="user_eve",
                                                              params=GetConversationsListParams(page=1, per_page=0)),
                     id="Invalid per_page below minimum boundary"),
        pytest.param(GetConversationsListParamsByRoleTestCase(role="user_bob",
                                                              params=GetConversationsListParams(page=3, per_page=101)),
                     id="Invalid per_page above maximum boundary"),
    ])
    def test_get_conversation_list_incorrect_params(self, test_case):
        messages_service = self.get_actor(test_case.role).messages_api
        messages_service.get_conversations_list(params=test_case.params,
                                                expected_success=False,
                                                status_code=422)

    @allure.suite("Create conversation")
    @allure.story("User can create conversation")
    @allure.description("Create conversation")
    @pytest.mark.parametrize("test_case", [
        pytest.param(CreateConversationByRoleTestCase(role="user_eve", payload=CreateConversationPayload(),
                                                      participant_role="user_bob"),
                     id="Create default conversation between users"),
        pytest.param(
            CreateConversationByRoleTestCase(role="user_eve", payload=CreateConversationPayload(name="A" * 100),
                                             participant_role="user_bob"),
            id="Max allowed conversation name"),
    ])
    def test_create_conversation(self, test_case, db_cleanup_conversation_by_aliases):
        messages_service = self.get_actor(test_case.role).messages_api

        db_cleanup_conversation_by_aliases(test_case.role, test_case.participant_role)

        conversation_participants: list[str] = []
        test_case_user_id = self.get_user_info(test_case.role).user_id
        participant_user_id = self.get_user_info(test_case.participant_role).user_id
        conversation_participants.append(participant_user_id)
        conversation_participants.append(test_case_user_id)

        conversation = messages_service.create_conversation(
            CreateConversationPayload(participant_ids=conversation_participants, name=test_case.payload.name))

        # cros check
        messages_service.get_conversation(conversation.id)
        assert conversation.participants[0].id == participant_user_id
        assert conversation.name == test_case.payload.name

    @allure.suite("Create conversation")
    @allure.story("User can create conversation")
    @allure.description("Create conversation - invalid participant id, not existed user")
    @pytest.mark.flaky(reruns=2, reruns_delay=1)
    @pytest.mark.parametrize("test_case", [
        pytest.param(CreateConversationByRoleTestCase(role="user_eve", payload=CreateConversationPayload()),
                     id="Attempt to create conversation with not existed user"),
    ])
    def test_create_conversation_not_existed_user(self, test_case):
        messages_service = self.get_actor(test_case.role).messages_api

        conversation_participants: list[str] = []
        test_case_user_id = self.get_user_info(test_case.role).user_id
        participant_user_id = self.data_helper.get_not_existed_uuid()
        conversation_participants.append(participant_user_id)
        conversation_participants.append(test_case_user_id)

        messages_service.create_conversation(
            CreateConversationPayload(participant_ids=conversation_participants, name=test_case.payload.name),
            expected_success=False, status_code=404)

    @allure.suite("Create conversation")
    @allure.story("User can create conversation")
    @allure.description("Create conversation - invalid participant id, invalid uuid")
    @pytest.mark.parametrize("test_case", [
        pytest.param(CreateConversationByRoleTestCase(role="user_eve", payload=CreateConversationPayload()),
                     id="Attempt to create conversation with with not existed use"),
    ])
    def test_create_conversation_incorrect(self, test_case):
        messages_service = self.get_actor(test_case.role).messages_api

        conversation_participants: list[str] = []
        test_case_user_id = self.get_user_info(test_case.role).user_id
        prepared_participant_id = self.data_helper.get_invalid_uuid()
        conversation_participants.append(prepared_participant_id)
        conversation_participants.append(test_case_user_id)

        messages_service.create_conversation(
            CreateConversationPayload(participant_ids=conversation_participants, name=test_case.payload.name),
            expected_success=False, status_code=422)

    @allure.suite("Create conversation")
    @allure.story("User can create conversation")
    @allure.description("Create conversation - too long conversation name")
    @pytest.mark.parametrize("test_case", [
        pytest.param(
            CreateConversationByRoleTestCase(role="user_eve", payload=CreateConversationPayload(name="A" * 101),
                                             participant_role="user_bob"),
            id="Attempt to create conversation with too long name"),

    ])
    def test_create_conversation_name_too_long(self, test_case):
        messages_service = self.get_actor(test_case.role).messages_api

        conversation_participants: list[str] = []
        test_case_user_id = self.get_user_info(test_case.role).user_id
        prepared_participant_id = test_case.participant_role
        conversation_participants.append(prepared_participant_id)
        conversation_participants.append(test_case_user_id)

        messages_service.create_conversation(
            CreateConversationPayload(participant_ids=conversation_participants, name=test_case.payload.name),
            expected_success=False, status_code=422)

    @allure.suite("Find and create conversation")
    @allure.story("User can find or create new conversation if it wasn't existed")
    @allure.description("Find and create conversation")
    @pytest.mark.parametrize("test_case_role, test_case_participant_role", [
        pytest.param("user_eve", "user_bob", id="Find or created new conversation")
    ])
    def test_find_or_create_conversation(self, test_case_role, db_get_username, test_case_participant_role,
                                         db_cleanup_conversation_by_aliases):
        messages_service = self.get_actor(test_case_role).messages_api
        participant_name = db_get_username(test_case_participant_role)
        db_cleanup_conversation_by_aliases(test_case_role, test_case_participant_role)

        conversation = messages_service.find_or_create_dm(participant_name)
        assert conversation.participants[1].username == participant_name

    @allure.suite("Find and create conversation")
    @allure.story("User can find or create new conversation if it wasn't existed")
    @allure.description("Find and create conversation - user_name doesn't exist")
    @pytest.mark.parametrize("test_case_role", [
        pytest.param(f"user_eve", id="Attempt to find/create conversation when username doesn't exist"),
    ])
    def test_find_or_create_conversation(self, test_case_role):
        messages_service = self.get_actor(test_case_role).messages_api
        participant_name = self.data_helper.get_random_username()

        messages_service.find_or_create_dm(participant_name, status_code=404, expected_success=False)

    @allure.suite("Find and create conversation")
    @allure.story("User can find or create new conversation if it wasn't existed")
    @allure.description("Find and create conversation - user_name is not valid")
    @pytest.mark.parametrize("test_case_role, invalid_user_name", [
        pytest.param(f"user_eve", " ", id="Attempt to find/create conversation when username empty spaces"),
        pytest.param(f"user_eve", None, id="Attempt to find/create conversation when username None"),
    ])
    def test_find_or_create_conversation(self, test_case_role, invalid_user_name):
        messages_service = self.get_actor(test_case_role).messages_api
        participant_name = invalid_user_name
        messages_service.find_or_create_dm(participant_name, status_code=404, expected_success=False)

    @allure.suite("Get existed conversation")
    @allure.story("User can get info about existing conversation")
    @allure.description("Get existed conversation")
    @pytest.mark.parametrize("test_case_role, test_case_participant_role", [
        pytest.param("user_eve", "user_bob", id="Get conversation between users")
    ])
    def test_get_conversation_by_id(self, test_case_role, test_case_participant_role, build_conversation,
                                    db_cleanup_conversation):
        # precondition - create new conversation
        conversation = build_conversation(role=test_case_role, participant_role=test_case_participant_role)
        messages_service = self.get_actor(test_case_role).messages_api
        messages_service.get_conversation(conversation)

        # post_condition - clear conversation
        db_cleanup_conversation(conversation)

    @allure.suite("Get existed conversation")
    @allure.story("User can get info about existing conversation")
    @allure.description("Get existed conversation - not existed conversation")
    @pytest.mark.parametrize("test_case_role, test_case_participant_role", [
        pytest.param("user_eve", "user_bob", id="Get not existed conversation")
    ])
    def test_get_conversation_by_id_not_existed(self, test_case_role, test_case_participant_role):
        conversation = self.data_helper.get_not_existed_uuid()
        messages_service = self.get_actor(test_case_role).messages_api
        messages_service.get_conversation(conversation, expected_success=False, status_code=404)

    @allure.suite("Get existed conversation")
    @allure.story("User can get info about existing conversation")
    @allure.description("Get existed conversation - not valid conversation uuid")
    @pytest.mark.parametrize("test_case_role, test_case_participant_role", [
        pytest.param("user_eve", "user_bob", id="Get conversation by invalid uuid")
    ])
    def test_get_conversation_by_id_not_valid_uuid(self, test_case_role, test_case_participant_role):
        conversation = self.data_helper.get_invalid_uuid()
        messages_service = self.get_actor(test_case_role).messages_api
        messages_service.get_conversation(conversation, expected_success=False, status_code=422)

    @allure.suite("Get existed conversation")
    @allure.story("User can get info about existing conversation")
    @allure.description("Get existed conversation - user isn't participant of it")
    @pytest.mark.parametrize("test_case_role, test_case_participant1_role, test_case_participant2_role ", [
        pytest.param("user_eve", "admin", "user_bob", id="Get conversation when user isn't participant")
    ])
    def test_get_conversation_by_id_not_participant(self, test_case_role, test_case_participant1_role,
                                                    test_case_participant2_role, db_get_conversation):
        conversation = db_get_conversation(test_case_participant1_role, test_case_participant2_role)
        messages_service = self.get_actor(test_case_role).messages_api
        messages_service.get_conversation(conversation, expected_success=False, status_code=403)

    @allure.suite("Get list messages")
    @allure.story("As a user i can see messages of a conversation")
    @allure.description("Get list messages")
    @pytest.mark.parametrize("test_case_participant1_role, test_case_participant2_role ", [
        pytest.param("user_bob", "admin", id="Get conversation messages"),
        pytest.param("admin", "user_bob", id="Get conversation messages")
    ])
    def test_get_messages(self, test_case_participant1_role, test_case_participant2_role, db_get_conversation):
        conversation = db_get_conversation(test_case_participant1_role, test_case_participant2_role)
        messages_service = self.get_actor(test_case_participant1_role).messages_api
        messages_service.get_conversation_messages(conversation,
                                                   params=GetConversationMessagesListParams(page=1, per_page=10))

    @allure.suite("Get list messages")
    @allure.story("As a user i can see messages of a conversation")
    @allure.description("Get list messages - not existed conversation")
    @pytest.mark.parametrize("test_case_participant1_role", [
        pytest.param("user_bob", id="Get messages of unexisted conversation"),
    ])
    def test_get_messages_not_existed(self, test_case_participant1_role):
        conversation = self.data_helper.get_not_existed_uuid()
        messages_service = self.get_actor(test_case_participant1_role).messages_api
        messages_service.get_conversation_messages(conversation, expected_success=False, status_code=404)

    @allure.suite("Get list messages")
    @allure.story("As a user i can see messages of a conversation")
    @allure.description("Get list messages - not existed conversation")
    @pytest.mark.parametrize("test_case_participant1_role", [
        pytest.param("user_bob", id="Get messages of unexisted conversation"),
    ])
    def test_get_messages_invalid_uuid(self, test_case_participant1_role):
        conversation = self.data_helper.get_invalid_uuid()
        messages_service = self.get_actor(test_case_participant1_role).messages_api
        messages_service.get_conversation_messages(conversation, expected_success=False, status_code=422)

    @allure.suite("Get list messages")
    @allure.story("As a user i can see messages of a conversation")
    @allure.description("Get list messages - user isn't participant")
    @pytest.mark.parametrize("test_case_role, test_case_participant1_role, test_case_participant2_role ", [
        pytest.param("user_eve", "admin", "user_bob", id="Get messages when user isn't participant")
    ])
    def test_get_messages_not_participant(self, test_case_role, test_case_participant1_role,
                                          test_case_participant2_role, db_get_conversation):
        conversation = db_get_conversation(test_case_participant1_role, test_case_participant2_role)
        messages_service = self.get_actor(test_case_role).messages_api
        messages_service.get_conversation_messages(conversation, expected_success=False, status_code=403)

    @allure.suite("Create message")
    @allure.story("As a user i can create message")
    @allure.description("Create message")
    @pytest.mark.parametrize("case", [
        pytest.param(CreateMessageByRoleTestCase(role="user_eve", participant_role="user_bob",
                                                 payload=CreateMessagePayload(content="M")),
                     id="Create a new message - min allowed content"),
        pytest.param(CreateMessageByRoleTestCase(role="user_eve", participant_role="user_bob",
                                                 payload=CreateMessagePayload(content="M" * 2000)),
                     id="Create a new message - max allowed content"),
        pytest.param(CreateMessageByRoleTestCase(role="user_eve", participant_role="user_bob",
                                                 payload=CreateMessagePayload(content="Message",
                                                                              image_url="image.jpg")),
                     id="Create a new message - with image"),
        pytest.param(CreateMessageByRoleTestCase(role="user_eve", participant_role="user_bob",
                                                 payload=CreateMessagePayload(content="Message", image_url=None)),
                     id="Create a new message - with image as None")
    ])
    def test_create_message(self, case, build_conversation, message_cleaner):
        conversation = build_conversation(case.role, case.participant_role)
        api_services = self.get_actor(case.role)
        payload = case.payload
        if payload.image_url:
            upload_service = api_services.upload_api
            image_url = upload_service.upload_image(payload.image_url)
            payload.image_url = image_url.url
        messages_service = api_services.messages_api
        message = messages_service.send_message(conversation_id=conversation, payload=payload)
        assert message.content == payload.content, "Content of created message is different from expected"
        assert message.conversation_id == conversation, "Conversation_id of created message is different from expected"
        assert not message.is_deleted, "Message is created as deleted"
        if payload.image_url:
            assert isinstance(message.image_url, str)

        message_cleaner(message.id, case.role)

    @allure.suite("Create message")
    @allure.story("As a user i can create message")
    @allure.description("Create message with invalid data at payload")
    @pytest.mark.parametrize("case", [
        pytest.param(CreateMessageByRoleTestCase(role="user_eve", participant_role="user_bob",
                                                 payload=CreateMessagePayload(content="")),
                     id="Create a new message - min allowed content"),
        pytest.param(CreateMessageByRoleTestCase(role="user_eve", participant_role="user_bob",
                                                 payload=CreateMessagePayload(content="M" * 2001)),
                     id="Create a new message - max allowed content"),
        pytest.param(CreateMessageByRoleTestCase(role="user_eve", participant_role="user_bob",
                                                 payload=CreateMessagePayload(content="Message", image_url="")),
                     id="Create a new message - image url - empty string"),
        pytest.param(CreateMessageByRoleTestCase(role="user_eve", participant_role="user_bob",
                                                 payload=CreateMessagePayload(content="Message", image_url="//")),
                     id="Create a new message - image url - special characters only"),
    ])
    def test_create_message_invalid_payload(self, case, db_get_conversation):
        conversation = db_get_conversation(case.role, case.participant_role)
        messages_service = self.get_actor(case.role).messages_api
        payload = case.payload
        messages_service.send_message(conversation_id=conversation, payload=payload, status_code=422,
                                      expected_success=False)

    @allure.suite("Create message")
    @allure.story("As a user i can create message")
    @allure.description("Create message - user isn't participant of the conversation")
    @pytest.mark.parametrize("test_case_role, test_case_participant1_role, test_case_participant2_role", [
        pytest.param("user_eve", "admin", "user_bob", id="Get messages when user isn't participant")
    ])
    def test_create_message_not_participant(self, test_case_role, test_case_participant1_role,
                                            test_case_participant2_role, db_get_conversation):
        conversation = db_get_conversation(test_case_participant1_role, test_case_participant2_role)
        messages_service = self.get_actor(test_case_role).messages_api
        payload = CreateMessagePayload(content="M")
        messages_service.send_message(conversation_id=conversation, payload=payload, status_code=403,
                                      expected_success=False)

    @allure.suite("Remove message")
    @allure.story("As a user i can remove created message")
    @allure.description("Remove message")
    @pytest.mark.parametrize("case", [
        pytest.param("user_eve", id="Remove message by creator"),
        pytest.param("admin", id="Remove message by creator"),
    ])
    def test_remove_message(self, case, build_message):
        prepared_message_id = build_message(case)
        messages_service = self.get_actor(case).messages_api
        messages_service.remove_message(message_id=prepared_message_id)

    @allure.suite("Remove message")
    @allure.story("As a user i can remove created message")
    @allure.description("Remove message - not existed message")
    @pytest.mark.parametrize("case", [pytest.param("user_eve", id="Remove message - message doesn't exist"),
                                      ])
    def test_remove_message_not_existed(self, case):
        prepared_message_id = self.data_helper.get_not_existed_uuid()
        messages_service = self.get_actor(case).messages_api
        messages_service.remove_message(message_id=prepared_message_id, status_code=404, expected_success=False)

    @allure.suite("Remove message")
    @allure.story("As a user i can remove created message")
    @allure.description("Remove message - not valid message id")
    @pytest.mark.parametrize("case", [pytest.param("user_eve", id="Remove message - message doesn't exist"),
                                      ])
    def test_remove_message_not_existed(self, case):
        prepared_message_id = self.data_helper.get_invalid_uuid()
        messages_service = self.get_actor(case).messages_api
        messages_service.remove_message(message_id=prepared_message_id, status_code=422, expected_success=False)

    @allure.suite("Remove message")
    @allure.story("As a user i can remove created message")
    @allure.description("Remove message - already removed")
    @pytest.mark.parametrize("case", [pytest.param("user_eve", id="Remove message - message doesn't exist"),
                                      ])
    def test_remove_message_already_removed(self, case, get_removed_message):
        prepared_message_id = get_removed_message(case)
        messages_service = self.get_actor(case).messages_api
        messages_service.remove_message(message_id=prepared_message_id)

    @allure.suite("Remove message")
    @allure.story("As a user i can remove created message")
    @allure.description("Remove message - message of participant")
    @pytest.mark.parametrize("case_user, participant_user", [
        pytest.param("user_bob", "admin", id="Remove message - message of participant"),
        pytest.param("admin", "user_bob", id="Remove message by admin - message of participant"),
        pytest.param("moderator", "user_bob", id="Remove message by moderator - message of participant"),
    ])
    def test_remove_message_of_participant(self, case_user, participant_user, build_conversation,
                                           build_message_remove_at_certain_conversation):
        conversation = build_conversation(case_user, participant_user)
        prepared_message_id = build_message_remove_at_certain_conversation(role=participant_user,
                                                                           conversation=conversation)
        messages_service = self.get_actor(case_user).messages_api
        messages_service.remove_message(message_id=prepared_message_id, expected_success=False, status_code=403)

    @allure.suite("Remove message")
    @allure.story("As a user i can remove created message")
    @allure.description("Remove message - created by another user, not participant")
    @pytest.mark.parametrize("case_user, participant_user1, participant_user2", [
        pytest.param("user_bob", "admin", "user_eve", id="Remove message - created by another user, not participant"),
    ])
    def test_remove_message_from_private_chat(self, case_user, participant_user1, participant_user2, build_conversation,
                                              build_message_remove_at_certain_conversation):
        conversation = build_conversation(participant_user1, participant_user2)
        prepared_message_id = build_message_remove_at_certain_conversation(role=participant_user2,
                                                                           conversation=conversation)
        messages_service = self.get_actor(case_user).messages_api
        messages_service.remove_message(message_id=prepared_message_id, expected_success=False, status_code=403)

    @allure.suite("Read conversation")
    @allure.story("As a user i can mark conversation as read")
    @allure.description("Read conversation")
    @pytest.mark.parametrize("case_user, participant_user", [
        pytest.param("user_bob", "admin", id="Read conversation"),
    ])
    def test_read_conversation(self, case_user, participant_user, build_conversation,
                               build_message_at_certain_conversation, db_mark_conversation_unread):
        conversation = build_conversation(case_user, participant_user)
        build_message_at_certain_conversation(role=participant_user, conversation=conversation)
        messages_service = self.get_actor(case_user).messages_api
        conversation_before = messages_service.get_conversation(conversation)
        assert conversation_before.unread_count > 0
        messages_service.read_conversation(conversation)
        conversation_after = messages_service.get_conversation(conversation)
        assert conversation_after.unread_count == 0

        db_mark_conversation_unread(conversation, case_user)

    @allure.suite("Read conversation")
    @allure.story("As a user i can mark conversation as read")
    @allure.description("Read conversation")
    @pytest.mark.parametrize("case_user", [
        pytest.param("user_bob", id="Read conversation - not existed"),
    ])
    def test_read_conversation_not_existed(self, case_user):
        conversation = self.data_helper.get_not_existed_uuid()
        messages_service = self.get_actor(case_user).messages_api
        messages_service.read_conversation(conversation, status_code=404, expected_success=False)

    @allure.suite("Read conversation")
    @allure.story("As a user i can mark conversation as read")
    @allure.description("Read conversation")
    @pytest.mark.parametrize("case_user", [
        pytest.param("user_bob", id="Read conversation - not valid uuid"),
    ])
    def test_read_conversation_not_valid_uuid(self, case_user):
        conversation = self.data_helper.get_invalid_uuid()
        messages_service = self.get_actor(case_user).messages_api
        messages_service.read_conversation(conversation, status_code=422, expected_success=False)

    @allure.suite("Read conversation")
    @allure.story("As a user i can mark conversation as read")
    @allure.description("Read conversation - user isn't participant")
    @pytest.mark.parametrize("case_user, participant_user1, participant_user2", [
        pytest.param("user_bob", "admin", "user_eve", id="Remove message - created by another user, not participant"),
    ])
    def test_read_conversation_not_participant(self, case_user, participant_user1, participant_user2,
                                               build_conversation,
                                               build_message_at_certain_conversation, db_mark_conversation_unread):
        conversation = build_conversation(participant_user1, participant_user2)
        build_message_at_certain_conversation(role=participant_user2, conversation=conversation)
        messages_service = self.get_actor(case_user).messages_api
        messages_service.read_conversation(conversation, expected_success=False, status_code=404)

    @allure.suite("Read conversation")
    @allure.story("As a user i can mark conversation as read")
    @allure.description("Read conversation - already read")
    @pytest.mark.parametrize("participant_user1, participant_user2", [
        pytest.param("user_bob", "admin", id="Read conversation - already read"),
    ])
    def test_read_conversation_already_read(self, participant_user1, participant_user2, build_conversation,
                                            build_message_at_certain_conversation, db_mark_conversation_read):

        conversation = build_conversation(participant_user1, participant_user2)
        build_message_at_certain_conversation(role=participant_user2, conversation=conversation)
        db_mark_conversation_read(conversation_id=conversation, role=participant_user1)

        messages_service = self.get_actor(participant_user1).messages_api
        messages_service.read_conversation(conversation)
