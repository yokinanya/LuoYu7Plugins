from typing import Callable, Literal
from nonebot.adapters.onebot.v11.message import Message, MessageSegment

from .arknights import draw_one_arknights, draw_ten_arknights
from .arknights_2 import draw_one_arknights_2, draw_ten_arknights_2


T_DrawDeck = Callable[[int], str | Message | MessageSegment]
"""抽卡函数"""
_DECK: dict[str, T_DrawDeck] = {
    # '明日方舟轮换池单抽': draw_one_arknights,
    # '明日方舟轮换池十连': draw_ten_arknights,
    '明日方舟单抽': draw_one_arknights_2,
    '明日方舟十连': draw_ten_arknights_2,
}
"""可用的抽卡函数"""


def _draw(draw_deck: T_DrawDeck, draw_seed: int) -> str | Message | MessageSegment:
    result = draw_deck(draw_seed)
    return result


def draw(deck_name: str, draw_seed: int) -> str | Message | MessageSegment:
    draw_deck = _DECK[deck_name]
    result = _draw(draw_deck=draw_deck, draw_seed=draw_seed)
    return result


def get_deck() -> list[str]:
    return [str(x) for x in _DECK.keys()]


__all__ = [
    'draw',
    'get_deck'
]
