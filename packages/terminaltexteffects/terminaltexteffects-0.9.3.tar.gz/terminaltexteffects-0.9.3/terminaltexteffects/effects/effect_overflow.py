"""Input text overflows ands scrolls the terminal in a random order until eventually appearing ordered.

Classes:
    Overflow: Input text overflows ands scrolls the terminal in a random order until eventually appearing ordered.
    OverflowConfig: Configuration for the Overflow effect.
    OverflowIterator: Iterates over the effect. Does not normally need to be called directly.
"""

import random
import typing
from dataclasses import dataclass

import terminaltexteffects.utils.argvalidators as argvalidators
from terminaltexteffects.engine.base_character import EffectCharacter
from terminaltexteffects.engine.base_effect import BaseEffect, BaseEffectIterator
from terminaltexteffects.engine.terminal import Terminal
from terminaltexteffects.utils import graphics
from terminaltexteffects.utils.argsdataclass import ArgField, ArgsDataClass, argclass
from terminaltexteffects.utils.geometry import Coord


def get_effect_and_args() -> tuple[type[typing.Any], type[ArgsDataClass]]:
    return Overflow, OverflowConfig


@argclass(
    name="overflow",
    help="Input text overflows ands scrolls the terminal in a random order until eventually appearing ordered.",
    description="overflow | Input text overflows ands scrolls the terminal in a random order until eventually appearing ordered.",
    epilog="""Example: terminaltexteffects overflow --final-gradient-stops 8A008A 00D1FF FFFFFF --final-gradient-steps 12 --overflow-gradient-stops f2ebc0 8dbfb3 f2ebc0 --overflow-cycles-range 2-4 --overflow-speed 3""",
)
@dataclass
class OverflowConfig(ArgsDataClass):
    """Configuration for the Overflow effect.

    Attributes:
        final_gradient_stops (tuple[graphics.Color, ...]): Tuple of colors for the final color gradient. If only one color is provided, the characters will be displayed in that color.
        final_gradient_steps (tuple[int, ...]): Tuple of the number of gradient steps to use. More steps will create a smoother and longer gradient animation. Valid values are n > 0.
        final_gradient_direction (graphics.Gradient.Direction): Direction of the final gradient.
        overflow_gradient_stops (tuple[graphics.Color, ...]): Tuple of colors for the overflow gradient.
        overflow_cycles_range (tuple[int, int]): Lower and upper range of the number of cycles to overflow the text. Valid values are n >= 0.
        overflow_speed (int): Speed of the overflow effect. Valid values are n > 0."""

    final_gradient_stops: tuple[graphics.Color, ...] = ArgField(
        cmd_name=["--final-gradient-stops"],
        type_parser=argvalidators.ColorArg.type_parser,
        nargs="+",
        default=("8A008A", "00D1FF", "FFFFFF"),
        metavar=argvalidators.ColorArg.METAVAR,
        help="Space separated, unquoted, list of colors for the character gradient (applied from bottom to top). If only one color is provided, the characters will be displayed in that color.",
    )  # type: ignore[assignment]
    "tuple[graphics.Color, ...] : Tuple of colors for the final color gradient. If only one color is provided, the characters will be displayed in that color."

    final_gradient_steps: tuple[int, ...] = ArgField(
        cmd_name=["--final-gradient-steps"],
        type_parser=argvalidators.PositiveInt.type_parser,
        nargs="+",
        default=(12,),
        metavar=argvalidators.PositiveInt.METAVAR,
        help="Space separated, unquoted, list of the number of gradient steps to use. More steps will create a smoother and longer gradient animation.",
    )  # type: ignore[assignment]
    "tuple[int, ...] : Tuple of the number of gradient steps to use. More steps will create a smoother and longer gradient animation."

    final_gradient_direction: graphics.Gradient.Direction = ArgField(
        cmd_name="--final-gradient-direction",
        type_parser=argvalidators.GradientDirection.type_parser,
        default=graphics.Gradient.Direction.VERTICAL,
        metavar=argvalidators.GradientDirection.METAVAR,
        help="Direction of the final gradient.",
    )  # type: ignore[assignment]
    "graphics.Gradient.Direction : Direction of the final gradient."

    overflow_gradient_stops: tuple[graphics.Color, ...] = ArgField(
        cmd_name=["--overflow-gradient-stops"],
        type_parser=argvalidators.ColorArg.type_parser,
        nargs="+",
        default=("f2ebc0", "8dbfb3", "f2ebc0"),
        metavar=argvalidators.ColorArg.METAVAR,
        help="Space separated, unquoted, list of colors for the overflow gradient.",
    )  # type: ignore[assignment]
    "tuple[graphics.Color, ...] : Tuple of colors for the overflow gradient."

    overflow_cycles_range: tuple[int, int] = ArgField(
        cmd_name=["--overflow-cycles-range"],
        type_parser=argvalidators.IntRange.type_parser,
        default=(2, 4),
        metavar=argvalidators.IntRange.METAVAR,
        help="Number of cycles to overflow the text.",
    )  # type: ignore[assignment]
    "tuple[int, int] : Lower and upper range of the number of cycles to overflow the text."

    overflow_speed: int = ArgField(
        cmd_name=["--overflow-speed"],
        type_parser=argvalidators.PositiveInt.type_parser,
        default=3,
        metavar=argvalidators.PositiveInt.METAVAR,
        help="Speed of the overflow effect.",
    )  # type: ignore[assignment]
    "int : Speed of the overflow effect."

    @classmethod
    def get_effect_class(cls):
        return Overflow


