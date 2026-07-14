from dataclasses import dataclass
from uuid import UUID
from dataclasses import asdict


@dataclass(slots=True)
class UserRegisteredEvent:
    user_id: UUID
    email: str
    username: str


@dataclass(slots=True)
class UserLoggedInEvent:
    user_id: UUID
    email: str



@dataclass(slots=True)
class UserChangedPasswordEvent:
    user_id: UUID
    email: str
    username: str
    
