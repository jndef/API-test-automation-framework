from psycopg2.extras import RealDictCursor

from mysql import connector
import psycopg2
import sqlite3
from mysql.connector.cursor import MySQLCursor

from auth.credentials import Credentials
from services.upload.api import data_helper


class DataBaseHandler:

    def __init__(self, config):
        self.db_name = config.db_name
        self.config = config
        self.connection = None
        self.cursor: MySQLCursor = None
        self.sslmode = None

    def _get_connection_params(self):
        if self.db_name in ['local_db']:
            return {
                'host': self.config.server,
                'database': self.config.database,
                'user': self.config.user,
                'password': self.config.password,
                'port': self.config.port
            }

        else:
            raise ValueError("Поддерживаются только local_db")

    def connect(self):
        params = self._get_connection_params()
        if self.db_name == 'mysql':
            self.connection = connector.connect(**params)
        elif self.db_name in ['postgres', 'local_db']:
            self.connection = psycopg2.connect(**params)
        elif self.db_name == 'sqlite':
            self.connection = sqlite3.connect(params["database"])
        """и также в этом методе можно возвращать connect
            в этом методе тогда создается объект курсора - тот, что запишется в self.cursor
        """
        self.cursor = self.connection.cursor(cursor_factory=RealDictCursor)


    # @staticmethod
    # def _table_name_verification(table_name):
    #     existed_tables = ['users', 'refresh_tokens', 'follows', 'posts', 'hashtags', 'post_hashtags', 'comments',
    #                       'likes', 'bookmarks', 'conversations', 'conversation_participants', 'messages',
    #                       'notifications']
    #     if table_name not in existed_tables:
    #         raise Exception(f"Table {table_name} does not exist")


    def get_user_by_name(self, user_alias: str = None):
        """
        Query to DB to get user by provided name (alias)
        :param user_alias:str - users alias used in framework for user's credentials
        :return: result of DB query
        """
        creds = Credentials()
        user_id: str = creds.get_user(alias=user_alias).user_id
        query = f"""
            SELECT username 
            FROM users
            WHERE id = %s
        """
        self.cursor.execute(query, (user_id,))

        return self.cursor.fetchone()["username"]

    def get_conversation_id_between_users(self, user_alias1: str, user_alias2: str):
        """
        Method to get conversation id between two users
        :param user_alias1: alias of 1st user
        :param user_alias2: alias of 2nd user
        :return:
        """
        creds = Credentials()

        user_id1, user_id2 = creds.get_user(user_alias1).user_id, creds.get_user(user_alias2).user_id
        query = f"""
            SELECT cp.conversation_id 
            FROM conversation_participants cp
            INNER JOIN conversations c ON c.id = cp.conversation_id
            WHERE cp.user_id IN (%s, %s) AND c.is_group is FALSE
            GROUP BY 1
            HAVING COUNT(*) = 2
        """
        self.cursor.execute(
            query, (user_id1, user_id2)
        )
        if self.cursor.rowcount > 0:
            return self.cursor.fetchone()["conversation_id"]
        return None

    def get_unread_conversation_for_user(self, user_alias: str):
        """
        Method to get conversation id between two users
        :param user_alias: alias of the user
        :return:
        """
        creds = Credentials()

        user_id= creds.get_user(user_alias).user_id
        query = f"""
        SELECT conversation_participants.conversation_id 
        FROM conversation_participants
        INNER JOIN conversations 
        ON conversation_participants.conversation_id = conversations.id  
        WHERE conversation_participants.user_id = %s 
        AND conversation_participants.last_read_at is NULL
        AND conversations.is_group is FALSE 
        """
        self.cursor.execute(
            query, (user_id,)
        )
        if self.cursor.rowcount > 0:
            return self.cursor.fetchone()["conversation_id"]
        return None


    def get_existed_conversation_of_user(self, user_alias: str):
        """
        Method, returned conversation id if existed
        :param user_alias: provided user alias used to get user_id
        :return:
        """
        creds = Credentials()
        user_id = creds.get_user(user_alias).user_id

        query = f"""
        SELECT conversation_participants.conversation_id
        FROM conversation_participants
        INNER JOIN conversations
        ON conversation_participants.conversation_id = conversations.id
        WHERE conversation_participants.user_id = %s
        AND conversations.is_group is FALSE
        ORDER BY conversations.updated_at DESC
        """
        self.cursor.execute(
            query, (user_id,)
        )
        if self.cursor.rowcount > 0:
            return self.cursor.fetchone()["conversation_id"]
        return None
    def check_conversation_by_id(self, conversation_id: str):
        """
        Check conversation count in DB using provided id
        :param conversation_id: conversation id (uuid format)
        :return:
        """
        query = f"""
            SELECT id 
            FROM conversations
            WHERE id = %s
        """
        self.cursor.execute(query, (conversation_id,))
        return self.cursor.rowcount

    def set_role(self, role: str, user_name: str):
        query = f"""
            UPDATE users 
            SET role = %s
            WHERE display_name = %s
        """
        self.cursor.execute(query, (role, user_name,))

    def make_conversation_unread(self,  user_id: str, conversation_id: str):
        query = f"""
            UPDATE conversation_participants 
            SET last_read_at = NULL
            WHERE user_id = %s
            AND conversation_id = %s
        """
        self.cursor.execute(query, (user_id, conversation_id,))
        self.connection.commit()

    def make_conversation_read(self,  user_id: str, conversation_id: str):
        last_read_at = data_helper.get_date_from_now(date_step="days", amount_to_change=-1)
        query = f"""
            UPDATE conversation_participants 
            SET last_read_at = %s
            WHERE user_id = %s
            AND conversation_id = %s
        """
        self.cursor.execute(query, (last_read_at, user_id, conversation_id,))
        self.connection.commit()

    def mark_all_notifications_unread(self, for_user: str = "Admin"):
        """
        Make all notifications unread for user with specified user (alias)
        :param for_user: user's alias, used to get correct user id for DB query
        :return:
        """
        query = f"""
            UPDATE notifications
            SET is_read = false 
            WHERE user_id IN (SELECT id from users WHERE display_name = %s)
        """
        self.cursor.execute(query, (for_user,))
        self.connection.commit()

    def delete_conversation(self, conversation_id: str):
        """
        Make all notifications unread for user with specified user (alias)
        :param conversation_id: conversation id (uuid format)
        :return:
        """
        query = f"DELETE FROM conversations WHERE id = %s"
        self.cursor.execute(query, (conversation_id,))
        self.connection.commit()


    def close_connection(self):
        self.connection.close()