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


    def generate_text(self, max_len=100):
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



    def get_not_existed_uuid(self):
        return fake.uuid4()

    def get_invalid_uuid(self,):
        return fake.uuid4()[0:-2]
