import os
import platform
import random
import string
from datetime import datetime, timezone, timedelta

from faker import Faker

from auth.credentials import Credentials
fake = Faker()
creds = Credentials()





def is_not_recent(created_at: datetime, minutes: int = 15) -> bool:
    """Check, if post created >N minutes ago"""
    now = datetime.now(timezone.utc)
    return (now - created_at) >= timedelta(minutes=minutes)




def find_not_recent_comment(comments, username):
    """Return the comment of specified author by username, published  > 15 minutes ago"""
    for comment in comments:
        if comment.author.username == username and is_not_recent(comment.created_at):
            return comment.id
    return None



def find_other_authors_post(posts, username):
    """Return post id of post, created by another user. Checked by post author's username"""
    for post in posts:
        if post.author.username != username:
            return post.id
    return None

def find_other_authors_comment(comments, username):
    """Return post id of post, created by another user. Checked by post author's username"""
    for comment in comments:
        if comment.author.username != username:
            return comment.id
    return None


class DataHelper:
    @staticmethod
    def get_path_to_file(file_name: str = None, folders: str = None):
        """
        Method, that prepared path to specified file name and folders.
        :param file_name: prepared name, required to build file path
        :param folders: prepared folder name, if file is placed in certain folder
        :return:
        """
        if folders is not None:
            os_name = platform.system()
            if os_name == "Darwin":
                folders = folders.replace("\\", "/")
            elif os_name == "Windows":
                folders = folders.replace("/", "\\")
            return os.path.join(os.getcwd(), f"{folders}", f"{file_name}")
        return os.path.join(os.getcwd(), f"{file_name}")

    def get_file_as_binary(self, image_file_name: str = None, folders: str = "test_data") -> bytes:
        """
        :param image_file_name: filename of image
        :param folders: optional, if images is placed at certain folder of project
        :return: binary format of provided image
        """
        path_to_file = self.get_path_to_file(file_name=image_file_name, folders=folders)
        print(path_to_file)
        with open (path_to_file, "rb") as f:
            file_content = f.read()
        return file_content

    @staticmethod
    def find_not_recent_post(posts, username):
        """Return the post of specified author by username, published  > 15 minutes ago"""
        for post in posts:
            if post.author.username == username and is_not_recent(post.created_at):
                return post.id
        return None

    def generate_string(self, length=10):
        """Генерирует слуself, чайную строку заданной длины"""
        letters = string.ascii_letters
        result = ""
        for _ in range(length):
            result += random.choice(letters)
        return result

    def generate_number(self, min_val=0, max_val=100):
        """Генерирует случайное число в заданном диапазоне"""
        return random.randint(min_val, max_val)

    def generate_email(self, domain="example.com"):
        """Генерирует случайный email"""
        username = fake.username()
        return f"{username}@{domain}"

    def generate_phone_number(self, country_code="+1"):
        """Генерирует случайный номер телефона"""
        return f"{country_code} {random.randint(100, 999)}-{random.randint(100, 999)}-{random.randint(1000, 9999)}"

    @staticmethod
    def generate_text(max_len=100):
        return fake.text(max_len)


    def get_random_post_payload(self, hashtags:bool=False):
        """Generates random post payload depending on allowed property values and max content length"""
        max_content_length = 2000
        hashtag_list = ["#buzzhive", "#devlife", "#tech", "#photograhy", "#coding", "#tech", "#nature", "#hello", "#automation", "#qa"]
        visibility_options = ["public", "followers_only"]
        image_url_options = [None, "temp_data/image.png"]
        random_content = self.generate_text(max_content_length)
        if hashtags:
            random_content = random_content +"\n"+random.choice(hashtag_list)
        return {
            "content": random_content,
            "image_url": random.choice(image_url_options),
            "visibility": random.choice(visibility_options)
        }

    def get_random_comment_payload(self):
        """Generates random comment payload depending on max content length"""
        max_content_length = 1000
        random_content = self.generate_text(max_content_length)
        return {
            "content": random_content,
        }

    def get_participant_id(self, alis:str):
        return creds.get_user(alis).user_id

    def get_random_username(self):
        return fake.user_name()

    def get_not_existed_uuid(self):
        return fake.uuid4()
    @staticmethod
    def get_date_from_now(date_step:str="days", amount_to_change:int=0):
        """
        Method to get date at YYYY-mm-ddTHH:MM:SS.ffZ format.
        :param date_step: interval type of time offset (Optional). By default - 'hours'
        :param amount_to_change:value of offset. Allows negative values to subtract provided about from now. By default - 0
        :return: Return time now by default at provided format
        """
        data_updater = {"hours": timedelta(hours=amount_to_change),
                         "minutes": timedelta(minutes=amount_to_change),
                         "days": timedelta(days=amount_to_change),
                         "years": timedelta(days=365*amount_to_change)}
        assert date_step in data_updater.keys(), "Unknown date_step"
        fake_date = fake.date_time().now()
        fake_date = fake_date + data_updater[date_step]
        return fake_date.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

    def get_invalid_uuid(self,):
        return fake.uuid4()[0:-2]


