from collections.abc import Collection, Sequence
from dataclasses import dataclass
from enum import IntEnum
from functools import lru_cache
from typing import Literal

from mahjong.meld import Meld


class _BlockType(IntEnum):
    QUAD = 0
    TRIPLET = 1
    PAIR = 2
    SEQUENCE = 3


@dataclass(frozen=True, order=True)
class _Block:
    tile_34: int
    ty: _BlockType

    @classmethod
    def from_meld(cls, meld: Meld) -> "_Block":
        tile_34 = meld.tiles_34[0]
        match meld.type:
            case Meld.CHI:
                return cls(tile_34, _BlockType.SEQUENCE)
            case Meld.PON:
                return cls(tile_34, _BlockType.TRIPLET)
            case Meld.KAN | Meld.SHOUMINKAN:
                return cls(tile_34, _BlockType.QUAD)
            case _:
                msg = f"invalid meld type: {meld.type}, tiles: {meld.tiles_34}"
                raise RuntimeError(msg)

    @property
    def tiles_34(self) -> list[int]:
        match self.ty:
            case _BlockType.QUAD:
                return [self.tile_34, self.tile_34, self.tile_34, self.tile_34]
            case _BlockType.TRIPLET:
                return [self.tile_34, self.tile_34, self.tile_34]
            case _BlockType.PAIR:
                return [self.tile_34, self.tile_34]
            case _BlockType.SEQUENCE:
                return [self.tile_34, self.tile_34 + 1, self.tile_34 + 2]


_Blocks = tuple[_Block, ...]


