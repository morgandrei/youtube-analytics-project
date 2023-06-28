import os

from googleapiclient.discovery import build
import json

api_key: str = os.getenv('YT_API_KEY')
youtube = build('youtube', 'v3', developerKey=api_key)


class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id
        self.__channel = youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        self.title = self.__channel["items"][0]["snippet"]["title"]
        self.description = self.__channel["items"][0]["snippet"]["description"]
        self.url = f"https://www.youtube.com/" + self.__channel['items'][0]['snippet']['customUrl']
        self.subscriber_count = int(self.__channel["items"][0]["statistics"]["subscriberCount"])
        self.video_count = int(self.__channel["items"][0]["statistics"]["videoCount"])
        self.view_count = int(self.__channel["items"][0]["statistics"]["viewCount"])

    def __str__(self):
        return str(f"'{self.title} ({self.url})'")

    def __add__(self, highload):
        """Метод для операции сложения"""
        return int(self.subscriber_count + highload.subscriber_count)

    def __sub__(self, highload):
        """Метод для операции вычитания"""
        return self.subscriber_count - highload.subscriber_count

    def __sub__(self, highload):
        """Метод для операции вычитания"""
        return highload.subscriber_count - self.subscriber_count

    def __gt__(self, highload):
        """Метод для операции сравнения «больше»"""
        return highload.subscriber_count < self.subscriber_count

    def __ge__(self, highload):
        """Метод для операции сравнения «больше или равно»"""
        return highload.subscriber_count <= self.subscriber_count

    def __lt__(self, highload):
        """Метод для операции сравнения «меньше»"""
        return highload.subscriber_count > self.subscriber_count

    def __le__(self, highload):
        """Метод для операции сравнения «меньше или равно»"""
        return highload.subscriber_count >= self.subscriber_count

    @property
    def channel_id(self):
        return self.__channel_id

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        channel = youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        print(json.dumps(channel, indent=2, ensure_ascii=False))

    @classmethod
    def get_service(cls):
        """Метод, возвращающий объект для работы с YouTube API"""
        return build('youtube', 'v3', developerKey=api_key)

    def to_json(self, data):
        with open(data, 'w', encoding='utf-8') as file:
            """Метод, сохраняющий в файл значения атрибутов экземпляра"""
            json.dump({'channel_id': self.__channel_id,
                       'title': self.title,
                       'description': self.description,
                       'url': self.url,
                       'subscriberCount': self.subscriber_count,
                       'videoCount': self.video_count,
                       'viewCount': self.view_count}, file, ensure_ascii=False, indent=2)
