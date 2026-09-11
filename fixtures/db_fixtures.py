import allure
from faker import Faker

fake = Faker()
import pytest

from auth.credentials import Credentials
from config.db_config import MyLocalDBConfig
from utils.db_helper import DataBaseHandler

creds = Credentials()


@allure.title("DB Fixture: Create/close connection to DB")
@pytest.fixture(name="db_connect", scope="session")
def connect_database():
    data_base = DataBaseHandler(MyLocalDBConfig)

    data_base.connect()

    # connection = sqlite3.connect("pytest_allure/test.db")
    print("DB connected")
    yield data_base
    data_base.close_connection()
    print("DB disconnected")


@pytest.fixture()
@allure.title("DB Fixture: remove conversation using conversation id")
def db_cleanup_conversation(db_connect):
    """
    DB Fixture to remove conversation using provided conversation_id
    :param db_connect: db connection from fixture
    :return:
    """

    def _cleanup(conversation_id):
        db_connect.delete_conversation(conversation_id)
        count = db_connect.check_conversation_by_id(conversation_id)
        assert count == 0
        print(f"cleanup_conversation: {conversation_id}")

    return _cleanup


@pytest.fixture()
@allure.title("DB Fixture: remove conversation using provided participants aliases")
def db_cleanup_conversation_by_aliases(db_connect):
    """
    DB Fixture to remove conversation using provided participants aliases
    :param db_connect: db connection from fixture
    :return:
    """

    def _cleanup_conversation(user_alias1: str, user_alias2: str):
        conversation_id = db_connect.get_conversation_id_between_users(user_alias1, user_alias2)
        if conversation_id is not None:
            db_connect.delete_conversation(conversation_id)

    return _cleanup_conversation


@pytest.fixture()
@allure.title("DB Fixture: get conversation using provided participants aliases")
def db_get_conversation(db_connect):
    """
    DB Fixture to get conversation using provided participants aliases
    :param db_connect: db connection from fixture
    :return:
    """

    def _get_conversation(user_alias1: str, user_alias2: str):
        conversation_id = db_connect.get_conversation_id_between_users(user_alias1, user_alias2)
        if conversation_id is not None:
            return conversation_id
        return None# raise BaseException(f"Conversation is absent")

    yield _get_conversation


@pytest.fixture()
@allure.title("DB Fixture: get rand conversation of the user by provided alias")
def db_get_rand_user_conversation(db_connect):
    """
    DB Fixture to get rand conversation of the user by provided alias
    :param db_connect: db connection from fixture
    :return:
    """

    def _get_user_conversation(user_alias: str):
        conversation_id = db_connect.get_existed_conversation_of_user(user_alias)
        if conversation_id is not None:
            return conversation_id

    yield _get_user_conversation


@allure.title("DB Fixture: get username by provided alias")
@pytest.fixture()
def db_get_username(db_connect):
    """
    DB fixture to get username by provided alias
    :param db_connect:
    :return: username (str)
    """

    def _get(alias: str) -> str:
        return db_connect.get_user_by_name(alias)

    yield _get


@allure.title("DB Fixture: mark conversation as unread")
@pytest.fixture()
def db_mark_conversation_unread(db_connect):
    """
    DB Fixture to mark conversation as unread
    :param db_connect: db connection to perform request to DB
    :return:
    """

    def _mark(conversation_id: str, role: str):
        user_id = creds.get_user(role).user_id
        db_connect.make_conversation_unread(user_id, conversation_id)

    yield _mark


@pytest.fixture()
@allure.title("DB Fixture: mark conversation as read")
def db_mark_conversation_read(db_connect):
    """
    Fixture to mark conversation as read
    :param db_connect: db connection to perform request to DB
    :return:
    """

    def _mark(conversation_id: str, role: str):
        user_id = creds.get_user(role).user_id
        db_connect.make_conversation_read(user_id, conversation_id)

    yield _mark

@pytest.fixture()
@allure.title("DB Fixture: get_comments_with_replies")
def db_get_comment_with_replies(db_connect):
    """
    DB Fixture get comment with replies
    :param db_connect: db connection to perform request to DB
    :return:
    """

    def _get_comments():
        comment = db_connect.get_comments_with_replies()
        return comment
    yield _get_comments
