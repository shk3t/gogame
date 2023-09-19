from __future__ import annotations
from enum import Enum


class OccupiedPointException(Exception):
    def __init__(self, message="This point is already occupied"):
        self.message = message
        super().__init__(self.message)


class StoneColor(int, Enum):
    WHITE = 1
    BLACK = 2


class Group:
    all_groups: list[Group] = []

    def __init__(self, color: StoneColor):
        self.all_groups.append(self)
        self.color = color
        self.member_stones: dict[tuple[int, int], Stone] = {}
        self.frontier_stones: dict[tuple[int, int], Stone] = {}
        self.liberties: set[tuple[int, int]] = set()

    def add(self, x: int, y: int, point: Stone | None):
            if point:
                if point.color == self.color:
                    self.member_stones[(x, y)] = point
                    point.group = self
                else:
                    self.frontier_stones[(x, y)] = point
            else:
                self.liberties.add((x, y))

    def update(self, points: dict[tuple[int, int], Stone | None]):
        for (x, y), point in points.items():
            self.add(x, y, point)

    def __del__(self):
        for group in self.all_groups:
            group.member_stones.clear()
            group.frontier_stones.clear()
            group.liberties.clear()
        self.all_groups.remove(self)

    def __str__(self):
        return "0"

    def __int__(self):
        return 0


class Stone:
    def __init__(self, color: StoneColor | int | str, group: Group | None = None):
        self.color: StoneColor = (
            color
            if isinstance(color, StoneColor)
            else (
                StoneColor(color) if isinstance(color, int) else StoneColor(int(color))
            )
        )
        self.group = group

    def __str__(self):
        return str(self.color.value)

    def __int__(self):
        return int(self.color.value)


class Board:
    all_groups = Group.all_groups

    def __init__(self, x_size: int = 19, y_size: int = 19):
        self.x_size = x_size
        self.y_size = y_size
        self.stones: list[list[Stone | None]] = [
            [None for _ in range(y_size)] for _ in range(x_size)
        ]

    def __getitem__(self, x: int) -> list[Stone | None]:
        return self.stones[x]

    def __str__(self):
        return str([[int(p) if p else 0 for p in col] for col in self.stones])

    def _get_adjacent(self, x: int, y: int) -> dict[tuple[int, int], Stone | None]:
        return {
            (x + dx, y + dy): self.stones[x + dx][y + dy]
            for dx, dy in ((-1, -1), (-1, 1), (1, -1), (1, 1))
        }

    def _clear_groups(self):
        for column in self.stones:
            for stone in column:
                if stone:
                    stone.group = None
        self.all_groups.clear()

    def _estimate_groups(self):
        self._clear_groups()
        for x, column in enumerate(self.stones):
            for y, stone in enumerate(column):
                if stone and not stone.group:
                    new_member_positions = {(x, y)}
                    current_group = Group(stone.color)

                    while new_member_positions:
                        next_member_position = new_member_positions.pop()
                        adjacent = self._get_adjacent(*next_member_position)
                        new_member_positions.update([
                            (x, y)
                            for (x, y), point in adjacent.items()
                            if (x, y) not in current_group.member_stones
                        ])
                        current_group.update(adjacent)

    def make_turn(self, x: int, y: int, stone: Stone) -> bool:
        self[x][y] = stone
        return False

    @staticmethod
    def from_rep(rep: str) -> Board:
        """Format:
        x_size;y_size;<board_rep>

        Where <board_rep> is the sequence of numbers,
        which represents the color of stone on a specific point
        OR vacant point if 0
        OR length of sequence of vacant points if in ().
        Last vacant points can be skipped"""

        x_size, y_size, board_rep = rep.split(";")
        x_size, y_size = int(x_size), int(y_size)
        board = Board(x_size, y_size)

        pos = 0
        left_par_i: int | None = None
        for i, char in enumerate(board_rep):
            if char == "(":
                left_par_i = i
            elif left_par_i is None:
                if char != "0":
                    board[pos // y_size][pos % y_size] = Stone(char)
                pos += 1
            elif char == ")":
                pos += int(board_rep[(left_par_i + 1) : i])
                left_par_i = None

        return board

    def to_rep(self) -> str:
        rep = ""
        zeros_combo = 0
        for column in self.stones:
            for stone in column:
                if stone:
                    rep += (
                        f"({zeros_combo})" if zeros_combo > 3 else ("0" * zeros_combo)
                    ) + str(stone)
                    zeros_combo = 0
                else:
                    zeros_combo += 1
        return f"{self.x_size};{self.y_size};" + rep

    to_rep.__doc__ = from_rep.__doc__


b = Board.from_rep("6;6;02000000000002(13)10002")
print(b.to_rep())
print(b)