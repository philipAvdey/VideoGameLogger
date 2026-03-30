from video_game import VideoGame
from typing import List


class User:
    def __init__(
        self,
        id: str,
        name: str,
        password: str,  # TODO: figure out some basic encryption
    ):
        self.str = str
        self.id = id
        self.name = name
        self.password = password
        self.diary: List[VideoGame] = (
            []
        )  # create as empty first, then we can add video games to this as they are loggged

    def add_video_game(self, video_game: VideoGame):
        self.diary.append(video_game)