class HandDivider:
    """
    Decompose a winning hand into all possible block combinations.

    A valid combination consists of 4 melds (sequences, triplets, or quads) plus 1 pair.
    Chiitoitsu (seven pairs) is also recognized when no melds are declared.
    Multiple valid decompositions may exist for the same hand.

    Each decomposition is a list of blocks, where each block is a list of tile indices
    in 34-format:

    - pair: ``[tile, tile]`` (length 2)
    - triplet: ``[tile, tile, tile]`` (length 3, identical tiles)
    - sequence: ``[tile, tile+1, tile+2]`` (length 3, consecutive tiles)
    - quad: ``[tile, tile, tile, tile]`` (length 4, identical tiles)
    """

    @staticmethod
    def divide_hand(
        tiles_34: Sequence[int],
        melds: Collection[Meld] | None = None,
    ) -> list[list[list[int]]]:
        """
        Return all valid decompositions of the hand into blocks.

        Decompose the full hand (including any declared melds) into every possible
        combination of 4 melds + 1 pair, or 7 pairs (chiitoitsu, only when no melds
        are declared).

        Single decomposition (one triplet, three sequences, and a pair):

        >>> from mahjong.hand_calculating.divider import HandDivider
        >>> from mahjong.tile import TilesConverter
        >>> tiles_34 = TilesConverter.one_line_string_to_34_array("234567m23455s777z")
        >>> result = HandDivider.divide_hand(tiles_34)
        >>> result
        [[[1, 2, 3], [4, 5, 6], [19, 20, 21], [22, 22], [33, 33, 33]]]

        Multiple decompositions (triplets vs. sequences):

        >>> tiles_34 = TilesConverter.one_line_string_to_34_array("11122233388899m")
        >>> result = HandDivider.divide_hand(tiles_34)
        >>> result
        [[[0, 0, 0], [1, 1, 1], [2, 2, 2], [7, 7, 7], [8, 8]], [[0, 1, 2], [0, 1, 2], [0, 1, 2], [7, 7, 7], [8, 8]]]

        Hands with declared melds:

        >>> from mahjong.meld import Meld
        >>> tiles_34 = TilesConverter.string_to_34_array(pin="234777888999", honors="22")
        >>> chi_1 = Meld(meld_type=Meld.CHI, tiles=TilesConverter.string_to_136_array(pin="789"))
        >>> chi_2 = Meld(meld_type=Meld.CHI, tiles=TilesConverter.string_to_136_array(pin="234"))
        >>> result = HandDivider.divide_hand(tiles_34, [chi_1, chi_2])
        >>> result
        [[[10, 11, 12], [15, 16, 17], [15, 16, 17], [15, 16, 17], [28, 28]]]

        Invalid hands return an empty list:

        >>> HandDivider.divide_hand([5] * 34)
        []

        :param tiles_34: hand in 34-format count array (length 34), including tiles from melds
        :param melds: declared melds (:class:`~mahjong.meld.Meld` objects); their tiles are
            subtracted from ``tiles_34`` before decomposing the concealed portion
        :return: list of decompositions, where each decomposition is a list of blocks
            (each block is a list of tile indices in 34-format)
        """
        if not HandDivider._validate_tiles(tiles_34):
            return []

        meld_blocks = HandDivider._melds_to_blocks(melds)
        pure_hand = HandDivider._get_pure_hand(tiles_34, meld_blocks)
        combinations = HandDivider._divide_hand_impl(pure_hand, meld_blocks)
        return [[b.tiles_34 for b in blocks] for blocks in combinations]

    @staticmethod
    def _validate_tiles(tiles_34: Sequence[int]) -> bool:
        return all(0 <= count <= 4 for count in tiles_34)

    @staticmethod
    def _melds_to_blocks(melds: Collection[Meld] | None = None) -> tuple[_Block, ...]:
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

        if not melds and (chiitoitsu := HandDivider._decompose_chiitoitsu(hand)):
            combinations.append(chiitoitsu)

        for man in man_combinations:
            for pin in pin_combinations:
                for sou in sou_combinations:
                    # For invalid suits, *_combinations will be [] and the loop will not be executed.
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
        return tuple(tuple(blocks) for blocks in combinations)

    @staticmethod
    def _decompose_chiitoitsu(pure_hand: list[int]) -> list[_Block]:
        if any(count not in {0, 2} for count in pure_hand):
            return []

        blocks = [_Block(i, _BlockType.PAIR) for i, count in enumerate(pure_hand) if count == 2]
        return blocks if len(blocks) == 7 else []

    @staticmethod
    def _decompose_single_color_hand(single_color_hand: list[int], suit: Literal[0, 9, 18]) -> list[list[_Block]]:
        remaining = sum(single_color_hand)
        combinations = HandDivider._decompose_single_color_hand_without_pair(single_color_hand, [], 0, suit, remaining)

        if not combinations:
            for pair in range(9):
                if single_color_hand[pair] < 2:
                    continue

                single_color_hand[pair] -= 2
                blocks = [_Block(suit + pair, _BlockType.PAIR)]
                comb = HandDivider._decompose_single_color_hand_without_pair(
                    single_color_hand,
                    blocks,
                    0,
                    suit,
                    remaining - 2,
                )
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
        remaining: int,
    ) -> list[list[_Block]]:
        if i == 9:
            # If there is no tile of the target suits, returns [[]].
            # If there are any tiles remaining, it returns [].
            return [blocks] if remaining == 0 else []

        if single_color_hand[i] == 0:
            return HandDivider._decompose_single_color_hand_without_pair(
                single_color_hand,
                blocks,
                i + 1,
                suit,
                remaining,
            )

        combinations: list[list[_Block]] = []

        if i < 7 and single_color_hand[i] >= 1 and single_color_hand[i + 1] >= 1 and single_color_hand[i + 2] >= 1:
            single_color_hand[i] -= 1
            single_color_hand[i + 1] -= 1
            single_color_hand[i + 2] -= 1
            new_blocks = [*blocks, _Block(suit + i, _BlockType.SEQUENCE)]
            new_combination = HandDivider._decompose_single_color_hand_without_pair(
                single_color_hand,
                new_blocks,
                i,
                suit,
                remaining - 3,
            )
            combinations.extend(new_combination)
            single_color_hand[i + 2] += 1
            single_color_hand[i + 1] += 1
            single_color_hand[i] += 1

        if single_color_hand[i] >= 3:
            single_color_hand[i] -= 3
            new_blocks = [*blocks, _Block(suit + i, _BlockType.TRIPLET)]
            new_combination = HandDivider._decompose_single_color_hand_without_pair(
                single_color_hand,
                new_blocks,
                i + 1,  # The triplet is extracted only once.
                suit,
                remaining - 3,
            )
            combinations.extend(new_combination)
            single_color_hand[i] += 3

        # If single_color_hand[i] is an invalid number (not empty, not a triplet, not a sequence),
        # [] is returned immediately.
        return combinations

    @staticmethod
    def _decompose_honors_hand(honors_hand: list[int]) -> list[_Block]:
        has_pair = False
        blocks: list[_Block] = []
        for i, count in enumerate(honors_hand):
            match count:
                case 0:
                    continue
                case 2:
                    if has_pair:
                        return []
                    blocks.append(_Block(27 + i, _BlockType.PAIR))
                    has_pair = True
                case 3:
                    blocks.append(_Block(27 + i, _BlockType.TRIPLET))
                case _:
                    return []

        return blocks
