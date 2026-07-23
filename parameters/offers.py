from enum import StrEnum
from typing import Optional, Dict, Any

from parameters.globals import Currency


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


def generate_offer(
        title_ru: Optional[str] = None,
        title_en: Optional[str] = None,
        description_ru: Optional[str] = None,
        description_en: Optional[str] = None,
        instructions_ru: Optional[str] = None,
        instructions_en: Optional[str] = None,
        cover_image_ru: Optional[str] = None,
        cover_image_en: Optional[str] = None,
        price: Optional[float] = None,
        currency: Optional[Currency] = None,
        is_autoselling: Optional[bool] = None,
        category_id: Optional[int] = None,
        min_quantity: Optional[int] = None,
        max_quantity: Optional[int] = None,
        quantity: Optional[int] = None,
        is_unlimited_quantity: Optional[bool] = None,
        post_payment_url: Optional[str] = None,
        delivery: Optional[DeliveryStatus] = None,
        pre_payment_settings: Optional[Dict[str, Any]] = None,
        notification_settings: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    data = {
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
    }

    data = {k: v for k, v in data.items() if v is not None}

    if pre_payment_settings is not None:
        data["pre_payment_settings"] = {
            k: v for k, v in pre_payment_settings.items() if v is not None
        }

    if notification_settings is not None:
        data["notification_settings"] = {
            k: v for k, v in notification_settings.items() if v is not None
        }

    return data


def regular_offer_template(
        title_ru: str,
        title_en: str,
        description_ru: str,
        description_en: str,
        price: float,
        category_id: int,
        currency: Currency | str = Currency.RUB,
        quantity: int = 999,
        cover_image_ru: str = None,
):
    return {
        "title_ru": title_ru,
        "title_en": title_en,
        "description_ru": description_ru,
        "description_en": description_en,
        "cover_image_ru": cover_image_ru,
        "price": price,
        "currency": currency,
        "category_id": category_id,
        "quantity": quantity,
    }


def autoselling_offer_template(
        title_ru: str,
        title_en: str,
        description_ru: str,
        description_en: str,
        price: float,
        category_id: int,
        currency: Currency | str = Currency.RUB,
        cover_image_ru: str = None,
):
    return {
        "title_ru": title_ru,
        "title_en": title_en,
        "description_ru": description_ru,
        "description_en": description_en,
        "cover_image_ru": cover_image_ru,
        "price": price,
        "currency": currency,
        "is_autoselling": True,
        "category_id": category_id,
    }


def unlimited_quantity_template(
        title_ru: str,
        title_en: str,
        description_ru: str,
        description_en: str,
        price: float,
        category_id: int,
        currency: Currency | str = Currency.RUB,
        cover_image_ru: str = None,
):
    return {
        "title_ru": title_ru,
        "title_en": title_en,
        "description_ru": description_ru,
        "description_en": description_en,
        "cover_image_ru": cover_image_ru,
        "price": price,
        "currency": currency,
        "category_id": category_id,
        "is_unlimited_quantity": True,
    }


def offer_with_email_notifications_template(
        email: str,
        title_ru: str,
        title_en: str,
        description_ru: str,
        description_en: str,
        price: float,
        category_id: int,
        currency: Currency | str = Currency.RUB,
        cover_image_ru: str = None,
):
    return {
        "title_ru": title_ru,
        "title_en": title_en,
        "description_ru": description_ru,
        "description_en": description_en,
        "cover_image_ru": cover_image_ru,
        "price": price,
        "currency": currency,
        "category_id": category_id,
        "notification_settings": {
            "type": "email",
            "email": email,
            "is_default": True,
        },
    }


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
        cover_image_ru: str = None,
):
    return {
        "title_ru": title_ru,
        "title_en": title_en,
        "description_ru": description_ru,
        "description_en": description_en,
        "cover_image_ru": cover_image_ru,
        "price": price,
        "currency": currency,
        "category_id": category_id,
        "notification_settings": {
            "type": "url",
            "http_method": http_method,
            "url": url,
            "is_default": True,
        },
    }


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
        cover_image_ru: str = None,
):
    return {
        "title_ru": title_ru,
        "title_en": title_en,
        "description_ru": description_ru,
        "description_en": description_en,
        "cover_image_ru": cover_image_ru,
        "price": price,
        "currency": currency,
        "category_id": category_id,
        "post_payment_url": post_payment_url,
        "pre_payment_settings": {
            "url": pre_payment_url,
            "allow_payment": allow_payment,
        },
    }


def generate_product_offer(
        title_ru: Optional[str] = None,
        title_en: Optional[str] = None,
        description_ru: Optional[str] = None,
        description_en: Optional[str] = None,
        instructions_ru: Optional[str] = None,
        instructions_en: Optional[str] = None,
        cover_image_ru: Optional[str] = None,
        cover_image_en: Optional[str] = None,
        price: Optional[float] = None,
        currency: Optional[Currency] = Currency.RUB,
        is_autoselling: Optional[bool] = None,
        category_id: Optional[int] = None,
        min_quantity: Optional[int] = None,
        max_quantity: Optional[int] = None,
        quantity: Optional[int] = None,
        is_unlimited_quantity: Optional[bool] = None,
        post_payment_url: Optional[str] = None,
        delivery: Optional[DeliveryStatus] = None,
        pre_payment_settings: Optional[Dict[str, Any]] = None,
        notification_settings: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    data = {
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
    }

    data = {k: v for k, v in data.items() if v is not None}

    if pre_payment_settings is not None:
        data["pre_payment_settings"] = {
            k: v
            for k, v in pre_payment_settings.items()
            if v is not None
        }

    if notification_settings is not None:
        data["notification_settings"] = {
            k: v
            for k, v in notification_settings.items()
            if v is not None
        }

    return data
