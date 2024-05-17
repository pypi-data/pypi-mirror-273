import os
import random
from typing import Any, Dict

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
    def get_video(self, video_url: str, download: bool = True, download_path: str = "") -> dict:
        """Get video and video information

        Args:
            video_url (str):
            download (bool, optional): [description]. Defaults to True.

        Returns:
            dict: Contains video information
        """
        youtube_dl_opts = {
            "quiet": True,
            "outtmpl": f"{download_path}/%(id)s.%(ext)s",
        }
        with YoutubeDL(youtube_dl_opts) as ydl:
            extracted_info_dict: Dict[str, Any] | None = ydl.extract_info(video_url, download=download)

        if extracted_info_dict is None:
            logger.error(f"Clip URL: {video_url} | Clip not available")
            info_dict: Dict[str, Any] = {"title": None, "url": None, "id": None, "streamer": None, "date": None, "file_size": None}
            return info_dict
        else:
            info_dict = extracted_info_dict

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
                # get the id of the video from the filename
                file_id = filename.split("/")[-1].split(".")[0]
                mirror = client.upload_video(f, f"{file_id}.mp4")
        except Exception as e:
            logger.error(f"Error uploading video: {e}")
            return VideoClient(url="", shortcode="", host="", filename="")
        if delete_file:
            # remove file
            os.remove(clip_file)

        return mirror

    def full(self, video_url: str, download_path: str = "", delete_file: bool = False) -> VideoClient:
        """Download and upload video

        Args:
            video_url (str): Video URL
            download_path (str, optional): Download path. Defaults to "".
            delete_file (bool, optional): Delete file after upload. Defaults to False.

        Returns:
            VideoClient: VideoClient object
        """
        video = self.get_video(video_url, download=True, download_path=download_path)
        
        # if download_path does not end with a slash, add one
        if download_path and not download_path.endswith("/"):
            download_path += "/"
        filename = download_path + video["filename"]
        print(filename)
        return self.upload_video(video["title"], filename=filename, delete_file=delete_file)