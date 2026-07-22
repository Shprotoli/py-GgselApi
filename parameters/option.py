from enum import Enum, StrEnum
from dataclasses import dataclass, asdict


class OptionVariant(Enum):
    CHECKBOX = {
        "type": "check_box",
        "has_splitted_products": False,
    }

    RADIO = {
        "type": "radio_button",
        "has_splitted_products": False,
    }

    RADIO_SPLITTED = {
        "type": "radio_button",
        "has_splitted_products": True,
    }

    TEXT = {
        "type": "text",
        "has_splitted_products": False,
    }

    MULTILINE_TEXT = {
        "type": "multiline_text",
        "has_splitted_products": False,
    }


@dataclass
class OptionParametr:
    type: str
    has_splitted_products: bool
    title_ru: str
    title_en: str
    comment_ru: str
    comment_en: str
    is_required: bool
    position: int


@dataclass
class OptionList:
    options: list[OptionParametr | dict]

    def asdict(self):
        return asdict(self)


OptionListType = OptionList | dict[str, list[OptionParametr, ...]]


def generate_option(
        option_type: OptionVariant,
        title_ru: str,
        title_en: str,
        comment_ru: str,
        comment_en: str,
        is_required: bool = True,
        position: int = 0,
) -> OptionParametr:
    return OptionParametr(
        **option_type.value,
        title_ru=title_ru,
        title_en=title_en,
        comment_ru=comment_ru,
        comment_en=comment_en,
        is_required=is_required,
        position=position,
    )


class DiscountType(StrEnum):
    FIXED = "fixed"
    PERCENT = "percent"


class ImpactType(StrEnum):
    INCREASE = "increase"
    DECREASE = "decrease"


class StatusVariantType(StrEnum):
    ACTIVE = "active"
    ARCHIVED = "archived"


@dataclass
class OptionValue:
    id: int
    title_ru: str
    title_en: str
    price: int | float
    discount_type: str
    impact_type: str
    is_default: bool
    status: str
    position: int


@dataclass
class OptionValueList:
    variants: list[OptionValue | dict]

    def asdict(self):
        return asdict(self)


OptionValueListType = OptionValueList | dict[str, list[OptionValue]]


def generate_option_value(
        title_ru: str,
        title_en: str,
        price: int | float,
        id: int | None = None,
        discount_type: str | DiscountType = DiscountType.FIXED,
        impact_type: str | ImpactType = ImpactType.DECREASE,
        is_default: bool = False,
        status: str | StatusVariantType = StatusVariantType.ACTIVE,
        position: int = 0,
) -> OptionValue:
    return OptionValue(
        id=id,
        title_ru=title_ru,
        title_en=title_en,
        price=price,
        discount_type=discount_type,
        impact_type=impact_type,
        is_default=is_default,
        status=status,
        position=position,
    )
