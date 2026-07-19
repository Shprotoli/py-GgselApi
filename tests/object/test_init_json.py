import unittest

from schemas.v1.balance_object import BalanceObject
from schemas.v1.categories_object import CategoriesObject
from schemas.v1.chats_object import ChatsObject
from schemas.v1.info_order_object import InfoOrderObject
from schemas.v1.last_sales_object import LastSalesObject
from schemas.v1.messages_object import MessagesObject
from schemas.v1.offer_list_object import OfferListObject
from schemas.v1.offer_object import OfferObject
from schemas.v1.offer_search_object import OfferSearchObject
from schemas.v1.receipts_object import ReceiptsObject
from schemas.v1.reviews_object import ReviewsObject
from schemas.v1.seller_goods_list_object import SellerGoodsListObject
from schemas.v1.token_object import TokenObject
from schemas.v1.unique_code_object import UniqueCodeObject


class TestTokenObject(unittest.TestCase):
    def test_token_object(self):
        TokenObject(
            retval=0,
            desc="string",
            token="string",
            seller_id=0,
            valid_thru="string",
        )


class TestBalanceObject(unittest.TestCase):
    def test_balance_object(self):
        BalanceObject(
            retval=0,
            retdesc="string",
            errors=["string"],
            content={
                "amount_t_lock": 0,
                "amount_t_free": 0,
                "amount_t_plus": 0,
            },
        )


class TestCategoriesObject(unittest.TestCase):
    def test_categories_object(self):
        CategoriesObject(
            retval=0,
            retdesc="string",
            category=[{"id": 0, "name": "string", "sub": [0], "cnt": 0}],
        )


class TestReceiptsObject(unittest.TestCase):
    def test_receipts_object(self):
        ReceiptsObject(
            retval=0,
            retdesc="string",
            errors=["string"],
            content={
                "page": 0,
                "count": 0,
                "has_next_page": True,
                "has_previous_page": True,
                "total_count": 0,
                "total_pages": 0,
                "items": [],
            },
        )


class TestOfferListObject(unittest.TestCase):
    def test_offer_list_object(self):
        OfferListObject(
            retval=0,
            retdesc="string",
            page=0,
            count=0,
            has_next_page=True,
            has_previous_page=True,
            total_count=0,
            total_pages=0,
            rows=[],
        )


class TestSellerGoodsListObject(unittest.TestCase):
    def test_seller_goods_list_object(self):
        SellerGoodsListObject(
            retval=0,
            retdesc="string",
            id_seller=0,
            name_seller="string",
            cnt_goods=0,
            pages=0,
            page=0,
            order_col="string",
            order_dir="string",
            rows=[],
        )


class TestOfferSearchObject(unittest.TestCase):
    def test_offer_search_object(self):
        OfferSearchObject(
            retval=0,
            retdesc="string",
            pages={"name": 0, "rows": 0},
            products=[],
        )


class TestOfferObject(unittest.TestCase):
    def test_offer_object(self):
        OfferObject(
            retval=0,
            retdesc="string",
            product={
                "id": 0,
                "id_prev": 0,
                "id_next": 0,
                "name": "string",
                "price": 0,
                "currency": "string",
                "url": "string",
                "info": "string",
                "add_info": "string",
                "release_date": "string",
                "agency_fee": "string",
                "agency_sum": "string",
                "agency_id": 0,
                "collection": "string",
                "propertygood": 0,
                "is_available": 0,
                "show_rest": 0,
                "num_in_stock": 0,
                "num_in_lock": 0,
                "prices": {
                    "initial": {"RUB": 0, "USD": 0, "EUR": 0},
                    "default": {"RUB": 0, "USD": 0, "EUR": 0},
                },
                "payment_methods": [],
                "prices_unit": {
                    "unit_name": "string",
                    "unit_amount": 0,
                    "unit_amount_desc": "string",
                    "unit_currency": "string",
                    "unit_cnt": 0,
                    "unit_cnt_min": 0,
                    "unit_cnt_max": 0,
                    "unit_cnt_desc": "string",
                    "unit_fixed": True,
                    "unit_only_int": True,
                },
                "unique_code_verification": {},
                "preview_imgs": [],
                "preview_videos": [],
                "type": "string",
                "text": "string",
                "file": "string",
                "category_id": 0,
                "breadcrumbs": [],
                "discounts": [],
                "units": [],
                "present": {},
                "gift_commiss": "string",
                "options": [],
                "options_check": 0,
                "statistics": {
                    "sales": 0,
                    "refunds": 0,
                    "good_reviews": 0,
                    "bad_reviews": 0,
                },
                "seller": {"id": 0, "name": "string"},
                "sale_info": {
                    "common_base_price": 0,
                    "common_price_usd": 0,
                    "common_price_eur": 0,
                    "common_price_rur": 0,
                    "sale_end": "string",
                    "sale_percent": "string",
                },
            },
        )


