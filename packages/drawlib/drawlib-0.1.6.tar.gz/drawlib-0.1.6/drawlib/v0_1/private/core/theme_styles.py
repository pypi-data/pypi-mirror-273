from typing import Dict, Tuple, List, Union
from drawlib.v0_1.private.util import error_handler
from drawlib.v0_1.private.core.model import (
    IconStyle,
    ImageStyle,
    LineStyle,
    LineArrowStyle,
    ShapeStyle,
    ShapeTextStyle,
    TextStyle,
)
from drawlib.v0_1.private.core.fonts import FontSourceCode
import drawlib.v0_1.private.validators.color as color_validator
import drawlib.v0_1.private.validators.style as style_validator
import drawlib.v0_1.private.validators.types as type_validator

list_ = list


class BackgroundColors:
    def __init__(self) -> None:
        self._colors: Dict[str, Tuple[int, int, int, float]] = dict()

    @error_handler
    def has(self, name: str) -> bool:
        """Whether having theme name or not"""
        return name in self._colors

    @error_handler
    def get(self, name: str = "") -> Tuple[int, int, int, float]:
        if not self.has(name):
            raise ValueError(f'Theme background-color name "' + name + '" does not exist.')
        return self._colors[name]

    @error_handler
    def list(self) -> List[str]:
        return list_(self._colors.keys())

    @error_handler
    def set(
        self,
        color: Union[Tuple[int, int, int], Tuple[int, int, int, float]],
        name: str = "",
    ) -> None:
        color_validator.validate_color("color", color)
        type_validator.validate_str("name", name)
        if len(color) == 3:
            color = (color[0], color[1], color[2], 1.0)
        self._colors[name] = color

    @error_handler
    def delete(self, name: str) -> None:
        if not self.has(name):
            raise ValueError(f'Theme background-color name "' + name + '" does not exist.')
        del self._colors[name]


class SourceCodeFonts:
    def __init__(self) -> None:
        self._fonts: Dict[str, SourceCodeFonts] = dict()

    @error_handler
    def has(self, name: str) -> bool:
        """Whether having theme name or not"""
        return name in self._fonts

    @error_handler
    def get(self, name: str = "") -> FontSourceCode:
        if not self.has(name):
            raise ValueError(f'Theme sourcecode-font name "' + name + '" does not exist.')
        return self._fonts[name]

    @error_handler
    def list(self) -> List[str]:
        return list_(self._fonts.keys())

    @error_handler
    def set(
        self,
        font: FontSourceCode,
        name: str = "",
    ) -> None:
        if not isinstance(font, FontSourceCode):
            raise ValueError("Arg font must be FontSourceCode.")
        type_validator.validate_str("name", name)

        self._fonts[name] = font

    @error_handler
    def delete(self, name: str) -> None:
        if not self.has(name):
            raise ValueError(f'Theme sourcecode-font name "' + name + '" does not exist.')
        del self._fonts[name]


class IconStyles:
    def __init__(self) -> None:
        self._styles: Dict[str, IconStyle] = dict()

    @error_handler
    def has(self, name: str) -> bool:
        """Whether having theme name or not"""
        return name in self._styles

    @error_handler
    def get(self, name: str = "") -> IconStyle:
        if not self.has(name):
            raise ValueError(f'Theme style name "' + name + '" does not exist.')
        return self._styles[name].copy()

    @error_handler
    def list(self) -> List[str]:
        return list_(self._styles.keys())

    @error_handler
    def set(self, style: IconStyle, name: str = "") -> None:
        style_validator.validate_iconstyle("style", style)
        type_validator.validate_str("name", name)
        self._styles[name] = style.copy()

    @error_handler
    def delete(self, name: str) -> None:
        if not self.has(name):
            raise ValueError(f'Theme style name "' + name + '" does not exist.')
        del self._styles[name]


class ImageStyles:
    def __init__(self) -> None:
        self._styles: Dict[str, ImageStyle] = dict()

    @error_handler
    def has(self, name: str) -> bool:
        """Whether having theme name or not"""
        return name in self._styles

    @error_handler
    def get(self, name: str = "") -> ImageStyle:
        if not self.has(name):
            raise ValueError(f'Theme style name "' + name + '" does not exist.')
        return self._styles[name].copy()

    @error_handler
    def list(self) -> List[str]:
        return list_(self._styles.keys())

    @error_handler
    def set(self, style: ImageStyle, name: str = "") -> None:
        style_validator.validate_imagestyle("style", style)
        type_validator.validate_str("name", name)
        self._styles[name] = style.copy()

    @error_handler
    def delete(self, name: str) -> None:
        if not self.has(name):
            raise ValueError(f'Theme style name "' + name + '" does not exist.')
        del self._styles[name]


class LineStyles:
    def __init__(self) -> None:
        self._styles: Dict[str, LineStyle] = dict()

    @error_handler
    def has(self, name: str) -> bool:
        """Whether having theme name or not"""
        return name in self._styles

    @error_handler
    def get(self, name: str = "") -> LineStyle:
        if not self.has(name):
            raise ValueError(f'Theme style name "' + name + '" does not exist.')
        return self._styles[name].copy()

    @error_handler
    def list(self) -> List[str]:
        return list_(self._styles.keys())

    @error_handler
    def set(self, style: LineStyle, name: str = "") -> None:
        style_validator.validate_linestyle("style", style)
        type_validator.validate_str("name", name)
        self._styles[name] = style.copy()

    @error_handler
    def delete(self, name: str) -> None:
        if not self.has(name):
            raise ValueError(f'Theme style name "' + name + '" does not exist.')
        del self._styles[name]


class LineArrowStyles:
    def __init__(self) -> None:
        self._styles: Dict[str, LineArrowStyle] = dict()

    @error_handler
    def has(self, name: str) -> bool:
        """Whether having theme name or not"""
        return name in self._styles

    @error_handler
    def get(self, name: str = "") -> LineArrowStyle:
        if not self.has(name):
            raise ValueError(f'Theme style name "' + name + '" does not exist.')
        return self._styles[name].copy()

    @error_handler
    def list(self) -> List[str]:
        return list_(self._styles.keys())

    @error_handler
    def set(self, style: LineArrowStyle, name: str = "") -> None:
        style_validator.validate_linearrowstyle("style", style)
        type_validator.validate_str("name", name)
        self._styles[name] = style.copy()

    @error_handler
    def delete(self, name: str) -> None:
        if not self.has(name):
            raise ValueError(f'Theme style name "' + name + '" does not exist.')
        del self._styles[name]


