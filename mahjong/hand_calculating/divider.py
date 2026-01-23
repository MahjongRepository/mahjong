from collections.abc import Collection, Sequence
from dataclasses import dataclass
from enum import Enum
from functools import lru_cache, total_ordering
from typing import Literal, Optional

from mahjong.meld import Meld
from mahjong.utils import is_chi, is_kan, is_pon


class _BlockType(Enum):
    QUAD = 0
    TRIPLET = 1
    PAIR = 2
    SEQUENCE = 3


@total_ordering
@dataclass(frozen=True)
class _Block:
    ty: _BlockType
    tile_34: int

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, _Block):
            return NotImplemented
        return (self.tile_34, self.ty.value) == (other.tile_34, other.ty.value)

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, _Block):
            return NotImplemented
        return (self.tile_34, self.ty.value) < (other.tile_34, other.ty.value)

    @classmethod
    def from_meld(cls, meld: Meld) -> "_Block":
        tiles_34 = meld.tiles_34
        if is_chi(tiles_34):
            return cls(_BlockType.SEQUENCE, tiles_34[0])
        elif is_pon(tiles_34):
            return cls(_BlockType.TRIPLET, tiles_34[0])
        elif is_kan(tiles_34):
            return cls(_BlockType.QUAD, tiles_34[0])
        else:
            msg = f"invalid meld type: {meld.type}, tiles: {tiles_34}"
            raise RuntimeError(msg)

    @property
    def tiles_34(self) -> list[int]:
        if self.ty == _BlockType.QUAD:
            return [self.tile_34, self.tile_34, self.tile_34, self.tile_34]
        elif self.ty == _BlockType.TRIPLET:
            return [self.tile_34, self.tile_34, self.tile_34]
        elif self.ty == _BlockType.PAIR:
            return [self.tile_34, self.tile_34]
        elif self.ty == _BlockType.SEQUENCE:
            return [self.tile_34, self.tile_34 + 1, self.tile_34 + 2]
        else:
            msg = f"invalid block type: {self.ty}"
            raise RuntimeError(msg)


_Blocks = tuple[_Block, ...]


