from hashlib import md5
from typing import List, Optional, Union
from urllib.parse import urlencode
from .const import Currencies, HTTPMethods
from .utils import AsyncRequestSession
from .models import Balance, Transaction


class Payok:
    API_HOST = "https://payok.io"
    API_DOCS = "https://payok.io/cabinet/documentation/doc_main.php"

    def __init__(
        self,
        api_id: int,
        api_key: str,
        secret_key: Optional[str] = None,
        shop: Optional[int] = None,
    ) -> None:
        """
        Init Payok API client
            :param api_id: Your API Key ID
            :param api_key: Your API Key
        """
        super().__init__()
        self.__api_id = api_id
        self.__api_key = api_key
        self.__secret_key = secret_key
        self._shop = shop
        self.session = AsyncRequestSession()

    async def get_balance(self) -> Balance:
        """
        Get balance and ref balance
            Docs: https://payok.io/cabinet/documentation/doc_api_balance
        """

        data = {"API_ID": self.__api_id, "API_KEY": self.__api_key}
        url = f"{self.API_HOST}/api/balance"
        response = await self.session._validate_response(
            HTTPMethods.POST.value, url=url, data=data
        )

        return Balance(**response)

    async def get_transactions(
        self, payment: Optional[Union[int, str]] = None, offset: Optional[int] = None
    ) -> Union[Transaction, List[Transaction]]:
        """
        payment	Int	ID платежа в вашей системе
        offset	Int	Отступ, пропуск указанного количества строк
        """
        method = HTTPMethods.POST.value
        url = f"{self.API_HOST}/api/transaction"
        data = {"API_ID": self.__api_id, "API_KEY": self.__api_key, "shop": self._shop}
        if payment:
            data["payment"] = payment
        if offset:
            data["offset"] = offset

        response = await self.session._validate_response(method, url, data=data)

        if payment:
            return Transaction(**response["1"])

        transactions = []
        for transaction in response.values():
            transactions.append(Transaction(**transaction))

        return transactions

    async def create_pay(
        self,
        amount: float,
        payment: Union[int, str],
        currency: Optional[str] = Currencies.RUB.value,
        desc: Optional[str] = "Description",
        email: Optional[str] = None,
        success_url: Optional[str] = None,
        method: Optional[str] = None,
        lang: Optional[str] = None,
        custom: Optional[str] = None,
    ) -> str:
        """
        Create payform url
            :param payment: Order number, unique in your system, up to 16 characters. (a-z0-9-_)
            :param amount : Order amount.
            :param currency : ISO 4217 currency. Default is "RUB".
            :param desc : Product name or description.
            :param email : Email Buyer mail. Defaults to None.
            :param success_url: Link to redirect after payment.
            :param method: Payment method
            :param lang: Interface language. RU or EN
            :param custom: Parameter that you want to pass in the notification.
            Docs: https://payok.io/cabinet/documentation/doc_payform.php
        """
        if not self.__secret_key:
            raise Exception("Secret key is empty")

        params = {
            "amount": amount,
            "payment": payment,
            "shop": self._shop,
            "currency": currency,
            "desc": desc,
            "email": email,
            "success_url": success_url,
            "method": method,
            "lang": lang,
            "custom": custom,
        }

        for key, value in params.copy().items():
            if value is None:
                del params[key]

        sign_params = "|".join(
            map(str, [amount, payment, self._shop, currency, desc, self.__secret_key])
        ).encode("utf-8")
        sign = md5(sign_params).hexdigest()
        params["sign"] = sign

        url = f"{self.API_HOST}/pay?" + urlencode(params)
        return url
