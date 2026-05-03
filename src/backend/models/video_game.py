import datetime
from turtle import title


class Game:
    def __init__(
        self,
        ratingId: str,
        username: str,
        title: str,
        rating: int,
        dateCompleted: str, # TODO: use more precise, like seconds? 
        releaseDate: str,
        coverArt: str
    ):
        self.ratingId = ratingId
        self.username = username # TODO: use user ID instead?
        self.title = title
        self.rating = rating
        self.dateCompleted = dateCompleted
        self.releaseDate = releaseDate
        self.coverArt = coverArt
