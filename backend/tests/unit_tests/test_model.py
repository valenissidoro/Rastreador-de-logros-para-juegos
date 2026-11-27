from backend.models.game_model import Game
from backend.models.achv_model import Achv
from pydantic import ValidationError
import pytest

# Vamos a testear usando enfoque de caja negra, en particular. Analisis de valores limites.
INVALID_GAME_CASES = [
    {"id": "1", "title": "No platform Game", "url": "ex.com", "achievements": []},
    {
        "title": "No id Game",
        "url": "exapmle2.com",
        "platform": "Nintendo",
        "achievements": [],
    },
    {"id": "2", "platform": "No title Game", "url": "exapmle3.com", "achievements": []},
]


INVALID_ACHIEVEMENT_CASES = [
    {
        "id": 1,
        "title": "No guide achv",
        "tag": [],
        "description": "example 1",
        "unlocked": True,
    },
    {
        "id": 2,
        "title": "No description achv",
        "tag": [],
        "guide": "example 2",
        "unlocked": True,
    },
    {
        "id": 3,
        "tag": [],
        "description": "No title achv",
        "guide": "example 3",
        "unlocked": False,
    },
    {
        "title": "No id achv",
        "tag": [],
        "description": "Example 4",
        "guide": "lalalala",
        "unlocked": True,
    },
    {
        "id": 5,
        "title": "Invalid tag",
        "tag": ["MISSABLE", "INVALID_TAG", "STORY"],
        "description": "Example 4",
        "guide": "lalalala",
        "unlocked": True,
    },
    {
        "id": "not a number",
        "title": "Invalid tag",
        "tag": ["MISSABLE","STORY"],
        "description": "Example 4",
        "guide": "lalalala",
        "unlocked": True,
    },
]


# Creo un logro valido
@pytest.fixture
def instance_valid_achievement():
    valid_achievement = Achv(
        id=2,
        title="Jumping Jack",
        tag=["MISSABLE", "GRIND"],
        description="Jump a lot",
        guide="Jump a thounsand time as Link",
        unlocked=True,
    )
    return valid_achievement


# Creo el juego valido que voy a usar en todos los tests.
@pytest.fixture
def instance_valid_game(instance_valid_achievement):
    valid_game = Game(
        id="1",
        title="Mayora's Maks",
        platform="Nintendo",
        url="www.exampleurl.com",
        achievements=[instance_valid_achievement],
    )
    return valid_game


def test_platinum_false_when_achievements_is_empty():
    empty_achievements = Game(
        id="1",
        title="Mayora's Maks",
        platform="Nintendo",
        url="www.exampleurl.com",
        achievements=[],
    )

    assert empty_achievements.platinum is False


def test_platinum_true_when_achievements_all_true(instance_valid_game):
    assert instance_valid_game.platinum is True


def test_platinum_false_when_mix(instance_valid_game):
    achievement = Achv(
        id=3,
        title="Jumping Jack",
        tag=["MISSABLE", "GRIND"],
        description="Jump a lot",
        guide="Jump a thounsand time as Link",
        unlocked=False,
    )
    instance_valid_game.achievements.append(achievement)

    assert instance_valid_game.platinum is False


def test_unlocked_is_false_on_default():
    false_unlocked_achv = Achv(
        id=4,
        title="example",
        tag=["GRIND", "STORY"],
        description="do nothing",
        guide="example",
    )

    assert false_unlocked_achv.unlocked is False


def test_tag_is_empty_on_default():
    empty_tag_achv = Achv(
        id=4,
        title="example",
        description="do nothing",
        guide="example2",
        unlocked=False,
    )

    assert empty_tag_achv.tag == []


@pytest.mark.parametrize("invalid_game", INVALID_GAME_CASES)
def test_invalid_game(invalid_game):
    with pytest.raises(ValidationError):
        Game(**invalid_game)


@pytest.mark.parametrize("invalid_achievement", INVALID_ACHIEVEMENT_CASES)
def test_invalid_achievement(invalid_achievement):
    with pytest.raises(ValidationError):
        Achv(**invalid_achievement)
