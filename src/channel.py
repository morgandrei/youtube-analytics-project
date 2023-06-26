import os

from googleapiclient.discovery import build
import json

api_key: str = os.getenv('YT_API_KEY')
youtube = build('youtube', 'v3', developerKey=api_key)


class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.channel_id = channel_id
        self.channel = youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()
        self.title = self.channel["items"][0]["snippet"]["title"]
        self.description = self.channel["items"][0]["snippet"]["description"]
        self.url = f"https://www.youtube.com/" + self.channel['items'][0]['snippet']['customUrl']
        self.subscriber_count = self.channel["items"][0]["statistics"]["subscriberCount"]
        self.video_count = self.channel["items"][0]["statistics"]["videoCount"]
        self.view_count = self.channel["items"][0]["statistics"]["viewCount"]

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        channel = youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()
        print(json.dumps(channel, indent=2, ensure_ascii=False))

    @classmethod
    def get_service(cls):
        """Метод, возвращающий объект для работы с YouTube API"""
        return build('youtube', 'v3', developerKey=api_key)

    def to_json(self, data):

        with open(data, 'w', encoding='utf-8') as file:
            """Метод, сохраняющий в файл значения атрибутов экземпляра"""
            json.dump({'channel_id': self.channel_id,
                       'title': self.title,
                       'description': self.description,
                       'url': self.url,
                       'subscriberCount': self.subscriber_count,
                       'videoCount': self.video_count,
                       'viewCount': self.view_count}, file, ensure_ascii=False, indent=2)

