import sqlite3
from faker import Faker
fake = Faker()
import pytest

from auth.credentials import Credentials
from config.db_config import MyLocalDBConfig
from utils.db_helper import DataBaseHandler
creds = Credentials()

@pytest.fixture(name="db_connect", scope="session")
def connect_database():
    data_base = DataBaseHandler(MyLocalDBConfig)

    data_base.connect()

    # connection = sqlite3.connect("pytest_allure/test.db")
    print("БД подключена")
    yield data_base
    data_base.close_connection()
    print("БД отключена")

    # connection.close()



@pytest.fixture()
def db_cleanup_conversation(db_connect):

    def _cleanup(conversation_id):
        # conversation_id = db_connect.get_conversation_id_between_users(user_a,user_b)
        db_connect.delete_conversation(conversation_id)
        count = db_connect.check_conversation_by_id(conversation_id)
        assert count == 0
        print(f"cleanup_conversation: {conversation_id}")
    return _cleanup

@pytest.fixture()
def db_cleanup_conversation_by_aliases(db_connect):
    def _cleanup_conversation(user_alias1:str, user_alias2:str):
        conversation_id = db_connect.get_conversation_id_between_users(user_alias1, user_alias2)
        if conversation_id is not None:
            db_connect.delete_conversation(conversation_id)
            print(f"Conversation is removed: {conversation_id}")
        else:
            print(f"Conversation is absent. Continue...")
    return _cleanup_conversation

@pytest.fixture()
def db_get_conversation(db_connect):
    def _get_conversation(user_alias1: str, user_alias2: str):
        conversation_id = db_connect.get_conversation_id_between_users(user_alias1, user_alias2)
        if conversation_id is not None:
            print(f"Conversation is found: {conversation_id}")
            return conversation_id
    yield _get_conversation

@pytest.fixture()
def db_get_rand_user_conversation(db_connect):
    def _get_user_conversation(user_alias:str):
        conversation_id = db_connect.get_existed_conversation_of_user(user_alias)
        if conversation_id is not None:
            print(f"Conversation is found: {conversation_id}")
            return conversation_id
        raise BaseException(f"Conversation is absent")
    yield _get_user_conversation

@pytest.fixture()
def db_get_user_name_by_alias(request, db_connect):
    case_info = request.param
    username = db_connect.get_user_by_name(case_info["alias"])
    if username is not None:
        yield username

@pytest.fixture()
def db_get_username(db_connect):
    def _get(alias: str) -> str:
        return db_connect.get_user_by_name(alias)
    yield _get




@pytest.fixture(name="reset_role_after")
def set_users_role_back(db_connect, request):
    yield
    change_role_data = request.param
    db_connect.set_role(table="users", user_name=change_role_data[0], role=change_role_data[1])

@pytest.fixture(name="mark_unread_all")
def mark_all_notifications_as_unred(db_connect, request):
    mark_unread = request.param
    db_connect.mark_all_notifications_unread(for_user=mark_unread)
    yield


@pytest.fixture()
def db_mark_conversation_unread(db_connect):
    """
    Fixture to mark conversation as unread
    :param db_connect: db connection to perform request to DB
    :return:
    """
    def _mark(conversation_id:str, role):
        user_id = creds.get_user(role).user_id
        db_connect.make_conversation_unread(user_id, conversation_id)
    yield _mark

@pytest.fixture()
def db_mark_conversation_read(db_connect):
    """
    Fixture to mark conversation as read
    :param db_connect: db connection to perform request to DB
    :return:
    """
    def _mark(conversation_id:str, role):
        user_id = creds.get_user(role).user_id
        db_connect.make_conversation_read(user_id, conversation_id)
    yield _mark
