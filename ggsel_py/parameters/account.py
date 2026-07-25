from enum import StrEnum


class Currency(StrEnum):
    WMT = "WMT"


class Type(StrEnum):
    AGENT_ACCRUALS = "agent_accurals"
    PRODUCT_SALES = "product_sales"
    ADD_FUNDS = "add_funds"
    EXCHANGE_RESPONSE = "exchange_response"
    EXCHANGE_REQUEST = "exchange_request"
    REFUND = "refund"
    ADV_GOODS = "adv_goods"
    EXTERNAL_COMMISSIONS = "external_commissions"
    HARD_DISK_RENT = "hard_disk_rent"
    EXTRA_PARTNER_SPACE = "extra_partner_space"
    GIFT_CERTIFICATES = "gift_certificates"
    TRANSFER_TO_WALLET = "transfer_to_wallet"


class CodeFilter(StrEnum):
    ONLY_WAITING_CODE_CHECK = "only_waiting_code_check"
    HIDE_WAITING_CODE_CHECK = "hide_waiting_code_check"
