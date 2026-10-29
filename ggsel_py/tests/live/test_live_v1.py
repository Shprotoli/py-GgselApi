# Live read-only requests of the V1 API (token), through the synchronous and asynchronous clients
import pytest

from ggsel_py.schemas.v1.balance_object import BalanceObject
from ggsel_py.schemas.v1.categories_object import CategoriesObject
from ggsel_py.schemas.v1.chats_object import ChatsObject
from ggsel_py.schemas.v1.info_order_object import InfoOrderObject
from ggsel_py.schemas.v1.last_sales_object import LastSalesObject
from ggsel_py.schemas.v1.messages_object import MessagesObject
from ggsel_py.schemas.v1.offer_list_object import OfferListObject
from ggsel_py.schemas.v1.offer_object import OfferObject
from ggsel_py.schemas.v1.receipts_object import ReceiptsObject
from ggsel_py.schemas.v1.reviews_object import ReviewsObject
from ggsel_py.schemas.v1.seller_goods_list_object import SellerGoodsListObject
from ggsel_py.schemas.v1.unique_code_object import UniqueCodeObject

pytestmark = pytest.mark.live

# The order and the product the live tests are checked against (see the order of `.env.test.example`)
ORDER_ID = 33455315
PRODUCT_ID = 102238375


def test_seller_balance_info(api_v1, expect):
    expect(api_v1.account.seller_balance_info(), BalanceObject)


def test_seller_receipts(api_v1, expect):
    expect(api_v1.account.seller_receipts(count=5), ReceiptsObject)


def test_all_categories(api_v1, expect):
    expect(api_v1.categories.all_categories(count=5), CategoriesObject)


def test_list_chats(api_v1, expect):
    result = expect(api_v1.chats.list_chats(pagesize=5), ChatsObject)

    assert isinstance(result.items, list)


def test_list_messages_of_order(api_v1, expect):
    result = expect(api_v1.chats.list_messages(ORDER_ID, count=5), MessagesObject)

    assert isinstance(result.messages, list)


def test_last_sales(api_v1, expect):
    result = expect(api_v1.orders.last_sales(top=5), LastSalesObject)

    assert isinstance(result.sales, list)


def test_order_info(api_v1, expect):
    result = expect(api_v1.orders.order_info(ORDER_ID), InfoOrderObject)

    # Nested objects stay dicts (contract of ggsel_flow)
    assert result.content["item_id"] == PRODUCT_ID


def test_check_unique_code(api_v1, unique_code, expect):
    result = expect(api_v1.orders.check_unique_code(unique_code), UniqueCodeObject)

    assert result.inv == ORDER_ID
    assert result.id_goods == PRODUCT_ID


def test_all_products(api_v1, expect):
    expect(api_v1.products.all_products(PRODUCT_ID), OfferListObject)


def test_product_info(api_v1, expect):
    expect(api_v1.products.product_info(PRODUCT_ID), OfferObject)


def test_all_products_for_seller(api_v1, seller_id, expect):
    # POST in the API, but it only reads the list of goods
    expect(api_v1.products.all_products_for_seller(id_seller=seller_id, rows=5), SellerGoodsListObject)


def test_user_reviews(api_v1, expect):
    expect(api_v1.reviews.user_reviews(PRODUCT_ID, count=5), ReviewsObject)


def test_async_client(run_async_v1, unique_code, expect):
    async def requests(api):
        return (
            await api.account.seller_balance_info(),
            await api.chats.list_chats(pagesize=5),
            await api.chats.list_messages(ORDER_ID, count=5),
            await api.orders.last_sales(top=5),
            await api.orders.order_info(ORDER_ID),
            await api.orders.check_unique_code(unique_code),
        )

    balance, chats, messages, sales, order, code = run_async_v1(requests)

    expect(balance, BalanceObject)
    expect(chats, ChatsObject)
    expect(messages, MessagesObject)
    expect(sales, LastSalesObject)
    assert expect(order, InfoOrderObject).content["item_id"] == PRODUCT_ID
    assert expect(code, UniqueCodeObject).inv == ORDER_ID
