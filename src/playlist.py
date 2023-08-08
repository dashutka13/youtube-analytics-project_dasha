import isodate

from src.channel import Channel


class PlayList:
    """Класс для ютуб-плейлиста"""
    def __init__(self, playlist_id):
        """
        Экземпляр инициализируется id плейлиста. Дальше все данные будут подтягиваться по API.
        """
        self.playlist_id = playlist_id
        self.youtube = Channel.get_service()
        playlists = self.youtube.playlists().list(id=self.playlist_id,
                                                            part='snippet',
                                                            maxResults=50,
                                                            ).execute()

        self.title = playlists["items"][0]["snippet"]["title"]
        self.url = f"https://www.youtube.com/playlist?list={self.playlist_id}"

    @property
    def total_duration(self):
        """
        возвращает объект класса datetime.timedelta с суммарной длительность плейлиста
        """
        playlist_videos = self.youtube.playlistItems().list(playlistId=self.playlist_id,
                                                       part='contentDetails',
                                                       maxResults=50,
                                                       ).execute()

        video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]

        video_response = self.youtube.videos().list(part='contentDetails,statistics',
                                               id=','.join(video_ids)
                                               ).execute()

        video_length = []
        for video in video_response['items']:
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            video_length.append(duration)
        return video_length[0] + video_length[1] + video_length[2] + video_length[3]

    def show_best_video(self):
        """
        возвращает ссылку на самое популярное видео из плейлиста (по количеству лайков)
        """
        playlist_videos = self.youtube.playlistItems().list(playlistId=self.playlist_id,
                                                            part='contentDetails',
                                                            maxResults=50,
                                                            ).execute()

        video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]

        video_response = self.youtube.videos().list(part='contentDetails,statistics',
                                                    id=','.join(video_ids)
                                                    ).execute()

        like_count = 0
        video_url = ""

        for video in video_response['items']:
            if int(video['statistics']['likeCount']) > like_count:
                like_count = int(video['statistics']['likeCount'])
                video_url = f"https://youtu.be/{video['id']}"
        return video_url
