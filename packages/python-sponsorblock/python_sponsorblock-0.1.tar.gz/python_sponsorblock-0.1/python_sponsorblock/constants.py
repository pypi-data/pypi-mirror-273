from typing import Tuple
from dataclasses import dataclass
from enum import Enum


class Category(Enum):
    SPONSOR = "sponsor"
    SELFPROMO = "selfpromo"
    INTERACTION = "interaction"
    INTRO = "intro"
    OUTRO = "outro"
    PREVIEW = "preview"
    MUSIC_OFFTOPIC = "music_offtopic"
    FILLER = "filler"


class ActionType(Enum):
    SKIP = "skip"
    MUTE = "mute"
    FULL = "full"
    POI = "poi"
    CHAPTER = "chapter"


class Service(Enum):
    YOUTUBE = "YouTube"


@dataclass
class Segment:
    UUID: str
    segment: Tuple[float, float]
    category: Category
    videoDuration: float
    actionType: ActionType
    locked: int
    votes: int
    description: str
