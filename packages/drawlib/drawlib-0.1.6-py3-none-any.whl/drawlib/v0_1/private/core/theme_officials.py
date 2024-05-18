from __future__ import annotations
import dataclasses
from typing import Optional, Dict, Tuple, Union, Literal, List
from copy import deepcopy

from drawlib.v0_1.private.core.model import (
    IconStyle,
    ImageStyle,
    LineStyle,
    LineArrowStyle,
    ShapeStyle,
    ShapeTextStyle,
    TextStyle,
)
from drawlib.v0_1.private.core.fonts import (
    FontBase,
    Font,
    FontSourceCode,
)
from drawlib.v0_1.private.core.colors import Colors

#######################
### Official Themes ###
#######################


def get_default() -> _ThemeReturnValue:
    """Change theme to default.

    Returns:
        None

    """

    # https://coolors.co/6d7cc5-70c2bf-e4dfda-d4b483-c1666b

    # primary color
    blue_light = _get_rgba_from_hex("#6D7CC5")
    blue_dark = _get_rgba_from_hex("#12152B")

    # secondary color
    green_light = _get_rgba_from_hex("#70C2BF")
    green_dark = _get_rgba_from_hex("#0C1D1C")

    # third color
    pink_light = _get_rgba_from_hex("#C1666B")
    pink_dark = _get_rgba_from_hex("#1D0C0D")

    default_template = _ThemeTemplate(
        icon_style="thin",
        icon_color=blue_dark,
        line_style="solid",
        line_width=2,
        line_color=blue_dark,
        arrowhead_style="->",
        arrowhead_scale=20,
        shape_line_style="solid",
        shape_line_width=1,
        shape_line_color=blue_dark,
        shape_fill_color=blue_light,
        shapetext_font=Font.SANSSERIF_REGULAR,
        shapetext_size=16,
        shapetext_color=blue_dark,
        text_font=Font.SANSSERIF_REGULAR,
        text_size=16,
        text_color=blue_dark,
    )

    blue_template = default_template.copy()

    green_template = default_template.copy()
    green_template.line_color = green_dark
    green_template.shape_line_color = green_dark
    green_template.shape_fill_color = green_light
    green_template.shapetext_color = green_dark
    green_template.text_color = green_dark

    pink_template = default_template.copy()
    pink_template.line_color = pink_dark
    pink_template.shape_line_color = pink_dark
    pink_template.shape_fill_color = pink_light
    pink_template.shapetext_color = pink_dark
    pink_template.text_color = pink_dark

    default_styles = _generate_styles(default_template)
    named_styles = [
        ("blue", list(_generate_styles(blue_template))),
        ("green", list(_generate_styles(green_template))),
        ("pink", list(_generate_styles(pink_template))),
    ]
    named_styles = _add_special_name_styles(default_styles, named_styles)

    return _ThemeReturnValue(
        backgroundcolor=(255, 255, 255, 1.0),
        sourcecodefont=FontSourceCode.SOURCECODEPRO,
        iconstyle=default_styles[0],
        imagestyle=default_styles[1],
        linestyle=default_styles[2],
        linearrowstyle=default_styles[3],
        shapestyle=default_styles[4],
        shapetextstyle=default_styles[5],
        textstyle=default_styles[6],
        named_styles=named_styles,
    )


