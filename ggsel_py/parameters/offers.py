from enum import StrEnum
from typing import Any

from ggsel_py.parameters.common import drop_none
from ggsel_py.parameters.globals import Currency


class StatusOffer(StrEnum):
    ACTIVE = "active"
    PAUSED = "paused"
    DRAFT = "draft"


class SortOffer(StrEnum):
    PRICE_ASC = "price_asc"
    PRICE_DESC = "price_desc"
    SALES_COUNT_ASC = "sales_count_asc"
    SALES_COUNT_DESC = "sales_count_desc"
    PRODUCTS_COUNT_ASC = "products_count_asc"
    PRODUCTS_COUNT_DESC = "products_count_desc"


class DeliveryStatus(StrEnum):
    AUTO = "auto"
    MANUAL = "manual"


class BatchAction(StrEnum):
    ACTIVATE = "activate"
    PAUSE = "pause"
    DELETE = "delete"


def generate_offer(
        title_ru: str | None = None,
        title_en: str | None = None,
        description_ru: str | None = None,
        description_en: str | None = None,
        instructions_ru: str | None = None,
        instructions_en: str | None = None,
        cover_image_ru: str | None = None,
        cover_image_en: str | None = None,
        price: float | None = None,
        currency: Currency | None = None,
        is_autoselling: bool | None = None,
        category_id: int | None = None,
        min_quantity: int | None = None,
        max_quantity: int | None = None,
        quantity: int | None = None,
        is_unlimited_quantity: bool | None = None,
        post_payment_url: str | None = None,
        delivery: DeliveryStatus | None = None,
        pre_payment_settings: dict[str, Any] | None = None,
        notification_settings: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """
    Builds the body for `create_offer`/`patch_offer`. Fields that are `None` are left out,
    including the fields inside `pre_payment_settings` and `notification_settings`.
    """
    data = drop_none({
        "title_ru": title_ru,
        "title_en": title_en,
        "description_ru": description_ru,
        "description_en": description_en,
        "instructions_ru": instructions_ru,
        "instructions_en": instructions_en,
        "cover_image_ru": cover_image_ru,
        "cover_image_en": cover_image_en,
        "price": price,
        "currency": currency,
        "is_autoselling": is_autoselling,
        "category_id": category_id,
        "min_quantity": min_quantity,
        "max_quantity": max_quantity,
        "quantity": quantity,
        "is_unlimited_quantity": is_unlimited_quantity,
        "post_payment_url": post_payment_url,
        "delivery": delivery,
    })

    if pre_payment_settings is not None:
        data["pre_payment_settings"] = drop_none(pre_payment_settings)

    if notification_settings is not None:
        data["notification_settings"] = drop_none(notification_settings)

    return data


def generate_product_offer(
        title_ru: str | None = None,
        title_en: str | None = None,
        description_ru: str | None = None,
        description_en: str | None = None,
        instructions_ru: str | None = None,
        instructions_en: str | None = None,
        cover_image_ru: str | None = None,
        cover_image_en: str | None = None,
        price: float | None = None,
        currency: Currency | None = Currency.RUB,
        is_autoselling: bool | None = None,
        category_id: int | None = None,
        min_quantity: int | None = None,
        max_quantity: int | None = None,
        quantity: int | None = None,
        is_unlimited_quantity: bool | None = None,
        post_payment_url: str | None = None,
        delivery: DeliveryStatus | None = None,
        pre_payment_settings: dict[str, Any] | None = None,
        notification_settings: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """The same as `generate_offer`, but the currency is RUB by default"""
    return generate_offer(
        title_ru=title_ru,
        title_en=title_en,
        description_ru=description_ru,
        description_en=description_en,
        instructions_ru=instructions_ru,
        instructions_en=instructions_en,
        cover_image_ru=cover_image_ru,
        cover_image_en=cover_image_en,
        price=price,
        currency=currency,
        is_autoselling=is_autoselling,
        category_id=category_id,
        min_quantity=min_quantity,
        max_quantity=max_quantity,
        quantity=quantity,
        is_unlimited_quantity=is_unlimited_quantity,
        post_payment_url=post_payment_url,
        delivery=delivery,
        pre_payment_settings=pre_payment_settings,
        notification_settings=notification_settings,
    )


def _offer_template(
        title_ru: str,
        title_en: str,
        description_ru: str,
        description_en: str,
        price: float,
        category_id: int,
        currency: Currency | str,
        cover_image_ru: str | None,
        fields_before_category: dict[str, Any] | None = None,
        **fields: Any,
) -> dict[str, Any]:
    """
    The fields shared by all `*_template` functions; unlike `generate_offer`, `None` values are kept.
    `fields` are added at the end, `fields_before_category` keep the historical order of the JSON body.
    """
    return {
        "title_ru": title_ru,
        "title_en": title_en,
        "description_ru": description_ru,
        "description_en": description_en,
        "cover_image_ru": cover_image_ru,
        "price": price,
        "currency": currency,
        **(fields_before_category or {}),
        "category_id": category_id,
        **fields,
    }


def regular_offer_template(
        title_ru: str,
        title_en: str,
        description_ru: str,
        description_en: str,
        price: float,
        category_id: int,
        currency: Currency | str = Currency.RUB,
        quantity: int = 999,
        cover_image_ru: str | None = None,
) -> dict[str, Any]:
    return _offer_template(
        title_ru, title_en, description_ru, description_en, price, category_id, currency, cover_image_ru,
        quantity=quantity,
    )


def autoselling_offer_template(
        title_ru: str,
        title_en: str,
        description_ru: str,
        description_en: str,
        price: float,
        category_id: int,
        currency: Currency | str = Currency.RUB,
        cover_image_ru: str | None = None,
) -> dict[str, Any]:
    return _offer_template(
        title_ru, title_en, description_ru, description_en, price, category_id, currency, cover_image_ru,
        fields_before_category={"is_autoselling": True},
    )


def unlimited_quantity_template(
        title_ru: str,
        title_en: str,
        description_ru: str,
        description_en: str,
        price: float,
        category_id: int,
        currency: Currency | str = Currency.RUB,
        cover_image_ru: str | None = None,
) -> dict[str, Any]:
    return _offer_template(
        title_ru, title_en, description_ru, description_en, price, category_id, currency, cover_image_ru,
        is_unlimited_quantity=True,
    )


def offer_with_email_notifications_template(
        email: str,
        title_ru: str,
        title_en: str,
        description_ru: str,
        description_en: str,
        price: float,
        category_id: int,
        currency: Currency | str = Currency.RUB,
        cover_image_ru: str | None = None,
) -> dict[str, Any]:
    return _offer_template(
        title_ru, title_en, description_ru, description_en, price, category_id, currency, cover_image_ru,
        notification_settings={
            "type": "email",
            "email": email,
            "is_default": True,
        },
    )


def offer_with_http_notification_template(
        url: str,
        http_method: str,
        title_ru: str,
        title_en: str,
        description_ru: str,
        description_en: str,
        price: float,
        category_id: int,
        currency: Currency | str = Currency.RUB,
        cover_image_ru: str | None = None,
) -> dict[str, Any]:
    return _offer_template(
        title_ru, title_en, description_ru, description_en, price, category_id, currency, cover_image_ru,
        notification_settings={
            "type": "url",
            "http_method": http_method,
            "url": url,
            "is_default": True,
        },
    )


def offer_with_pre_and_post_payment_template(
        pre_payment_url: str,
        post_payment_url: str,
        title_ru: str,
        title_en: str,
        description_ru: str,
        description_en: str,
        price: float,
        category_id: int,
        allow_payment: bool = True,
        currency: Currency | str = Currency.RUB,
        cover_image_ru: str | None = None,
) -> dict[str, Any]:
    return _offer_template(
        title_ru, title_en, description_ru, description_en, price, category_id, currency, cover_image_ru,
        post_payment_url=post_payment_url,
        pre_payment_settings={
            "url": pre_payment_url,
            "allow_payment": allow_payment,
        },
    )
