# A class file that handles requests from the `Products` category of the GGSell API
from parameters.products import Variant
from parameters.globals import Lang
from schemas.offer_list_object import OfferListObject
from api.v1.category import Category


class Products(Category):
    # This method does not work and returns incorrect answers
    """
    Source docs: https://seller.ggsel.com/docs/updates-prices-of-products-and-variants-in-bulk
    def product_edit_prices(
            self,
            product_id: int,
            price: int,
            variants: list[Variant] = (),
    ) -> dict:
        payload = {
            "product_id": product_id,
            "price": price,
            "variants": [
                variant.as_dict() for variant in variants
            ],
        }

        response = self.client.post("product/edit/prices", data=payload)
        data = response.json()

        return data
    """

    def products_list(
            self,
            ids: str | int | list[str, int],
            page: int = 1,
            count: int = 10,
            lang: str | Lang = Lang.RU,
            locale: str | Lang = Lang.RU,
    ) -> OfferListObject:
        """
        Source docs: https://seller.ggsel.com/docs/return-all-products
        The method gets a list of products based on the specified parameters

        :param ids: Comma separated product IDs
        :param page: Page
        :param count: Count products
        :param lang: The language of the goods
        :param locale: Localization of goods
        :return: dataclass OfferListObject containing a json response from the API
        """
        if not isinstance(ids, (list, tuple)):
            ids = [ids]

        params = {
            "ids": ",".join(map(str, ids)),
            "page": page,
            "count": count,
        }
        headers = {
            "lang": lang,
            "locale": locale,
        }

        response = self.client.get("products/list", params=params, headers=headers)
        data = response.json()

        return OfferListObject(**data)