class ShapeStyles:
    def __init__(self) -> None:
        self._styles: Dict[str, ShapeStyle] = dict()

    @error_handler
    def has(self, name: str) -> bool:
        """Whether having theme name or not"""
        return name in self._styles

    @error_handler
    def get(self, name: str = "") -> ShapeStyle:
        if not self.has(name):
            raise ValueError(f'Theme style name "' + name + '" does not exist.')
        return self._styles[name].copy()

    @error_handler
    def list(self) -> List[str]:
        return list_(self._styles.keys())

    @error_handler
    def set(self, style: ShapeStyle, name: str = "") -> None:
        style_validator.validate_shapestyle("style", style)
        type_validator.validate_str("name", name)
        self._styles[name] = style.copy()

    @error_handler
    def delete(self, name: str) -> None:
        if not self.has(name):
            raise ValueError(f'Theme style name "' + name + '" does not exist.')
        del self._styles[name]


class ShapeTextStyles:
    def __init__(self) -> None:
        self._styles: Dict[str, ShapeTextStyle] = dict()

    @error_handler
    def has(self, name: str) -> bool:
        """Whether having theme name or not"""
        return name in self._styles

    @error_handler
    def get(self, name: str = "") -> ShapeTextStyle:
        if not self.has(name):
            raise ValueError(f'Theme style name "' + name + '" does not exist.')
        return self._styles[name].copy()

    @error_handler
    def list(self) -> List[str]:
        return list_(self._styles.keys())

    @error_handler
    def set(self, style: ShapeTextStyle, name: str = "") -> None:
        style_validator.validate_shapetextstyle("style", style)
        type_validator.validate_str("name", name)
        self._styles[name] = style.copy()

    @error_handler
    def delete(self, name: str) -> None:
        if not self.has(name):
            raise ValueError(f'Theme style name "' + name + '" does not exist.')
        del self._styles[name]


class TextStyles:
    def __init__(self) -> None:
        self._styles: Dict[str, TextStyle] = dict()

    @error_handler
    def has(self, name: str) -> bool:
        """Whether having theme name or not"""
        return name in self._styles

    @error_handler
    def get(self, name: str = "") -> TextStyle:
        if not self.has(name):
            raise ValueError(f'Theme style name "' + name + '" does not exist.')
        return self._styles[name].copy()

    @error_handler
    def list(self) -> List[str]:
        return list_(self._styles.keys())

    @error_handler
    def set(self, style: TextStyle, name: str = "") -> None:
        style_validator.validate_textstyle("style", style)
        type_validator.validate_str("name", name)
        self._styles[name] = style.copy()

    @error_handler
    def delete(self, name: str) -> None:
        if not self.has(name):
            raise ValueError(f'Theme style name "' + name + '" does not exist.')
        del self._styles[name]


class ArcStyles:
    def __init__(self, shapestyles: ShapeStyles) -> None:
        self._styles: Dict[str, ShapeStyle] = dict()
        self._shapestyles = shapestyles

    @error_handler
    def has(self, name: str) -> bool:
        """Whether having theme name or not"""
        return name in self._styles

    @error_handler
    def get(self, name: str = "", use_shapestyles_if_not_exist: bool = True) -> ShapeStyle:
        if self.has(name):
            return self._styles[name].copy()
        if not use_shapestyles_if_not_exist:
            raise ValueError(f'Theme style name "' + name + '" does not exist.')
        return self._shapestyles.get(name)

    @error_handler
    def list(self) -> List[str]:
        return list_(self._styles.keys())

    @error_handler
    def set(self, style: ShapeStyle, name: str = "") -> None:
        style_validator.validate_shapestyle("style", style)
        type_validator.validate_str("name", name)
        self._styles[name] = style.copy()

    @error_handler
    def delete(self, name: str) -> None:
        if not self.has(name):
            raise ValueError(f'Theme style name "' + name + '" does not exist.')
        del self._styles[name]


class CircleStyles:
    def __init__(self, shapestyles: ShapeStyles) -> None:
        self._styles: Dict[str, ShapeStyle] = dict()
        self._shapestyles = shapestyles

    @error_handler
    def has(self, name: str) -> bool:
        """Whether having theme name or not"""
        return name in self._styles

    @error_handler
    def get(self, name: str = "", use_shapestyles_if_not_exist: bool = True) -> ShapeStyle:
        if self.has(name):
            return self._styles[name].copy()
        if not use_shapestyles_if_not_exist:
            raise ValueError(f'Theme style name "' + name + '" does not exist.')
        return self._shapestyles.get(name)

    @error_handler
    def list(self) -> List[str]:
        return list_(self._styles.keys())

    @error_handler
    def set(self, style: ShapeStyle, name: str = "") -> None:
        style_validator.validate_shapestyle("style", style)
        type_validator.validate_str("name", name)
        self._styles[name] = style.copy()

    @error_handler
    def delete(self, name: str) -> None:
        if not self.has(name):
            raise ValueError(f'Theme style name "' + name + '" does not exist.')
        del self._styles[name]


class DonutsStyles:
    def __init__(self, shapestyles: ShapeStyles) -> None:
        self._styles: Dict[str, ShapeStyle] = dict()
        self._shapestyles = shapestyles

    @error_handler
    def has(self, name: str) -> bool:
        """Whether having theme name or not"""
        return name in self._styles

    @error_handler
    def get(self, name: str = "", use_shapestyles_if_not_exist: bool = True) -> ShapeStyle:
        if self.has(name):
            return self._styles[name].copy()
        if not use_shapestyles_if_not_exist:
            raise ValueError(f'Theme style name "' + name + '" does not exist.')
        return self._shapestyles.get(name)

    @error_handler
    def list(self) -> List[str]:
        return list_(self._styles.keys())

    @error_handler
    def set(self, style: ShapeStyle, name: str = "") -> None:
        style_validator.validate_shapestyle("style", style)
        type_validator.validate_str("name", name)
        self._styles[name] = style.copy()

    @error_handler
    def delete(self, name: str) -> None:
        if not self.has(name):
            raise ValueError(f'Theme style name "' + name + '" does not exist.')
        del self._styles[name]


