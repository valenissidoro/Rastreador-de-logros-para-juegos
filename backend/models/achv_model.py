from enum import StrEnum
from pydantic import BaseModel

class Tags(StrEnum):
    Story = "STORY"
    Missable = "MISSABLE"
    Grind = "GRIND"
    Unmissable = "UNMISSABLE"
    Collectable = "COLLECTABLE"
    RNG = "RNG"
    Multiplayer = "MULTIPLAYER"
    TimeLimited = "TIME LIMITED"
    Buggy = "BUGGY"
    Stackable = "STACKABLE"
    TwoController = "TWO CONTROLLER"
    DifficultySpecific = "DIFFICULTY SPECIFIC"


class Achv(BaseModel):
    id : int
    title : str
    tag : list[Tags] = []
    description : str
    guide : str
    unlocked : bool = False