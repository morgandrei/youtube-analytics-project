import datetime
import isodate

from src.channel import youtube


class PlayList:

    def __init__(self, playlist_id):
        self.__playlist_id = playlist_id
        self.__youtube = youtube
        playlist_videos = self.__youtube.playlists().list(id=self.__playlist_id,
                                                          part='snippet',
                                                          maxResults=50,
                                                          ).execute()
        self.title = playlist_videos["items"][0]["snippet"]["title"]
        self.url = f"https://www.youtube.com/playlist?list={self.__playlist_id}"

    @property
    def total_duration(self):
        total = datetime.timedelta()
        videos = self.get_videos()['items']
        for video in videos:
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            total += duration
        return total

    def show_best_video(self):
        videos = self.get_videos()['items']
        best_video_id = max(videos, key=lambda x: int(x['statistics']['likeCount']))
        url_best_video = f'https://youtu.be/{best_video_id["id"]}'
        return url_best_video

    def get_playlist_videos(self):
        return youtube.playlistItems().list(playlistId=self.__playlist_id,
                                            part='contentDetails, snippet',
                                            maxResults=50).execute()

    def get_videos(self):
        video_ids: list[str] = [video['contentDetails']['videoId'] for video in self.get_playlist_videos()['items']]
        return youtube.videos().list(part='contentDetails,statistics',
                                     id=','.join(video_ids)
                                     ).execute()