class EllipseStyles:
    def __init__(self, shapestyles: ShapeStyles) -> None:
        self._styles: Dict[str, ShapeStyle] = dict()
        self._shapestyles = shapestyles

    @error_handler
    def has(self, name: str) -> bool:
        """Whether having theme name or not"""
        return name in self._styles

    @error_handler
    def get(self, name: str = "", use_shapestyles_if_not_exist: bool = True) -> ShapeStyle:
        if self.has(name):
            return self._styles[name].copy()
        if not use_shapestyles_if_not_exist:
            raise ValueError(f'Theme style name "' + name + '" does not exist.')
        return self._shapestyles.get(name)

    @error_handler
    def list(self) -> List[str]:
        return list_(self._styles.keys())

    @error_handler
    def set(self, style: ShapeStyle, name: str = "") -> None:
        style_validator.validate_shapestyle("style", style)
        type_validator.validate_str("name", name)
        self._styles[name] = style.copy()

    @error_handler
    def delete(self, name: str) -> None:
        if not self.has(name):
            raise ValueError(f'Theme style name "' + name + '" does not exist.')
        del self._styles[name]


class FanStyles:
    def __init__(self, shapestyles: ShapeStyles) -> None:
        self._styles: Dict[str, ShapeStyle] = dict()
        self._shapestyles = shapestyles

    @error_handler
    def has(self, name: str) -> bool:
        """Whether having theme name or not"""
        return name in self._styles

    @error_handler
    def get(self, name: str = "", use_shapestyles_if_not_exist: bool = True) -> ShapeStyle:
        if self.has(name):
            return self._styles[name].copy()
        if not use_shapestyles_if_not_exist:
            raise ValueError(f'Theme style name "' + name + '" does not exist.')
        return self._shapestyles.get(name)

    @error_handler
    def list(self) -> List[str]:
        return list_(self._styles.keys())

    @error_handler
    def set(self, style: ShapeStyle, name: str = "") -> None:
        style_validator.validate_shapestyle("style", style)
        type_validator.validate_str("name", name)
        self._styles[name] = style.copy()

    @error_handler
    def delete(self, name: str) -> None:
        if not self.has(name):
            raise ValueError(f'Theme style name "' + name + '" does not exist.')
        del self._styles[name]


class PolygonStyles:
    def __init__(self, shapestyles: ShapeStyles) -> None:
        self._styles: Dict[str, ShapeStyle] = dict()
        self._shapestyles = shapestyles

    @error_handler
    def has(self, name: str) -> bool:
        """Whether having theme name or not"""
        return name in self._styles

    @error_handler
    def get(self, name: str = "", use_shapestyles_if_not_exist: bool = True) -> ShapeStyle:
        if self.has(name):
            return self._styles[name].copy()
        if not use_shapestyles_if_not_exist:
            raise ValueError(f'Theme style name "' + name + '" does not exist.')
        return self._shapestyles.get(name)

    @error_handler
    def list(self) -> List[str]:
        return list_(self._styles.keys())

    @error_handler
    def set(self, style: ShapeStyle, name: str = "") -> None:
        style_validator.validate_shapestyle("style", style)
        type_validator.validate_str("name", name)
        self._styles[name] = style.copy()

    @error_handler
    def delete(self, name: str) -> None:
        if not self.has(name):
            raise ValueError(f'Theme style name "' + name + '" does not exist.')
        del self._styles[name]


class RectangleStyles:
    def __init__(self, shapestyles: ShapeStyles) -> None:
        self._styles: Dict[str, ShapeStyle] = dict()
        self._shapestyles = shapestyles

    @error_handler
    def has(self, name: str) -> bool:
        """Whether having theme name or not"""
        return name in self._styles

    @error_handler
    def get(self, name: str = "", use_shapestyles_if_not_exist: bool = True) -> ShapeStyle:
        if self.has(name):
            return self._styles[name].copy()
        if not use_shapestyles_if_not_exist:
            raise ValueError(f'Theme style name "' + name + '" does not exist.')
        return self._shapestyles.get(name)

    @error_handler
    def list(self) -> List[str]:
        return list_(self._styles.keys())

    @error_handler
    def set(self, style: ShapeStyle, name: str = "") -> None:
        style_validator.validate_shapestyle("style", style)
        type_validator.validate_str("name", name)
        self._styles[name] = style.copy()

    @error_handler
    def delete(self, name: str) -> None:
        if not self.has(name):
            raise ValueError(f'Theme style name "' + name + '" does not exist.')
        del self._styles[name]


class RegularpolygonStyles:
    def __init__(self, shapestyles: ShapeStyles) -> None:
        self._styles: Dict[str, ShapeStyle] = dict()
        self._shapestyles = shapestyles

    @error_handler
    def has(self, name: str) -> bool:
        """Whether having theme name or not"""
        return name in self._styles

    @error_handler
    def get(self, name: str = "", use_shapestyles_if_not_exist: bool = True) -> ShapeStyle:
        if self.has(name):
            return self._styles[name].copy()
        if not use_shapestyles_if_not_exist:
            raise ValueError(f'Theme style name "' + name + '" does not exist.')
        return self._shapestyles.get(name)

    @error_handler
    def list(self) -> List[str]:
        return list_(self._styles.keys())

    @error_handler
    def set(self, style: ShapeStyle, name: str = "") -> None:
        style_validator.validate_shapestyle("style", style)
        type_validator.validate_str("name", name)
        self._styles[name] = style.copy()

    @error_handler
    def delete(self, name: str) -> None:
        if not self.has(name):
            raise ValueError(f'Theme style name "' + name + '" does not exist.')
        del self._styles[name]


