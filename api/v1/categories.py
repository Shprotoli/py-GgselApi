# A class file that handles requests from the `Categories` category of the GGSell API
from schemas.categories_object import CategoriesObject
from api.v1.category import Category


class Categories(Category):
    def categories(
            self,
            page: int = 1,
            count: int = 10,
            category_id: str = "",
            lang: str = "ru-RU"
    ) -> CategoriesObject:
        """
        Source docs: https://seller.ggsel.com/docs/return-all-categories
        This feature allows you to receive lists of GGSel categories/subcategories

        :param page: Category page
        :param count: The number of master categories that will be found
        :param category_id: The ID of the specific category to be found
                            (P.S In this case, count will affect the categories within the requested category)
        :param lang: The language in which the categories will be returned
        :return: dataclass CategoriesObject containing a json response from the API
        """
        params = {
            "page": page,
            "count": count,
            "category_id": category_id,
        }
        headers = {
            "lang": lang,
        }

        response = self.client.get("categories", params=params, headers=headers)
        data = response.json()

        return CategoriesObject(**data)