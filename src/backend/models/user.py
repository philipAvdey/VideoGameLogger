from dataclasses import dataclass, field
import datetime
from typing import List
import uuid

@dataclass
class User:
    userId: str
    username: str
    password: str
    diary: List[dict] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict) -> 'User':
        """Create User from dictionary"""
        if not isinstance(data, dict):
            raise ValueError("User data must be a dictionary")
        
        # Ensure required fields exist
        user_id = data.get('userId')
        username = data.get('username')
        password = data.get('password')
        
        if not user_id:
            user_id = str(uuid.uuid4())
        if not username:
            raise ValueError("User username is required")
        if not password:
            raise ValueError("User password is required")
        
        return cls(
            userId=user_id,
            username=username,
            password=password,
            diary=data.get('diary', []),
        )

    def to_dict(self) -> dict:
        """Convert User to dictionary"""
        return {
            'userId': self.userId,
            'username': self.username,
            'password': self.password,
            'diary': self.diary,
        }