class WedgeStyles:
    def __init__(self, shapestyles: ShapeStyles) -> None:
        self._styles: Dict[str, ShapeStyle] = dict()
        self._shapestyles = shapestyles

    @error_handler
    def has(self, name: str) -> bool:
        """Whether having theme name or not"""
        return name in self._styles

    @error_handler
    def get(self, name: str = "", use_shapestyles_if_not_exist: bool = True) -> ShapeStyle:
        if self.has(name):
            return self._styles[name].copy()
        if not use_shapestyles_if_not_exist:
            raise ValueError(f'Theme style name "' + name + '" does not exist.')
        return self._shapestyles.get(name)

    @error_handler
    def list(self) -> List[str]:
        return list_(self._styles.keys())

    @error_handler
    def set(self, style: ShapeStyle, name: str = "") -> None:
        style_validator.validate_shapestyle("style", style)
        type_validator.validate_str("name", name)
        self._styles[name] = style.copy()

    @error_handler
    def delete(self, name: str) -> None:
        if not self.has(name):
            raise ValueError(f'Theme style name "' + name + '" does not exist.')
        del self._styles[name]


class ArrowStyles:
    def __init__(self, shapestyles: ShapeStyles) -> None:
        self._styles: Dict[str, ShapeStyle] = dict()
        self._shapestyles = shapestyles

    @error_handler
    def has(self, name: str) -> bool:
        """Whether having theme name or not"""
        return name in self._styles

    @error_handler
    def get(self, name: str = "", use_shapestyles_if_not_exist: bool = True) -> ShapeStyle:
        if self.has(name):
            return self._styles[name].copy()
        if not use_shapestyles_if_not_exist:
            raise ValueError(f'Theme style name "' + name + '" does not exist.')
        return self._shapestyles.get(name)

    @error_handler
    def list(self) -> List[str]:
        return list_(self._styles.keys())

    @error_handler
    def set(self, style: ShapeStyle, name: str = "") -> None:
        style_validator.validate_shapestyle("style", style)
        type_validator.validate_str("name", name)
        self._styles[name] = style.copy()

    @error_handler
    def delete(self, name: str) -> None:
        if not self.has(name):
            raise ValueError(f'Theme style name "' + name + '" does not exist.')
        del self._styles[name]


class ChevronStyles:
    def __init__(self, shapestyles: ShapeStyles) -> None:
        self._styles: Dict[str, ShapeStyle] = dict()
        self._shapestyles = shapestyles

    @error_handler
    def has(self, name: str) -> bool:
        """Whether having theme name or not"""
        return name in self._styles

    @error_handler
    def get(self, name: str = "", use_shapestyles_if_not_exist: bool = True) -> ShapeStyle:
        if self.has(name):
            return self._styles[name].copy()
        if not use_shapestyles_if_not_exist:
            raise ValueError(f'Theme style name "' + name + '" does not exist.')
        return self._shapestyles.get(name)

    @error_handler
    def list(self) -> List[str]:
        return list_(self._styles.keys())

    @error_handler
    def set(self, style: ShapeStyle, name: str = "") -> None:
        style_validator.validate_shapestyle("style", style)
        type_validator.validate_str("name", name)
        self._styles[name] = style.copy()

    @error_handler
    def delete(self, name: str) -> None:
        if not self.has(name):
            raise ValueError(f'Theme style name "' + name + '" does not exist.')
        del self._styles[name]


class ParallelogramStyles:
    def __init__(self, shapestyles: ShapeStyles) -> None:
        self._styles: Dict[str, ShapeStyle] = dict()
        self._shapestyles = shapestyles

    @error_handler
    def has(self, name: str) -> bool:
        """Whether having theme name or not"""
        return name in self._styles

    @error_handler
    def get(self, name: str = "", use_shapestyles_if_not_exist: bool = True) -> ShapeStyle:
        if self.has(name):
            return self._styles[name].copy()
        if not use_shapestyles_if_not_exist:
            raise ValueError(f'Theme style name "' + name + '" does not exist.')
        return self._shapestyles.get(name)

    @error_handler
    def list(self) -> List[str]:
        return list_(self._styles.keys())

    @error_handler
    def set(self, style: ShapeStyle, name: str = "") -> None:
        style_validator.validate_shapestyle("style", style)
        type_validator.validate_str("name", name)
        self._styles[name] = style.copy()

    @error_handler
    def delete(self, name: str) -> None:
        if not self.has(name):
            raise ValueError(f'Theme style name "' + name + '" does not exist.')
        del self._styles[name]


class RhombusStyles:
    def __init__(self, shapestyles: ShapeStyles) -> None:
        self._styles: Dict[str, ShapeStyle] = dict()
        self._shapestyles = shapestyles

    @error_handler
    def has(self, name: str) -> bool:
        """Whether having theme name or not"""
        return name in self._styles

    @error_handler
    def get(self, name: str = "", use_shapestyles_if_not_exist: bool = True) -> ShapeStyle:
        if self.has(name):
            return self._styles[name].copy()
        if not use_shapestyles_if_not_exist:
            raise ValueError(f'Theme style name "' + name + '" does not exist.')
        return self._shapestyles.get(name)

    @error_handler
    def list(self) -> List[str]:
        return list_(self._styles.keys())

    @error_handler
    def set(self, style: ShapeStyle, name: str = "") -> None:
        style_validator.validate_shapestyle("style", style)
        type_validator.validate_str("name", name)
        self._styles[name] = style.copy()

    @error_handler
    def delete(self, name: str) -> None:
        if not self.has(name):
            raise ValueError(f'Theme style name "' + name + '" does not exist.')
        del self._styles[name]


