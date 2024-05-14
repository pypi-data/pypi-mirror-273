import os
import random

from requests import Session
from retry import retry
from pyVHL.mirror_clients import Client
from youtube_dl import YoutubeDL
from loguru import logger

from pyVHL.model._model import VideoClient


class pyvhl:
    """
    Handles proccessing of mirroring videos from Reddit and Twitter.
    """

    def __init__(self) -> None:
        session = Session()
        session.headers["User-Agent"] = "pyVHL/0.1.2"
        self.client = Client(session=session)
        self.clients = {
            "streamable": self.client.streamable,
            "catbox": self.client.catbox,
        }

    @retry(delay=5, tries=5)
    def get_video(self, video_url: str, download: bool = True) -> dict:
        """Get video and video information

        Args:
            video_url (str):
            download (bool, optional): [description]. Defaults to True.

        Returns:
            dict: Contains video information
        """
        youtube_dl_opts = {
            "quiet": True,
            "outtmpl": "%(id)s.%(ext)s",
        }
        with YoutubeDL(youtube_dl_opts) as ydl:
            info_dict = ydl.extract_info(video_url, download=download)

        # get size of file downloaded
        if download:
            file_size = os.stat(info_dict["id"] + "." + info_dict["ext"]).st_size
        else:
            file_size = 0

        if info_dict["extractor"] == "twitch:clips":
            clip_title = info_dict["title"]
            clip_url = info_dict["formats"][-1]["url"]
            clip_id = info_dict["id"]
            clip_streamer = info_dict["creator"]
            clip_date = info_dict["upload_date"]
            extractor = info_dict["extractor"]
            return {
                "filename": info_dict["id"] + "." + info_dict["ext"],  # "filename": "clip.mp4
                "title": clip_title,
                "url": clip_url,
                "id": clip_id,
                "streamer": clip_streamer,
                "date": clip_date,
                "extractor": extractor,
                "file_size": file_size,
            }

        elif info_dict["extractor"] == "youtube":
            clip_title = info_dict["title"]
            clip_url = info_dict["webpage_url"]
            clip_id = info_dict["id"]
            clip_streamer = video_url.split("/")[3]
            clip_date = info_dict["upload_date"]
            extractor = info_dict["extractor"]
            return {
                "filename": info_dict["id"] + "." + info_dict["ext"],  # "filename": "clip.mp4
                "title": clip_title,
                "url": clip_url,
                "id": clip_id,
                "streamer": clip_streamer,
                "date": clip_date,
                "extractor": extractor,
                "file_size": file_size,
            }

        elif info_dict["extractor"] == "facebook":
            info_dict = info_dict["entries"][-1]
            clip_title = info_dict["title"]
            clip_url = info_dict["url"]
            clip_id = info_dict["id"]
            clip_streamer = video_url.split("/")[3]
            clip_date = info_dict["upload_date"]
            extractor = info_dict["extractor"]
            return {
                "title": clip_title,
                "url": clip_url,
                "id": clip_id,
                "streamer": clip_streamer,
                "date": clip_date,
                "extractor": extractor,
                "file_size": file_size,
            }

        elif info_dict["extractor"] == "fb":
            info_dict = info_dict["entries"][-1]
            clip_title = info_dict["title"]
            clip_url = info_dict["url"]
            clip_id = info_dict["id"]
            clip_streamer = video_url.split("/")[3]
            clip_date = info_dict["upload_date"]
            extractor = info_dict["extractor"]
            return {
                "title": clip_title,
                "url": clip_url,
                "id": clip_id,
                "streamer": clip_streamer,
                "date": clip_date,
                "extractor": extractor,
            }

        elif info_dict["extractor"] == "generic":
            clip_title = info_dict["title"]
            clip_url = info_dict["webpage_url"]
            clip_id = info_dict["id"]
            clip_streamer = info_dict["uploader"]
            clip_date = info_dict["upload_date"]
            return {
                "title": clip_title,
                "url": clip_url,
                "id": clip_id,
                "streamer": clip_streamer,
                "date": clip_date,
                "file_size": file_size,
            }

        else:
            logger.error(f"Clip URL: {video_url} | Clip not available")
            return {"title": None, "url": None, "id": None, "streamer": None, "date": None, "file_size": None}

    @retry(tries=10, delay=5)
    def upload_video(self, clip_title: str, filename: str, host: str = "", delete_file=False) -> VideoClient:
        """Uploads clip to one of the mirror clients

        Args:
            clip_title (str): Clip title
            filename (str): Clip filename
            host (str): Mirror host. Defaults to random host. Must be either 'streamable' or 'catbox'
            delete_file (bool): Delete file after upload. Defaults to False
        Returns:
            dict: Contains mirror url and host
        """
        if host not in ["streamable", "catbox", ""]:
            raise ValueError("Invalid host, must be either 'streamable' or 'catbox'")
        if host:
            client_name = host
            client = self.clients[host]
        else:
            client_name = random.choice(list(self.clients.keys()))
            client = self.clients[client_name]

        clip_file = None
        if os.path.exists(filename):
            clip_file = filename
        else:
            raise FileNotFoundError("Clip file not found")

        try:
            with open(clip_file, "rb") as f:
                mirror = client.upload_video(f, f"{id}.mp4")
        except Exception as e:
            logger.error(f"Error uploading video: {e}")
            return {"url": mirror.url, "host": client_name}
        if delete_file:
            # remove file
            os.remove(clip_file)

        return mirror
