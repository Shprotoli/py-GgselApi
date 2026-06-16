from tools.handlers import handler_response_api, ApiResult
from parameters.globals import Lang
from api.v1.category import Category
from schemas.last_sales_object import LastSalesObject
from schemas.info_order_object import InfoOrderObject
from schemas.unique_code_object import UniqueCodeObject


class Orders(Category):
    def last_sales(self, seller_id: int, group: bool = True, top: int = 10, locale: str | Lang = Lang.RU) -> ApiResult:
        """
        Source docs: https://seller.ggsel.com/docs/return-last-sales
        This function gets a list of recent sales.
        The information is similar to the information on the page: `https://seller.ggsel.com/orders`

        :param seller_id: [NOW WORKING]
        :param group: [NOW WORKING]
        :param top: Number of entries
        :param locale: Localization of the returned information
        :return: dataclass LastSalesObject containing a json response from the API
        """
        params = {
            "seller_id": seller_id,
            "group": group,
            "top": top,
        }
        headers = {
            "locale": locale,
        }

        response = self.client.get("seller-last-sales", params=params, headers=headers)
        data = response.json()

        return handler_response_api(LastSalesObject, data=data)

    def order_info(self, invoice_id: int, locale: str | Lang = Lang.RU) -> ApiResult:
        """
        Source docs: https://seller.ggsel.com/docs/get-order-info
        This method returns general information about the customer and what they have purchased.

        :param invoice_id: Unique order number
        :param locale: locale: Localization of the returned information
        :return: dataclass InfoOrderObject containing a json response from the API
        """
        headers = {
            "locale": locale,
        }

        response = self.client.get(f"purchase/info/{invoice_id}", headers=headers)
        data = response.json()

        return handler_response_api(InfoOrderObject, data=data)

    def check_unique_code(self, unique_code: str) -> ApiResult:
        """
        Source docs: https://seller.ggsel.com/docs/check-unique-code
        Unlike `order_info`, this method returns more specific information about the product
        that the customer purchased using the unique order code.

        :param unique_code:
        :return:
        """
        response = self.client.get(f"purchases/unique-code/{unique_code}")
        data = response.json()

        return handler_response_api(UniqueCodeObject, data=data)
