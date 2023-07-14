from src.channel import youtube


class IncorrectId(Exception):
    def __init__(self, *args, **kwargs):
        self.message = args[0] if args else 'Видео с таким id не существует'


class Video:
    def __init__(self, id_video):
        self.id_video = id_video
        try:

            self.video_response = youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                        id=self.id_video).execute()
            if len(self.video_response["items"]) == 0:
                raise IncorrectId
        except IncorrectId as m:
            print(m)
            self.title = None
            self.url = None
            self.view_count = None
            self.like_count = None
        else:
            self.title: str = self.video_response['items'][0]['snippet']['title']
            self.video_url: str = f"https://www.youtube.com/watch?v={self.id_video}"
            self.view_count: int = self.video_response['items'][0]['statistics']['viewCount']
            self.like_count: int = self.video_response['items'][0]['statistics']['likeCount']

    def __str__(self):
        return self.title


class PLVideo(Video):

    def __init__(self, id_video, id_playlist):
        self.id_video = id_video
        super().__init__(self.id_video)
        self.id_playlist = id_playlist

    def __str__(self):
        return self.title
