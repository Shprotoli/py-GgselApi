from dataclasses import dataclass

from schemas.ggsel_object import GgselObject


@dataclass
class OfferPricesPart:
    RUB: int
    USD: int
    EUR: int


@dataclass
class OfferPrices:
    initial: OfferPricesPart
    default: OfferPricesPart


@dataclass
class OfferPaymentLimit:
    min: int
    max: int


@dataclass
class OfferPaymentCurrency:
    currency: str
    code: str
    price: int
    limit: OfferPaymentLimit


@dataclass
class OfferPaymentMethod:
    name: str
    currencies: list[OfferPaymentCurrency]


@dataclass
class OfferPricesUnit:
    unit_name: str
    unit_amount: int
    unit_amount_desc: str
    unit_currency: str
    unit_cnt: int
    unit_cnt_min: int
    unit_cnt_max: int
    unit_cnt_desc: str
    unit_fixed: bool
    unit_only_int: bool


@dataclass
class OfferPreviewImage:
    url: str
    width: int
    height: int


@dataclass
class OfferPreviewVideo:
    url: str
    width: int
    height: int


@dataclass
class OfferBreadcrumb:
    id: int
    name: str


@dataclass
class OfferVariant:
    value: int
    text: str
    default: int
    modify: str
    modify_type: str
    modify_value: str
    modify_value_default: str
    num_in_stock: int
    visible: int


@dataclass
class OfferOption:
    name: int
    label: str
    type: str
    separate_content: int
    required: int
    modifier_visible: int
    variants: list[OfferVariant]


@dataclass
class OfferStatistics:
    sales: int
    refunds: int
    good_reviews: int
    bad_reviews: int


@dataclass
class OfferSeller:
    id: int
    name: str


@dataclass
class OfferSaleInfo:
    common_base_price: int
    common_price_usd: int
    common_price_eur: int
    common_price_rur: int
    sale_end: str
    sale_percent: str


@dataclass
class OfferProduct:
    id: int
    id_prev: int
    id_next: int
    name: str
    price: int
    currency: str
    url: str
    info: str
    add_info: str
    release_date: str
    agency_fee: str
    agency_sum: str
    agency_id: int
    collection: str
    propertygood: int
    is_available: int
    show_rest: int
    num_in_stock: int
    num_in_lock: int
    prices: OfferPrices
    payment_methods: list[OfferPaymentMethod]
    prices_unit: OfferPricesUnit
    unique_code_verification: dict
    preview_imgs: list[OfferPreviewImage]
    preview_videos: list[OfferPreviewVideo]
    type: str
    text: str
    file: str
    category_id: int
    breadcrumbs: list[OfferBreadcrumb]
    discounts: list[dict]
    units: list[dict]
    present: dict
    gift_commiss: str
    options: list[OfferOption]
    options_check: int
    statistics: OfferStatistics
    seller: OfferSeller
    sale_info: OfferSaleInfo


@dataclass
class OfferObject(GgselObject):
    retdesc: str
    product: OfferProduct