from dataclasses import dataclass

from ggsel_py.schemas.ggsel_object import GgselObjectApiV2
from ggsel_py.schemas.v2.category_object import CategoryObject


@dataclass
class PrePaymentSettingsObject:
    is_enabled: bool | None = None
    url: str | None = None
    allow_payment: bool | None = None


@dataclass
class NotificationSettingsObject:
    type: str | None = None
    url: str | None = None
    email: str | None = None
    http_method: str | None = None
    is_disabled: bool | None = None
    is_default: bool | None = None


@dataclass
class OfferEntity(GgselObjectApiV2):
    id: int | None = None
    status: str | None = None
    title_ru: str | None = None
    title_en: str | None = None
    description_ru: str | None = None
    description_en: str | None = None
    price: float | None = None
    currency: str | None = None
    is_autoselling: bool | None = None
    category: CategoryObject | None = None
    min_quantity: int | None = None
    max_quantity: int | None = None
    quantity: int | None = None
    is_unlimited_quantity: bool | None = None
    instructions_ru: str | None = None
    instructions_en: str | None = None
    post_payment_url: str | None = None
    delivery: str | None = None
    cover_image_ru_url: str | None = None
    cover_image_en_url: str | None = None
    has_options: bool | None = None
    has_products: bool | None = None
    has_splitted_products: bool | None = None
    created_at: str | None = None
    updated_at: str | None = None
    pre_payment_settings: PrePaymentSettingsObject | None = None
    notification_settings: NotificationSettingsObject | None = None


@dataclass
class OfferObject(GgselObjectApiV2):
    data: OfferEntity | None = None