class TestReviewsObject(unittest.TestCase):
    def test_reviews_object(self):
        ReviewsObject(
            retval=0,
            retdesc="string",
            totalPages=0,
            totalItems=0,
            totalGood=0,
            totalBad=0,
            reviews=[],
        )


class TestUniqueCodeObject(unittest.TestCase):
    def test_unique_code_object(self):
        UniqueCodeObject(
            retval=0,
            retdesc="string",
            inv=0,
            id_goods=0,
            amount=0,
            type_curr="string",
            amount_usd=0,
            profit=0,
            date_pay="string",
            email="string",
            name_invoice="string",
            lang="string",
            agent_id=0,
            agent_percent="string",
            query_string="string",
            unit_goods="string",
            cnt_goods="string",
            promo_code="string",
            bonus_code="string",
            cart_uid="string",
            unique_code_state={
                "state": 0,
                "date_check": "string",
                "date_delivery": "string",
                "date_confirmed": "string",
                "date_refuted": "string",
            },
            options=[],
        )


class TestLastSalesObject(unittest.TestCase):
    def test_last_sales_object(self):
        LastSalesObject(retval=0, retdesc="string", sales=[])


class TestChatsObject(unittest.TestCase):
    def test_chats_object(self):
        ChatsObject(cnt_pages=0, items=[])


class TestMessagesObject(unittest.TestCase):
    def test_messages_object(self):
        MessagesObject(messages=[])


class TestInfoOrderObject(unittest.TestCase):
    def test_info_order_object(self):
        InfoOrderObject(
            retval=0,
            retdesc="string",
            content={
                "item_id": 0,
                "content_id": 0,
                "cart_uid": "string",
                "name": "string",
                "amount": 0,
                "currency_type": "USD",
                "invoice_state": 0,
                "purchase_date": "2024-01-01T12:00:00Z",
                "date_pay": "2024-01-01T12:30:00Z",
                "agent_id": 0,
                "agent_percent": 0,
                "agent_fee": 0,
                "query_string": "string",
                "unit_goods": "string",
                "cnt_goods": "string",
                "promo_code": "string",
                "bonus_code": "string",
                "feedback": {
                    "deleted": True,
                    "feedback": "string",
                    "feedback_type": "positive",
                    "comment": "string",
                },
                "unique_code_state": {
                    "state": 0,
                    "date_check": "string",
                    "date_delivery": "string",
                    "date_confirmed": "string",
                    "date_refuted": "string",
                },
                "options": [],
                "buyer_info": {
                    "payment_method": "string",
                    "account": "string",
                    "email": "string",
                    "phone": "string",
                    "skype": "string",
                    "whatsapp": "string",
                    "ip_address": "string",
                    "payment_aggregator": "string",
                },
                "owner": 0,
                "day_lock": 0,
                "lock_state": "free",
                "profit": 0,
                "external_order_id": "string",
            },
        )


if __name__ == "__main__":
    unittest.main()
