from src.channel import Channel


class Video:
    """Класс для ютуб-видеоролика"""

    def __init__(self, video_id: str):
        """
        Экземпляр инициализируется id видеоролика. Дальше все данные будут подтягиваться по API.
        """

        youtube = Channel.get_service()

        try:
            result = youtube.videos().list(id=video_id, part="snippet, statistics").execute()

            self.video_id = video_id
            self.video_title = result["items"][0]["snippet"]["title"]
            self.video_url = f"https://www.youtube.com/watch?v={self.video_id}"
            self.view_count = result["items"][0]["statistics"]["viewCount"]
            self.like_count = result["items"][0]["statistics"]["likeCount"]

        except:
            self.video_id = video_id
            self.video_title = None
            self.video_url = None
            self.view_count = None
            self.like_count = None

    def __str__(self):
        return self.video_title


class PLVideo(Video):
    def __init__(self, video_id: str, playlist_id: str):
        super().__init__(video_id)
        self.video_id = video_id
        self.channel_id = playlist_id