def get_gray() -> _ThemeReturnValue:
    """Change theme to gray.

    Returns:
        None

    """

    # https://coolors.co/palette/f8f9fa-e9ecef-dee2e6-ced4da-adb5bd-6c757d-495057-343a40-212529

    # primary color
    gray1 = _get_rgba_from_hex("#ADB5BD")
    gray_dark = _get_rgba_from_hex("#212529")

    # secondary color
    gray2 = _get_rgba_from_hex("#CED4DA")

    # third color
    gray3 = _get_rgba_from_hex("#DEE2E6")

    default_template = _ThemeTemplate(
        icon_style="thin",
        icon_color=gray_dark,
        line_style="solid",
        line_width=2,
        line_color=gray_dark,
        arrowhead_style="->",
        arrowhead_scale=20,
        shape_line_style="solid",
        shape_line_width=1,
        shape_line_color=gray_dark,
        shape_fill_color=gray1,
        shapetext_font=Font.SANSSERIF_REGULAR,
        shapetext_size=16,
        shapetext_color=gray_dark,
        text_font=Font.SANSSERIF_REGULAR,
        text_size=16,
        text_color=gray_dark,
    )

    gray1_template = default_template.copy()
    gray2_template = default_template.copy()
    gray2_template.shape_fill_color = gray2
    gray3_template = default_template.copy()
    gray3_template.shape_fill_color = gray3

    default_styles = _generate_styles(default_template)
    named_styles = [
        ("gray1", list(_generate_styles(gray1_template))),
        ("gray2", list(_generate_styles(gray2_template))),
        ("gray3", list(_generate_styles(gray3_template))),
    ]
    named_styles = _add_special_name_styles(default_styles, named_styles)

    return _ThemeReturnValue(
        backgroundcolor=(255, 255, 255, 1.0),
        sourcecodefont=FontSourceCode.SOURCECODEPRO,
        iconstyle=default_styles[0],
        imagestyle=default_styles[1],
        linestyle=default_styles[2],
        linearrowstyle=default_styles[3],
        shapestyle=default_styles[4],
        shapetextstyle=default_styles[5],
        textstyle=default_styles[6],
        named_styles=named_styles,
    )


############
### Data ###
############


@dataclasses.dataclass
class _ThemeTemplate:
    """Helper dataclass for defining theme styles"""

    def copy(self) -> _ThemeTemplate:
        return deepcopy(self)

    # icon
    icon_style: Literal["thin", "light", "regular", "bold", "fill"]
    icon_color: Union[
        Tuple[float, float, float],
        Tuple[float, float, float, float],
    ]

    # line
    line_style: Literal["solid", "dashed", "dotted", "dashdot"]
    line_width: float
    line_color: Union[
        Tuple[float, float, float],
        Tuple[float, float, float, float],
    ]
    arrowhead_style: Literal[
        "->",
        "<-",
        "<->",
        "-|>",
        "<|-",
        "<|-|>",
    ]
    arrowhead_scale: int

    # shape
    shape_line_style: Literal["solid", "dashed", "dotted", "dashdot"]
    shape_line_width: float
    shape_line_color: Union[
        Tuple[float, float, float],
        Tuple[float, float, float, float],
    ]
    shape_fill_color: Union[
        Tuple[float, float, float],
        Tuple[float, float, float, float],
    ]

    # shapetext
    shapetext_font: FontBase
    shapetext_size: int
    shapetext_color: Union[
        Tuple[float, float, float],
        Tuple[float, float, float, float],
    ]

    # text
    text_font: FontBase
    text_size: int
    text_color: Union[
        Tuple[float, float, float],
        Tuple[float, float, float, float],
    ]


@dataclasses.dataclass
class _ThemeReturnValue:
    backgroundcolor: Tuple[int, int, int, float]
    sourcecodefont: FontSourceCode
    iconstyle: IconStyle
    imagestyle: ImageStyle
    linestyle: LineStyle
    linearrowstyle: LineArrowStyle
    shapestyle: ShapeStyle
    shapetextstyle: ShapeTextStyle
    textstyle: TextStyle

    named_styles: List[
        Tuple[
            str,
            List[
                Union[
                    IconStyle,
                    ImageStyle,
                    LineStyle,
                    LineArrowStyle,
                    ShapeStyle,
                    ShapeTextStyle,
                    TextStyle,
                ]
            ],
        ]
    ]


############
### Util ###
############