class StarStyles:
    def __init__(self, shapestyles: ShapeStyles) -> None:
        self._styles: Dict[str, ShapeStyle] = dict()
        self._shapestyles = shapestyles

    @error_handler
    def has(self, name: str) -> bool:
        """Whether having theme name or not"""
        return name in self._styles

    @error_handler
    def get(self, name: str = "", use_shapestyles_if_not_exist: bool = True) -> ShapeStyle:
        if self.has(name):
            return self._styles[name].copy()
        if not use_shapestyles_if_not_exist:
            raise ValueError(f'Theme style name "' + name + '" does not exist.')
        return self._shapestyles.get(name)

    @error_handler
    def list(self) -> List[str]:
        return list_(self._styles.keys())

    @error_handler
    def set(self, style: ShapeStyle, name: str = "") -> None:
        style_validator.validate_shapestyle("style", style)
        type_validator.validate_str("name", name)
        self._styles[name] = style.copy()

    @error_handler
    def delete(self, name: str) -> None:
        if not self.has(name):
            raise ValueError(f'Theme style name "' + name + '" does not exist.')
        del self._styles[name]


class TrapezoidStyles:
    def __init__(self, shapestyles: ShapeStyles) -> None:
        self._styles: Dict[str, ShapeStyle] = dict()
        self._shapestyles = shapestyles

    @error_handler
    def has(self, name: str) -> bool:
        """Whether having theme name or not"""
        return name in self._styles

    @error_handler
    def get(self, name: str = "", use_shapestyles_if_not_exist: bool = True) -> ShapeStyle:
        if self.has(name):
            return self._styles[name].copy()
        if not use_shapestyles_if_not_exist:
            raise ValueError(f'Theme style name "' + name + '" does not exist.')
        return self._shapestyles.get(name)

    @error_handler
    def list(self) -> List[str]:
        return list_(self._styles.keys())

    @error_handler
    def set(self, style: ShapeStyle, name: str = "") -> None:
        style_validator.validate_shapestyle("style", style)
        type_validator.validate_str("name", name)
        self._styles[name] = style.copy()

    @error_handler
    def delete(self, name: str) -> None:
        if not self.has(name):
            raise ValueError(f'Theme style name "' + name + '" does not exist.')
        del self._styles[name]


class TriangleStyles:
    def __init__(self, shapestyles: ShapeStyles) -> None:
        self._styles: Dict[str, ShapeStyle] = dict()
        self._shapestyles = shapestyles

    @error_handler
    def has(self, name: str) -> bool:
        """Whether having theme name or not"""
        return name in self._styles

    @error_handler
    def get(self, name: str = "", use_shapestyles_if_not_exist: bool = True) -> ShapeStyle:
        if self.has(name):
            return self._styles[name].copy()
        if not use_shapestyles_if_not_exist:
            raise ValueError(f'Theme style name "' + name + '" does not exist.')
        return self._shapestyles.get(name)

    @error_handler
    def list(self) -> List[str]:
        return list_(self._styles.keys())

    @error_handler
    def set(self, style: ShapeStyle, name: str = "") -> None:
        style_validator.validate_shapestyle("style", style)
        type_validator.validate_str("name", name)
        self._styles[name] = style.copy()

    @error_handler
    def delete(self, name: str) -> None:
        if not self.has(name):
            raise ValueError(f'Theme style name "' + name + '" does not exist.')
        del self._styles[name]


class BubblespeechStyles:
    def __init__(self, shapestyles: ShapeStyles) -> None:
        self._styles: Dict[str, ShapeStyle] = dict()
        self._shapestyles = shapestyles

    @error_handler
    def has(self, name: str) -> bool:
        """Whether having theme name or not"""
        return name in self._styles

    @error_handler
    def get(self, name: str = "", use_shapestyles_if_not_exist: bool = True) -> ShapeStyle:
        if self.has(name):
            return self._styles[name].copy()
        if not use_shapestyles_if_not_exist:
            raise ValueError(f'Theme style name "' + name + '" does not exist.')
        return self._shapestyles.get(name)

    @error_handler
    def list(self) -> List[str]:
        return list_(self._styles.keys())

    @error_handler
    def set(self, style: ShapeStyle, name: str = "") -> None:
        style_validator.validate_shapestyle("style", style)
        type_validator.validate_str("name", name)
        self._styles[name] = style.copy()

    @error_handler
    def delete(self, name: str) -> None:
        if not self.has(name):
            raise ValueError(f'Theme style name "' + name + '" does not exist.')
        del self._styles[name]


class ArcTextStyles:
    def __init__(self, shapetextstyles: ShapeTextStyles) -> None:
        self._styles: Dict[str, ShapeTextStyle] = dict()
        self._shapetextstyles = shapetextstyles

    @error_handler
    def has(self, name: str) -> bool:
        """Whether having theme name or not"""
        return name in self._styles

    @error_handler
    def get(self, name: str = "", use_shapetextstyles_if_not_exist: bool = True) -> ShapeTextStyle:
        if self.has(name):
            return self._styles[name].copy()
        if not use_shapetextstyles_if_not_exist:
            raise ValueError(f'Theme style name "' + name + '" does not exist.')
        return self._shapetextstyles.get(name)

    @error_handler
    def list(self) -> List[str]:
        return list_(self._styles.keys())

    @error_handler
    def set(self, style: ShapeTextStyle, name: str = "") -> None:
        style_validator.validate_shapetextstyle("style", style)
        type_validator.validate_str("name", name)
        self._styles[name] = style.copy()

    @error_handler
    def delete(self, name: str) -> None:
        if not self.has(name):
            raise ValueError(f'Theme style name "' + name + '" does not exist.')
        del self._styles[name]


class CircleTextStyles:
    def __init__(self, shapetextstyles: ShapeTextStyles) -> None:
        self._styles: Dict[str, ShapeTextStyle] = dict()
        self._shapetextstyles = shapetextstyles

    @error_handler
    def has(self, name: str) -> bool:
        """Whether having theme name or not"""
        return name in self._styles

    @error_handler
    def get(self, name: str = "", use_shapetextstyles_if_not_exist: bool = True) -> ShapeTextStyle:
        if self.has(name):
            return self._styles[name].copy()
        if not use_shapetextstyles_if_not_exist:
            raise ValueError(f'Theme style name "' + name + '" does not exist.')
        return self._shapetextstyles.get(name)

    @error_handler
    def list(self) -> List[str]:
        return list_(self._styles.keys())

    @error_handler
    def set(self, style: ShapeTextStyle, name: str = "") -> None:
        style_validator.validate_shapetextstyle("style", style)
        type_validator.validate_str("name", name)
        self._styles[name] = style.copy()

    @error_handler
    def delete(self, name: str) -> None:
        if not self.has(name):
            raise ValueError(f'Theme style name "' + name + '" does not exist.')
        del self._styles[name]


