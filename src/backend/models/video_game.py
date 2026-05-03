from dataclasses import asdict, dataclass
import uuid

@dataclass
class Game:
    gameId: str
    title: str
    rating: int
    dateCompleted: str # TODO: use more precise, like seconds? 
    releaseDate: str
    coverArt: str
    userId: str
    ratingId: str

    @classmethod
    def from_dict(cls, data: dict) -> 'Game':
        """Create Game from dictionary"""

        user_id = data.get('userId')
        title = data.get('title')
        dateCompleted = data.get('dateCompleted')
        
        if not user_id:
            user_id = str(uuid.uuid4())
        if not dateCompleted:
            raise ValueError("User dateCompleted is required")
        if not title:
            raise ValueError("User title is required")
        
        return cls(
            gameId=data.get('gameId', str(uuid.uuid4())),
            title=title,
            rating=data.get('rating', 0),
            dateCompleted=dateCompleted,
            releaseDate=data.get('releaseDate', ''),
            coverArt=data.get('coverArt', ''),
            userId=user_id,
            ratingId=str(uuid.uuid4())
        )

    def to_dict(self) -> dict:
        """Convert Game to dictionary"""
        return asdict(self)