def _get_rgba_from_hex(hex_color: str) -> Tuple[int, int, int, float]:
    """
    Convert a hexadecimal color code to RGBA values.

    Args:
        hex_color (str): The hexadecimal color code (e.g., "#FF5733" or "#FFF").

    Returns:
        tuple[int, int, int, float]: A tuple containing the RGBA values (0-255 for R, G, B and 0.0-1.0 for A).
    """

    # Remove the '#' prefix if present
    hex_color = hex_color.lstrip("#")

    # Determine the length of the hex color code
    hex_length = len(hex_color)

    # Convert the hex code to RGB values
    if hex_length == 3:  # Short hex format (#RGB)
        r = int(hex_color[0] * 2, 16)
        g = int(hex_color[1] * 2, 16)
        b = int(hex_color[2] * 2, 16)
        a = 1.0
    elif hex_length in (6, 8):  # Full hex format (#RRGGBB)
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        if hex_length == 8:  # With alpha
            a = int(hex_color[6:8], 16)
        else:
            a = 1.0
    else:
        raise ValueError("Invalid hex color code format")

    return (r, g, b, a)


def _generate_styles(
    template: _ThemeTemplate,
) -> Tuple[IconStyle, ImageStyle, LineStyle, LineArrowStyle, ShapeStyle, ShapeTextStyle, TextStyle]:

    icon = IconStyle(
        style=template.icon_style,
        color=template.icon_color,
        halign="center",
        valign="center",
    )
    image = ImageStyle(
        lwidth=0,
        lstyle=template.shape_line_style,
        lcolor=template.shape_line_color,
        halign="center",
        valign="center",
    )
    line = LineStyle(
        style=template.line_style,
        width=template.line_width,
        color=template.line_color,
    )
    linearrow = LineArrowStyle(
        lstyle=template.line_style,
        lwidth=template.line_width,
        hstyle=template.arrowhead_style,
        hscale=template.arrowhead_scale,
        color=template.line_color,
    )
    shape = ShapeStyle(
        lwidth=template.shape_line_width,
        lstyle=template.shape_line_style,
        lcolor=template.shape_line_color,
        fcolor=template.shape_fill_color,
        halign="center",
        valign="center",
    )
    shapetext = ShapeTextStyle(
        font=template.text_font,
        size=template.text_size,
        color=template.text_color,
        halign="center",
        valign="center",
    )
    text = TextStyle(
        font=template.text_font,
        size=template.text_size,
        color=template.text_color,
        halign="center",
        valign="center",
    )

    return (icon, image, line, linearrow, shape, shapetext, text)


def _add_special_name_styles(
    default_styles: Union[
        IconStyle,
        ImageStyle,
        LineStyle,
        LineArrowStyle,
        ShapeStyle,
        ShapeTextStyle,
        TextStyle,
    ],
    named_styles: List[
        Tuple[
            str,
            List[
                Union[
                    IconStyle,
                    ImageStyle,
                    LineStyle,
                    LineArrowStyle,
                    ShapeStyle,
                    ShapeTextStyle,
                    TextStyle,
                ]
            ],
        ]
    ],
) -> List[
    Tuple[
        str,
        List[
            Union[
                IconStyle,
                ImageStyle,
                LineStyle,
                LineArrowStyle,
                ShapeStyle,
                ShapeTextStyle,
                TextStyle,
            ]
        ],
    ]
]:
    new_named_styles = deepcopy(named_styles)
    default_shapetextstyle = default_styles[5]

    # add white ShapeTextStyle
    if not isinstance(default_shapetextstyle, ShapeTextStyle):
        raise ValueError()
    white_shapetextstyle = default_shapetextstyle.copy()
    white_shapetextstyle.color = Colors.White
    new_named_styles.append(("white", [white_shapetextstyle]))

    # add IconStyle and LineArrowStyle with new names
    for name, styles in named_styles:
        icon, image, line, linearrow, shape, shapetext, text = styles
        if isinstance(icon, IconStyle) and isinstance(shape, ShapeStyle):
            icon_lcolor = icon.copy()
            icon_lcolor.color = shape.lcolor
            icon_fcolor = icon.copy()
            icon_fcolor.color = shape.fcolor
            new_named_styles.append((f"lcolor-{name}", [icon_lcolor]))
            new_named_styles.append((f"fcolor-{name}", [icon_fcolor]))
        else:
            raise ValueError()

        if isinstance(linearrow, LineArrowStyle):
            new_named_styles.append((f"linearrow-{name}", [linearrow]))
        else:
            raise ValueError()

    return new_named_styles