class DonutsTextStyles:
    def __init__(self, shapetextstyles: ShapeTextStyles) -> None:
        self._styles: Dict[str, ShapeTextStyle] = dict()
        self._shapetextstyles = shapetextstyles

    @error_handler
    def has(self, name: str) -> bool:
        """Whether having theme name or not"""
        return name in self._styles

    @error_handler
    def get(self, name: str = "", use_shapetextstyles_if_not_exist: bool = True) -> ShapeTextStyle:
        if self.has(name):
            return self._styles[name].copy()
        if not use_shapetextstyles_if_not_exist:
            raise ValueError(f'Theme style name "' + name + '" does not exist.')
        return self._shapetextstyles.get(name)

    @error_handler
    def list(self) -> List[str]:
        return list_(self._styles.keys())

    @error_handler
    def set(self, style: ShapeTextStyle, name: str = "") -> None:
        style_validator.validate_shapetextstyle("style", style)
        type_validator.validate_str("name", name)
        self._styles[name] = style.copy()

    @error_handler
    def delete(self, name: str) -> None:
        if not self.has(name):
            raise ValueError(f'Theme style name "' + name + '" does not exist.')
        del self._styles[name]


class EllipseTextStyles:
    def __init__(self, shapetextstyles: ShapeTextStyles) -> None:
        self._styles: Dict[str, ShapeTextStyle] = dict()
        self._shapetextstyles = shapetextstyles

    @error_handler
    def has(self, name: str) -> bool:
        """Whether having theme name or not"""
        return name in self._styles

    @error_handler
    def get(self, name: str = "", use_shapetextstyles_if_not_exist: bool = True) -> ShapeTextStyle:
        if self.has(name):
            return self._styles[name].copy()
        if not use_shapetextstyles_if_not_exist:
            raise ValueError(f'Theme style name "' + name + '" does not exist.')
        return self._shapetextstyles.get(name)

    @error_handler
    def list(self) -> List[str]:
        return list_(self._styles.keys())

    @error_handler
    def set(self, style: ShapeTextStyle, name: str = "") -> None:
        style_validator.validate_shapetextstyle("style", style)
        type_validator.validate_str("name", name)
        self._styles[name] = style.copy()

    @error_handler
    def delete(self, name: str) -> None:
        if not self.has(name):
            raise ValueError(f'Theme style name "' + name + '" does not exist.')
        del self._styles[name]


class FanTextStyles:
    def __init__(self, shapetextstyles: ShapeTextStyles) -> None:
        self._styles: Dict[str, ShapeTextStyle] = dict()
        self._shapetextstyles = shapetextstyles

    @error_handler
    def has(self, name: str) -> bool:
        """Whether having theme name or not"""
        return name in self._styles

    @error_handler
    def get(self, name: str = "", use_shapetextstyles_if_not_exist: bool = True) -> ShapeTextStyle:
        if self.has(name):
            return self._styles[name].copy()
        if not use_shapetextstyles_if_not_exist:
            raise ValueError(f'Theme style name "' + name + '" does not exist.')
        return self._shapetextstyles.get(name)

    @error_handler
    def list(self) -> List[str]:
        return list_(self._styles.keys())

    @error_handler
    def set(self, style: ShapeTextStyle, name: str = "") -> None:
        style_validator.validate_shapetextstyle("style", style)
        type_validator.validate_str("name", name)
        self._styles[name] = style.copy()

    @error_handler
    def delete(self, name: str) -> None:
        if not self.has(name):
            raise ValueError(f'Theme style name "' + name + '" does not exist.')
        del self._styles[name]


class PolygonTextStyles:
    def __init__(self, shapetextstyles: ShapeTextStyles) -> None:
        self._styles: Dict[str, ShapeTextStyle] = dict()
        self._shapetextstyles = shapetextstyles

    @error_handler
    def has(self, name: str) -> bool:
        """Whether having theme name or not"""
        return name in self._styles

    @error_handler
    def get(self, name: str = "", use_shapetextstyles_if_not_exist: bool = True) -> ShapeTextStyle:
        if self.has(name):
            return self._styles[name].copy()
        if not use_shapetextstyles_if_not_exist:
            raise ValueError(f'Theme style name "' + name + '" does not exist.')
        return self._shapetextstyles.get(name)

    @error_handler
    def list(self) -> List[str]:
        return list_(self._styles.keys())

    @error_handler
    def set(self, style: ShapeTextStyle, name: str = "") -> None:
        style_validator.validate_shapetextstyle("style", style)
        type_validator.validate_str("name", name)
        self._styles[name] = style.copy()

    @error_handler
    def delete(self, name: str) -> None:
        if not self.has(name):
            raise ValueError(f'Theme style name "' + name + '" does not exist.')
        del self._styles[name]


class RectangleTextStyles:
    def __init__(self, shapetextstyles: ShapeTextStyles) -> None:
        self._styles: Dict[str, ShapeTextStyle] = dict()
        self._shapetextstyles = shapetextstyles

    @error_handler
    def has(self, name: str) -> bool:
        """Whether having theme name or not"""
        return name in self._styles

    @error_handler
    def get(self, name: str = "", use_shapetextstyles_if_not_exist: bool = True) -> ShapeTextStyle:
        if self.has(name):
            return self._styles[name].copy()
        if not use_shapetextstyles_if_not_exist:
            raise ValueError(f'Theme style name "' + name + '" does not exist.')
        return self._shapetextstyles.get(name)

    @error_handler
    def list(self) -> List[str]:
        return list_(self._styles.keys())

    @error_handler
    def set(self, style: ShapeTextStyle, name: str = "") -> None:
        style_validator.validate_shapetextstyle("style", style)
        type_validator.validate_str("name", name)
        self._styles[name] = style.copy()

    @error_handler
    def delete(self, name: str) -> None:
        if not self.has(name):
            raise ValueError(f'Theme style name "' + name + '" does not exist.')
        del self._styles[name]


