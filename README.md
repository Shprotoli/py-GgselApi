<img src="logos/Logo_1.png" width="400" alt="Logo">

**ENG:**

py-GGSel API is a low-level library that provides a convenient interface for interacting with the GGsel API through a set of methods.

The library is designed using object-oriented programming (OOP) principles, which ensures flexibility, extensibility, and ease of integration into various projects.

Currently, py-GGSel API is in the early stages of development, so the functionality may change, and some features may be limited.

py-GGSel is based on the official GGSel API and its documentation — https://seller.ggsel.com/docs/seller-api-v-1

---

**RU:**

py-GGSel API — это низкоуровневая библиотека, предоставляющая удобный интерфейс для взаимодействия с API GGsel через набор методов.

Библиотека разработана с использованием принципов объектно-ориентированного программирования (ООП), что обеспечивает гибкость, расширяемость и удобство интеграции в различные проекты.

В настоящее время py-GGSel API находится на ранней стадии разработки, поэтому функциональность может изменяться, а некоторые возможности — быть ограниченными.

py-GGSel основан на GGSel API и его документации — https://seller.ggsel.com/docs/seller-api-v-1

---

You can find all the available API methods in the official GGSel API documentation.

To call a specific method from the documentation, you can follow these steps: First, create an API instance (`GgselApiV1`), then select a category (API instance argument), and finally call the desired method (the method names are almost identical to those in the documentation).

```python
from api.ggsel_api import GgselApiV1
from schemas.v1.balance_object import BalanceObject

TOKEN = "YOUR TOKEN"  # Method for get token — https://seller.ggsel.com/docs/return-seller-token

api_obj = GgselApiV1(TOKEN)

api_account_category = api_obj.account  # Choosing a category
balance_info: BalanceObject = api_account_category.seller_balance_info()
```