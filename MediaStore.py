import yaml
import os
from instagrapi.types import Media
from urllib.request import urlretrieve

MEDIA_LIST_YAML_PATH = "media_list.yaml"

class VideoInfo:

    def __init__(
        self,
        video_file_name,
        content_id,
        caption_text,
        like_count,
    ):
        self.video_file_name = video_file_name
        self.content_id = content_id
        self.caption_text = caption_text
        self.like_count = like_count

    @classmethod
    def from_media(cls, ig_media:Media, download=True, download_dir:str="./videos"):
        url = ig_media.video_url
        if url is None:
            print("cannot put non reel media in VideoInfo")
            return None

        content_id = ig_media.id
        video_file_name = f"{content_id}.mp4"
        caption_text = ig_media.caption_text

        # download video
        if download:
            video_path = os.path.join(download_dir, video_file_name)
            urlretrieve(str(url), video_path)

        video_info = VideoInfo(
            video_file_name=video_file_name,
            content_id=content_id,
            caption_text=caption_text,
            like_count=ig_media.like_count
        )

        return video_info
    
    def encode(self):
        return {
            "video_file_name": self.video_file_name,
            "content_id": self.content_id,
            "caption_text": self.caption_text,
            "like_count": self.like_count
        }
    
    @classmethod
    def decode(cls, data):
        return VideoInfo(
            video_file_name=data["video_file_name"],
            content_id=data["content_id"],
            caption_text=data["caption_text"],
            like_count=data["like_count"]
        )

class MediaStore:

    def __init__(self, media_store_path:str):
        self.media_store_path = media_store_path
        if not os.path.exists(media_store_path):
            os.makedirs(media_store_path)
        # if the yaml file doesn't exist, create it
        if not os.path.exists(self._get_media_list_path()):
            with open(self._get_media_list_path(), 'w') as f:
                yaml.dump({}, f)

    def save_media(self, ig_media:Media):
        # add step to distinguish content type here
        video_info = VideoInfo.from_media(ig_media, download=True, download_dir=self.media_store_path)
        if video_info is None:
            print("cannot save media")
            return

        media_list = self._load_media_list()
        media_list[video_info.content_id] = video_info.encode()
        self._save_media_list(media_list)

    def save_medias(self, medias:list[Media]):
        for media in medias:
            self.save_media(media)

    def delete_media_by_content_id(self, content_id:str):
        media_list = self._load_media_list()
        del media_list[content_id]
        self._save_media_list(media_list)

    def delete_media(self, video_info:VideoInfo):
        self.delete_media_by_content_id(video_info.content_id)

    def get_all_media(self):
        media_list = self._load_media_list()
        return {content_id: VideoInfo.decode(data) for content_id, data in media_list.items()}
    
    def get_one_media(self):
        media_list = self._load_media_list()
        if len(media_list) == 0:
            return None
        content_id, data = media_list.popitem()
        return VideoInfo.decode(data)

    def _get_media_list_path(self):
        return os.path.join(self.media_store_path, MEDIA_LIST_YAML_PATH)
    
    def _load_media_list(self):
        with open(self._get_media_list_path(), 'r') as f:
            return yaml.load(f, Loader=yaml.FullLoader)
        
    def _save_media_list(self, media_list):
        with open(self._get_media_list_path(), 'w') as f:
            yaml.dump(media_list, f)
        