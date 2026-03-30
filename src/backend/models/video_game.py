import datetime


class VideoGame:
    def __init__(
        self,
        id: str,
        user_id: str,  # user id that logged this game
        name: str,
        cover_url: str,
        date_finished: datetime.date,
        rating: float,
        review: str,
    ):
        self.str = str
        self.id = id
        self.name = name
        # TODO: get image via url, which we can probably get via API. if we cannot get image, then use default
        self.cover_url = cover_url
        self.user_id = user_id
        self.date_finished = date_finished
        self.rating = rating
        self.review = review