class OverflowIterator(BaseEffectIterator[OverflowConfig]):
    class Row:
        def __init__(self, characters: list[EffectCharacter], final: bool = False) -> None:
            self.characters = characters
            self.current_index = 0
            self.final = final

        def move_up(self) -> None:
            for character in self.characters:
                current_row = character.motion.current_coord.row
                character.motion.set_coordinate(Coord(character.motion.current_coord.column, current_row + 1))

        def setup(self) -> None:
            for character in self.characters:
                character.motion.set_coordinate(Coord(character.input_coord.column, 0))

        def set_color(self, color: int | str) -> None:
            for character in self.characters:
                character.animation.set_appearance(character.input_symbol, color)

    def __init__(self, effect: "Overflow"):
        super().__init__(effect)
        self.pending_chars: list[EffectCharacter] = []
        self.pending_rows: list[OverflowIterator.Row] = []
        self.active_rows: list[OverflowIterator.Row] = []
        self.character_final_color_map: dict[EffectCharacter, graphics.Color] = {}
        self.build()

    def build(self) -> None:
        final_gradient = graphics.Gradient(*self.config.final_gradient_stops, steps=self.config.final_gradient_steps)
        final_gradient_mapping = final_gradient.build_coordinate_color_mapping(
            self.terminal.output_area.top, self.terminal.output_area.right, self.config.final_gradient_direction
        )
        for character in self.terminal.get_characters(fill_chars=True):
            self.character_final_color_map[character] = final_gradient_mapping[character.input_coord]
        lower_range, upper_range = self.config.overflow_cycles_range
        rows = self.terminal.get_characters_grouped(Terminal.CharacterGroup.ROW_TOP_TO_BOTTOM)
        if upper_range > 0:
            for _ in range(random.randint(lower_range, upper_range)):
                random.shuffle(rows)
                for row in rows:
                    copied_characters = [
                        self.terminal.add_character(character.input_symbol, character.input_coord) for character in row
                    ]
                    self.pending_rows.append(OverflowIterator.Row(copied_characters))
        # add rows in correct order to the end of self.pending_rows
        for row in self.terminal.get_characters_grouped(Terminal.CharacterGroup.ROW_TOP_TO_BOTTOM, fill_chars=True):
            next_row = OverflowIterator.Row(row)
            for character in next_row.characters:
                character.animation.set_appearance(character.symbol, self.character_final_color_map[character])
            next_row.set_color(
                final_gradient.get_color_at_fraction(row[0].input_coord.row / self.terminal.output_area.top)
            )
            self.pending_rows.append(OverflowIterator.Row(row, final=True))
        self._delay = 0
        self._overflow_gradient = graphics.Gradient(
            *self.config.overflow_gradient_stops,
            steps=max((self.terminal.output_area.top // max(1, len(self.config.overflow_gradient_stops) - 1)), 1),
        )

    def __next__(self) -> str:
        if self.pending_rows:
            if not self._delay:
                for _ in range(random.randint(1, self.config.overflow_speed)):
                    if self.pending_rows:
                        for row in self.active_rows:
                            row.move_up()
                            if not row.final:
                                row.set_color(
                                    self._overflow_gradient.spectrum[
                                        min(
                                            row.characters[0].motion.current_coord.row,
                                            len(self._overflow_gradient.spectrum) - 1,
                                        )
                                    ]
                                )
                        next_row = self.pending_rows.pop(0)
                        next_row.setup()
                        next_row.move_up()
                        if not next_row.final:
                            next_row.set_color(self._overflow_gradient.spectrum[0])
                        for character in next_row.characters:
                            self.terminal.set_character_visibility(character, True)
                        self.active_rows.append(next_row)
                self._delay = random.randint(0, 3)

            else:
                self._delay -= 1
            self.active_rows = [
                row
                for row in self.active_rows
                if row.characters[0].motion.current_coord.row <= self.terminal.output_area.top
            ]
            self.update()
            return self.frame
        else:
            raise StopIteration


class Overflow(BaseEffect[OverflowConfig]):
    """Input text overflows ands scrolls the terminal in a random order until eventually appearing ordered.

    Attributes:
        effect_config (OverflowConfig): Configuration for the effect.
        terminal_config (TerminalConfig): Configuration for the terminal.
    """

    _config_cls = OverflowConfig
    _iterator_cls = OverflowIterator

    def __init__(self, input_data: str) -> None:
        """Initialize the effect with the provided input data.

        Args:
            input_data (str): The input data to use for the effect."""
        super().__init__(input_data)
