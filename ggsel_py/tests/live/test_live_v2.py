# Live read-only requests of the V2 API (API key), through the synchronous and asynchronous clients
from datetime import datetime

import pytest

from ggsel_py.parameters.offers import DeliveryStatus
from ggsel_py.schemas.v2.list_of import ListOfCategories, ListOfOffers, ListOfOption, ListOfProducts
from ggsel_py.schemas.v2.offer_object import OfferObject
from ggsel_py.schemas.v2.option_object import OptionObject

pytestmark = pytest.mark.live

# The order and the product the live tests are checked against (see the order of `.env.test.example`)
PRODUCT_ID = 102238375

# In V2 the product of the order is an offer
OFFER_ID = PRODUCT_ID


def test_list_of_categories(api_v2, expect):
    result = expect(api_v2.categories.list_of_categories(parent_id=0, limit=5), ListOfCategories)

    assert isinstance(result.data, list)


def test_search_categories(api_v2, expect):
    result = expect(api_v2.categories.search_categories("Perplexity", limit=5), ListOfCategories)

    assert isinstance(result.data, list)


def test_list_offers(api_v2, expect):
    result = expect(
        api_v2.offers.list_offers("", DeliveryStatus.AUTO, datetime(2020, 1, 1), limit=5),
        ListOfOffers,
    )

    assert isinstance(result.data, list)


def test_get_offer(api_v2, expect):
    result = expect(api_v2.offers.get_offer(OFFER_ID), OfferObject)

    assert result.data["id"] == OFFER_ID


def test_offer_options(api_v2, expect):
    options = expect(api_v2.options.list_active_offer_options(OFFER_ID), ListOfOption)
    if not options.data:
        pytest.skip("the offer has no active options")

    option_id = options.data[0]["id"]
    result = expect(api_v2.options.view_option(OFFER_ID, option_id), OptionObject)

    assert result.data["id"] == option_id


def test_list_products(api_v2, expect):
    expect(api_v2.products.list_products(OFFER_ID), ListOfProducts)


def test_list_splitted_products(api_v2, expect):
    options = expect(api_v2.options.list_active_offer_options(OFFER_ID), ListOfOption)
    splitted = [option for option in options.data or [] if option.get("has_splitted_products")]
    if not splitted or not splitted[0].get("variants"):
        pytest.skip("the offer has no options with splitted products")

    variant_id = splitted[0]["variants"][0]["id"]
    expect(api_v2.products.list_splitted_products(OFFER_ID, variant_id), ListOfProducts)


def test_async_client(run_async_v2, expect):
    async def requests(api):
        return (
            await api.categories.search_categories("Perplexity", limit=5),
            await api.offers.get_offer(OFFER_ID),
            await api.options.list_active_offer_options(OFFER_ID),
            await api.products.list_products(OFFER_ID),
        )

    categories, offer, options, products = run_async_v2(requests)

    expect(categories, ListOfCategories)
    assert expect(offer, OfferObject).data["id"] == OFFER_ID
    expect(options, ListOfOption)
    expect(products, ListOfProducts)
