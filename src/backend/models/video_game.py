import datetime
from turtle import title


class Game:
    def __init__(
        self,
        ratingId: str,
        title: str,
        rating: int,
        dateCompleted: str, # TODO: use more precise, like seconds? 
        releaseDate: str,
        coverArt: str,
        userId: str,
    ):
        self.ratingId = ratingId
        self.title = title
        self.rating = rating
        self.dateCompleted = dateCompleted
        self.releaseDate = releaseDate
        self.coverArt = coverArt
        self.userId = userId