class HandDivider:
    @staticmethod
    def divide_hand(
        tiles_34: Sequence[int],
        melds: Optional[Collection[Meld]] = None,
    ) -> list[list[list[int]]]:
        """
        Return a list of possible hands.
        :param tiles_34:
        :param melds: list of Meld objects
        :return:
        """
        meld_blocks = HandDivider._melds_to_blocks(melds)
        pure_hand = HandDivider._get_pure_hand(tiles_34, meld_blocks)
        combinations = HandDivider._divide_hand_impl(pure_hand, meld_blocks)
        return [[b.tiles_34 for b in blocks] for blocks in combinations]

    @staticmethod
    def _melds_to_blocks(melds: Optional[Collection[Meld]] = None) -> tuple[_Block, ...]:
        if not melds:
            return ()
        return tuple(_Block.from_meld(m) for m in melds)

    @staticmethod
    def _get_pure_hand(tiles_34: Sequence[int], melds: tuple[_Block, ...]) -> tuple[int, ...]:
        pure_hand_list = list(tiles_34)
        for meld in melds:
            for index in meld.tiles_34:
                pure_hand_list[index] -= 1

        return tuple(pure_hand_list)

    @staticmethod
    @lru_cache(maxsize=128)
    def _divide_hand_impl(pure_hand: tuple[int, ...], melds: tuple[_Block, ...]) -> tuple[_Blocks, ...]:
        hand = list(pure_hand)
        man_combinations = HandDivider._decompose_single_color_hand(hand[0:9], 0)
        pin_combinations = HandDivider._decompose_single_color_hand(hand[9:18], 9)
        sou_combinations = HandDivider._decompose_single_color_hand(hand[18:27], 18)
        honors = HandDivider._decompose_honors_hand(hand[27:34])

        combinations: list[list[_Block]] = []

        chiitoitsu = HandDivider._decompose_chiitoitsu(hand)
        if chiitoitsu:
            combinations.append(chiitoitsu)

        for man in man_combinations:
            for pin in pin_combinations:
                for sou in sou_combinations:
                    all_blocks = [*man, *pin, *sou, *honors]

                    num_pair = sum(block.ty == _BlockType.PAIR for block in all_blocks)
                    if num_pair != 1:
                        continue

                    all_blocks.extend(melds)
                    if len(all_blocks) != 5:
                        continue

                    all_blocks.sort()
                    combinations.append(all_blocks)

        combinations.sort()
        return tuple(tuple(b for b in blocks) for blocks in combinations)

    @staticmethod
    def _decompose_chiitoitsu(pure_hand: list[int]) -> list[_Block]:
        blocks = [_Block(_BlockType.PAIR, i) for i, count in enumerate(pure_hand) if count == 2]
        return blocks if len(blocks) == 7 else []

    @staticmethod
    def _decompose_single_color_hand(single_color_hand: list[int], suit: Literal[0, 9, 18]) -> list[list[_Block]]:
        combinations = HandDivider._decompose_single_color_hand_without_pair(single_color_hand, [], 0, suit)

        if not combinations:
            for pair in range(9):
                if single_color_hand[pair] < 2:
                    continue

                single_color_hand[pair] -= 2
                blocks = [_Block(_BlockType.PAIR, suit + pair)]
                comb = HandDivider._decompose_single_color_hand_without_pair(single_color_hand, blocks, 0, suit)
                single_color_hand[pair] += 2

                if not comb:
                    continue

                combinations.extend(comb)

        return combinations

    @staticmethod
    def _decompose_single_color_hand_without_pair(
        single_color_hand: list[int],
        blocks: list[_Block],
        i: int,
        suit: Literal[0, 9, 18],
    ) -> list[list[_Block]]:
        if i == 9:
            return [blocks] if sum(single_color_hand) == 0 else []

        if single_color_hand[i] == 0:
            return HandDivider._decompose_single_color_hand_without_pair(single_color_hand, blocks, i + 1, suit)

        combinations: list[list[_Block]] = []

        if i < 7 and single_color_hand[i] >= 1 and single_color_hand[i + 1] >= 1 and single_color_hand[i + 2] >= 1:
            single_color_hand[i] -= 1
            single_color_hand[i + 1] -= 1
            single_color_hand[i + 2] -= 1
            new_blocks = [*blocks, _Block(_BlockType.SEQUENCE, suit + i)]
            new_combination = HandDivider._decompose_single_color_hand_without_pair(
                single_color_hand,
                new_blocks,
                i,
                suit,
            )
            combinations.extend(new_combination)
            single_color_hand[i + 2] += 1
            single_color_hand[i + 1] += 1
            single_color_hand[i] += 1

        if single_color_hand[i] >= 3:
            single_color_hand[i] -= 3
            new_blocks = [*blocks, _Block(_BlockType.TRIPLET, suit + i)]
            new_combination = HandDivider._decompose_single_color_hand_without_pair(
                single_color_hand,
                new_blocks,
                i + 1,
                suit,
            )
            combinations.extend(new_combination)
            single_color_hand[i] += 3

        return combinations

    @staticmethod
    def _decompose_honors_hand(honors_hand: list[int]) -> list[_Block]:
        has_pair = False
        blocks: list[_Block] = []
        for i, count in enumerate(honors_hand):
            if count == 0:
                continue
            elif count in (1, 4):
                return []
            elif count == 2:
                if has_pair:
                    return []
                blocks.append(_Block(_BlockType.PAIR, 27 + i))
                has_pair = True
            elif count == 3:
                blocks.append(_Block(_BlockType.TRIPLET, 27 + i))
            else:
                return []

        return blocks
