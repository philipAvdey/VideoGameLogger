import datetime


class SearchResult:
    def __init__(
        self,
        id: str,
        title: str,
        coverArt: str,
        releaseDate: str,
        ratingCount: int
    ):
        self.id = id
        self.title = title
        self.coverArt = coverArt
        self.ratingCount = ratingCount
        self.releaseDate = releaseDate