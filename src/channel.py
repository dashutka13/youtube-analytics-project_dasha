import json
import os

from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id

        youtube = Channel.get_service()
        result = youtube.channels().list(id=self.get_channel_id, part="snippet, statistics").execute()

        self.title = result["items"][0]["snippet"]["title"]
        self.description = result["items"][0]["snippet"]["description"].split(":)")[0]
        self.url = f"https://www.youtube.com/channel/{self.get_channel_id}"
        self.subscriber_count = result["items"][0]["statistics"]["subscriberCount"]
        self.video_count = result["items"][0]["statistics"]["videoCount"]
        self.view_count = result["items"][0]["statistics"]["viewCount"]

    def __str__(self):
        return f'{self.title} ({self.url})'

    def __add__(self, other):
        return int(self.subscriber_count) + int(other.subscriber_count)

    def __sub__(self, other):
        return int(self.subscriber_count) - int(other.subscriber_count)

    def __gt__(self, other):
        return self.subscriber_count > other.subscriber_count

    def __ge__(self, other):
        return self.subscriber_count >= other.subscriber_count

    def __lt__(self, other):
        return self.subscriber_count < other.subscriber_count

    def __le__(self, other):
        return self.subscriber_count <= other.subscriber_count

    def __eq__(self, other):
        return self.subscriber_count == other.subscriber_count

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        api_key: str = os.getenv('API')
        youtube = build('youtube', 'v3', developerKey=api_key)
        channel = youtube.channels().list(id=self.get_channel_id, part="snippet, statistics").execute()
        channel = json.dumps(channel, indent=2, ensure_ascii=False)
        print(channel)

    @property
    def get_channel_id(self):
        return self.__channel_id

    @classmethod
    def get_service(cls):
        """
        класс-метод, возвращающий объект для работы с YouTube API
        """
        api_key: str = os.getenv('API')
        return build('youtube', 'v3', developerKey=api_key)

    def to_json(self, save_to_json):
        """
        метод, сохраняющий в файл значения атрибутов экземпляра Channel
        """
        add_to_json = {
            "channel_id": self.get_channel_id,
            "title": self.title,
            "description": self.description,
            "url": self.url,
            "video_count": self.video_count,
            "view_count": self.view_count,
            "subscriber_count": self.subscriber_count
        }
        with open(save_to_json, "w", encoding="utf-8") as file:
            json.dump(add_to_json, file)
