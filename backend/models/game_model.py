from backend.models.achv_model import Achv
from pydantic import BaseModel

class Game(BaseModel):
    id : str
    title: str
    platform: str
    url : str | None = NotImplementedError
    achievements : list[Achv] = []

    @property
    def platinum(self)->bool:
        return bool(self.achievements) and all(a.unlocked for a in self.achievements)