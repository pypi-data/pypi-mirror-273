from abc import ABC


class VideoClient(ABC):
    def __init__(self, url: str, shortcode: str):
        self.url: str = url
        self.shortcode: str = shortcode

    def get_video(self):
        pass


class StreamableVideo(VideoClient):
    host: str = "streamable"
    shortcode: str
    url: str = ""


class CatboxVideo(VideoClient):
    host: str = "catbox"
    shortcode: str
    url: str = ""