class RegularpolygonTextStyles:
    def __init__(self, shapetextstyles: ShapeTextStyles) -> None:
        self._styles: Dict[str, ShapeTextStyle] = dict()
        self._shapetextstyles = shapetextstyles

    @error_handler
    def has(self, name: str) -> bool:
        """Whether having theme name or not"""
        return name in self._styles

    @error_handler
    def get(self, name: str = "", use_shapetextstyles_if_not_exist: bool = True) -> ShapeTextStyle:
        if self.has(name):
            return self._styles[name].copy()
        if not use_shapetextstyles_if_not_exist:
            raise ValueError(f'Theme style name "' + name + '" does not exist.')
        return self._shapetextstyles.get(name)

    @error_handler
    def list(self) -> List[str]:
        return list_(self._styles.keys())

    @error_handler
    def set(self, style: ShapeTextStyle, name: str = "") -> None:
        style_validator.validate_shapetextstyle("style", style)
        type_validator.validate_str("name", name)
        self._styles[name] = style.copy()

    @error_handler
    def delete(self, name: str) -> None:
        if not self.has(name):
            raise ValueError(f'Theme style name "' + name + '" does not exist.')
        del self._styles[name]


class WedgeTextStyles:
    def __init__(self, shapetextstyles: ShapeTextStyles) -> None:
        self._styles: Dict[str, ShapeTextStyle] = dict()
        self._shapetextstyles = shapetextstyles

    @error_handler
    def has(self, name: str) -> bool:
        """Whether having theme name or not"""
        return name in self._styles

    @error_handler
    def get(self, name: str = "", use_shapetextstyles_if_not_exist: bool = True) -> ShapeTextStyle:
        if self.has(name):
            return self._styles[name].copy()
        if not use_shapetextstyles_if_not_exist:
            raise ValueError(f'Theme style name "' + name + '" does not exist.')
        return self._shapetextstyles.get(name)

    @error_handler
    def list(self) -> List[str]:
        return list_(self._styles.keys())

    @error_handler
    def set(self, style: ShapeTextStyle, name: str = "") -> None:
        style_validator.validate_shapetextstyle("style", style)
        type_validator.validate_str("name", name)
        self._styles[name] = style.copy()

    @error_handler
    def delete(self, name: str) -> None:
        if not self.has(name):
            raise ValueError(f'Theme style name "' + name + '" does not exist.')
        del self._styles[name]


class ArrowTextStyles:
    def __init__(self, shapetextstyles: ShapeTextStyles) -> None:
        self._styles: Dict[str, ShapeTextStyle] = dict()
        self._shapetextstyles = shapetextstyles

    @error_handler
    def has(self, name: str) -> bool:
        """Whether having theme name or not"""
        return name in self._styles

    @error_handler
    def get(self, name: str = "", use_shapetextstyles_if_not_exist: bool = True) -> ShapeTextStyle:
        if self.has(name):
            return self._styles[name].copy()
        if not use_shapetextstyles_if_not_exist:
            raise ValueError(f'Theme style name "' + name + '" does not exist.')
        return self._shapetextstyles.get(name)

    @error_handler
    def list(self) -> List[str]:
        return list_(self._styles.keys())

    @error_handler
    def set(self, style: ShapeTextStyle, name: str = "") -> None:
        style_validator.validate_shapetextstyle("style", style)
        type_validator.validate_str("name", name)
        self._styles[name] = style.copy()

    @error_handler
    def delete(self, name: str) -> None:
        if not self.has(name):
            raise ValueError(f'Theme style name "' + name + '" does not exist.')
        del self._styles[name]


class ChevronTextStyles:
    def __init__(self, shapetextstyles: ShapeTextStyles) -> None:
        self._styles: Dict[str, ShapeTextStyle] = dict()
        self._shapetextstyles = shapetextstyles

    @error_handler
    def has(self, name: str) -> bool:
        """Whether having theme name or not"""
        return name in self._styles

    @error_handler
    def get(self, name: str = "", use_shapetextstyles_if_not_exist: bool = True) -> ShapeTextStyle:
        if self.has(name):
            return self._styles[name].copy()
        if not use_shapetextstyles_if_not_exist:
            raise ValueError(f'Theme style name "' + name + '" does not exist.')
        return self._shapetextstyles.get(name)

    @error_handler
    def list(self) -> List[str]:
        return list_(self._styles.keys())

    @error_handler
    def set(self, style: ShapeTextStyle, name: str = "") -> None:
        style_validator.validate_shapetextstyle("style", style)
        type_validator.validate_str("name", name)
        self._styles[name] = style.copy()

    @error_handler
    def delete(self, name: str) -> None:
        if not self.has(name):
            raise ValueError(f'Theme style name "' + name + '" does not exist.')
        del self._styles[name]


class ParallelogramTextStyles:
    def __init__(self, shapetextstyles: ShapeTextStyles) -> None:
        self._styles: Dict[str, ShapeTextStyle] = dict()
        self._shapetextstyles = shapetextstyles

    @error_handler
    def has(self, name: str) -> bool:
        """Whether having theme name or not"""
        return name in self._styles

    @error_handler
    def get(self, name: str = "", use_shapetextstyles_if_not_exist: bool = True) -> ShapeTextStyle:
        if self.has(name):
            return self._styles[name].copy()
        if not use_shapetextstyles_if_not_exist:
            raise ValueError(f'Theme style name "' + name + '" does not exist.')
        return self._shapetextstyles.get(name)

    @error_handler
    def list(self) -> List[str]:
        return list_(self._styles.keys())

    @error_handler
    def set(self, style: ShapeTextStyle, name: str = "") -> None:
        style_validator.validate_shapetextstyle("style", style)
        type_validator.validate_str("name", name)
        self._styles[name] = style.copy()

    @error_handler
    def delete(self, name: str) -> None:
        if not self.has(name):
            raise ValueError(f'Theme style name "' + name + '" does not exist.')
        del self._styles[name]


