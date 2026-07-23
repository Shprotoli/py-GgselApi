from dataclasses import dataclass

from schemas.ggsel_object import GgselObjectApiV2
from schemas.v2.category_object import CategoryObject


@dataclass
class PrePaymentSettingsObject:
    is_enabled: bool = None
    url: str = None
    allow_payment: bool = None


@dataclass
class NotificationSettingsObject:
    type: str = None
    url: str = None
    email: str = None
    http_method: str = None
    is_disabled: bool = None
    is_default: bool = None


@dataclass
class OfferEntity(GgselObjectApiV2):
    id: int = None
    status: str = None
    title_ru: str = None
    title_en: str = None
    description_ru: str = None
    description_en: str = None
    price: float = None
    currency: str = None
    is_autoselling: bool = None
    category: CategoryObject = None
    min_quantity: int = None
    max_quantity: int = None
    quantity: int = None
    is_unlimited_quantity: bool = None
    instructions_ru: str = None
    instructions_en: str = None
    post_payment_url: str = None
    delivery: str = None
    cover_image_ru_url: str = None
    cover_image_en_url: str = None
    has_options: bool = None
    has_products: bool = None
    has_splitted_products: bool = None
    created_at: str = None
    updated_at: str = None
    pre_payment_settings: PrePaymentSettingsObject = None
    notification_settings: NotificationSettingsObject = None


@dataclass
class OfferObject(GgselObjectApiV2):
    data: OfferEntity | None = None
