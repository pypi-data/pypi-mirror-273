import asyncio
import ssl
from typing import Optional
import aiohttp
import certifi

from .exceptions import CodeErrorFactory


# Асинхронная сессия для запросов
class AsyncRequestSession:
    def __init__(self) -> None:
        self._session: Optional[aiohttp.ClientSession] = None
        self._loop = asyncio.get_event_loop()

    # Вызов сессии
    async def get_session(self) -> aiohttp.ClientSession:
        if self._session is None:
            ssl_context = ssl.create_default_context(cafile=certifi.where())
            connector = aiohttp.TCPConnector(ssl=ssl_context)
            new_session = aiohttp.ClientSession(connector=connector)
            self._session = new_session

        return self._session

    # Закрытие сессии
    async def close(self) -> None:
        if self._session is None:
            return None

        await self._session.close()

    async def _validate_response(self, HTTPMethods: str, url: str, data: dict) -> dict:
        session = await self.get_session()
        response = await session.request(HTTPMethods, url=url, data=data)
        try:
            response = await response.json(content_type="text/plain")
        except:  # noqa: E722
            raise CodeErrorFactory(1, "Ответ получен не в Json")

        if response.get("status") and response.pop("status") == "error":
            desc = response.get("text", response.get("error_text"))
            code = response["error_code"]
            raise CodeErrorFactory(code, desc)

        return response

    def __del__(self):
        if self._session:
            self._loop.run_until_complete(self._session.close())