class RhombusTextStyles:
    def __init__(self, shapetextstyles: ShapeTextStyles) -> None:
        self._styles: Dict[str, ShapeTextStyle] = dict()
        self._shapetextstyles = shapetextstyles

    @error_handler
    def has(self, name: str) -> bool:
        """Whether having theme name or not"""
        return name in self._styles

    @error_handler
    def get(self, name: str = "", use_shapetextstyles_if_not_exist: bool = True) -> ShapeTextStyle:
        if self.has(name):
            return self._styles[name].copy()
        if not use_shapetextstyles_if_not_exist:
            raise ValueError(f'Theme style name "' + name + '" does not exist.')
        return self._shapetextstyles.get(name)

    @error_handler
    def list(self) -> List[str]:
        return list_(self._styles.keys())

    @error_handler
    def set(self, style: ShapeTextStyle, name: str = "") -> None:
        style_validator.validate_shapetextstyle("style", style)
        type_validator.validate_str("name", name)
        self._styles[name] = style.copy()

    @error_handler
    def delete(self, name: str) -> None:
        if not self.has(name):
            raise ValueError(f'Theme style name "' + name + '" does not exist.')
        del self._styles[name]


class StarTextStyles:
    def __init__(self, shapetextstyles: ShapeTextStyles) -> None:
        self._styles: Dict[str, ShapeTextStyle] = dict()
        self._shapetextstyles = shapetextstyles

    @error_handler
    def has(self, name: str) -> bool:
        """Whether having theme name or not"""
        return name in self._styles

    @error_handler
    def get(self, name: str = "", use_shapetextstyles_if_not_exist: bool = True) -> ShapeTextStyle:
        if self.has(name):
            return self._styles[name].copy()
        if not use_shapetextstyles_if_not_exist:
            raise ValueError(f'Theme style name "' + name + '" does not exist.')
        return self._shapetextstyles.get(name)

    @error_handler
    def list(self) -> List[str]:
        return list_(self._styles.keys())

    @error_handler
    def set(self, style: ShapeTextStyle, name: str = "") -> None:
        style_validator.validate_shapetextstyle("style", style)
        type_validator.validate_str("name", name)
        self._styles[name] = style.copy()

    @error_handler
    def delete(self, name: str) -> None:
        if not self.has(name):
            raise ValueError(f'Theme style name "' + name + '" does not exist.')
        del self._styles[name]


class TrapezoidTextStyles:
    def __init__(self, shapetextstyles: ShapeTextStyles) -> None:
        self._styles: Dict[str, ShapeTextStyle] = dict()
        self._shapetextstyles = shapetextstyles

    @error_handler
    def has(self, name: str) -> bool:
        """Whether having theme name or not"""
        return name in self._styles

    @error_handler
    def get(self, name: str = "", use_shapetextstyles_if_not_exist: bool = True) -> ShapeTextStyle:
        if self.has(name):
            return self._styles[name].copy()
        if not use_shapetextstyles_if_not_exist:
            raise ValueError(f'Theme style name "' + name + '" does not exist.')
        return self._shapetextstyles.get(name)

    @error_handler
    def list(self) -> List[str]:
        return list_(self._styles.keys())

    @error_handler
    def set(self, style: ShapeTextStyle, name: str = "") -> None:
        style_validator.validate_shapetextstyle("style", style)
        type_validator.validate_str("name", name)
        self._styles[name] = style.copy()

    @error_handler
    def delete(self, name: str) -> None:
        if not self.has(name):
            raise ValueError(f'Theme style name "' + name + '" does not exist.')
        del self._styles[name]


class TriangleTextStyles:
    def __init__(self, shapetextstyles: ShapeTextStyles) -> None:
        self._styles: Dict[str, ShapeTextStyle] = dict()
        self._shapetextstyles = shapetextstyles

    @error_handler
    def has(self, name: str) -> bool:
        """Whether having theme name or not"""
        return name in self._styles

    @error_handler
    def get(self, name: str = "", use_shapetextstyles_if_not_exist: bool = True) -> ShapeTextStyle:
        if self.has(name):
            return self._styles[name].copy()
        if not use_shapetextstyles_if_not_exist:
            raise ValueError(f'Theme style name "' + name + '" does not exist.')
        return self._shapetextstyles.get(name)

    @error_handler
    def list(self) -> List[str]:
        return list_(self._styles.keys())

    @error_handler
    def set(self, style: ShapeTextStyle, name: str = "") -> None:
        style_validator.validate_shapetextstyle("style", style)
        type_validator.validate_str("name", name)
        self._styles[name] = style.copy()

    @error_handler
    def delete(self, name: str) -> None:
        if not self.has(name):
            raise ValueError(f'Theme style name "' + name + '" does not exist.')
        del self._styles[name]


class BubblespeechTextStyles:
    def __init__(self, shapetextstyles: ShapeTextStyles) -> None:
        self._styles: Dict[str, ShapeTextStyle] = dict()
        self._shapetextstyles = shapetextstyles

    @error_handler
    def has(self, name: str) -> bool:
        """Whether having theme name or not"""
        return name in self._styles

    @error_handler
    def get(self, name: str = "", use_shapetextstyles_if_not_exist: bool = True) -> ShapeTextStyle:
        if self.has(name):
            return self._styles[name].copy()
        if not use_shapetextstyles_if_not_exist:
            raise ValueError(f'Theme style name "' + name + '" does not exist.')
        return self._shapetextstyles.get(name)

    @error_handler
    def list(self) -> List[str]:
        return list_(self._styles.keys())

    @error_handler
    def set(self, style: ShapeTextStyle, name: str = "") -> None:
        style_validator.validate_shapetextstyle("style", style)
        type_validator.validate_str("name", name)
        self._styles[name] = style.copy()

    @error_handler
    def delete(self, name: str) -> None:
        if not self.has(name):
            raise ValueError(f'Theme style name "' + name + '" does not exist.')
        del self._styles[name]
