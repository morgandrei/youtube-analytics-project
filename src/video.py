from src.channel import youtube


class Video:
    def __init__(self, id_video):
        self.id_video = id_video
        video_response = youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                               id=self.id_video).execute()
        self.video_title: str = video_response['items'][0]['snippet']['title']
        self.video_url: str = f"https://www.youtube.com/watch?v={self.id_video}"
        self.view_count: int = video_response['items'][0]['statistics']['viewCount']
        self.like_count: int = video_response['items'][0]['statistics']['likeCount']

    def __str__(self):
        return self.video_title


class PLVideo(Video):

    def __init__(self, id_video, id_playlist):
        self.id_video = id_video
        super().__init__(self.id_video)
        self.id_playlist = id_playlist

    def __str__(self):
        return self.video_title
