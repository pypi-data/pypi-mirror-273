![PyPI - Python Version](https://img.shields.io/pypi/pyversions/payok-aio)
![PyPI - Implementation](https://img.shields.io/pypi/implementation/payok_aio)
![PyPI - Version](https://img.shields.io/pypi/v/payok_aio)
[![wakatime](https://wakatime.com/badge/user/d1734201-6222-408c-98a4-642d2b764ecb/project/018dfcb0-b754-4ee2-98d0-437403cb0bf1.svg)](https://wakatime.com/badge/user/d1734201-6222-408c-98a4-642d2b764ecb/project/018dfcb0-b754-4ee2-98d0-437403cb0bf1)

# Payok API Client

Python асинхронный клиент для взаимодействия с Payok API. Позволяет получать баланс, транзакции и создавать платежные формы.

## Установка

```bash
pip install payok-aio
```

## Примеры использования

```python
import asyncio
from payok_aio import Payok

# Замените на реальные значения своих API ID и API Key
api_id = 123456
api_key = "your_api_key"

# Создаем экземпляр класса Payok
payok_instance = Payok(api_id=api_id, api_key=api_key)

async def main():
    # Получаем баланс
    balance_result = await payok_instance.get_balance()
    if balance_result:
        print(f"Баланс: {balance_result.balance}, Реф. баланс: {balance_result.ref_balance}")
    else:
        print("Не удалось получить баланс.")

    # Получаем транзакции
    transactions_result = await payok_instance.get_transactions()
    if transactions_result:
        if isinstance(transactions_result, list):
            for transaction in transactions_result:
                print(f"Транзакция {transaction.transaction_id}: {transaction.amount} {transaction.currency}")
        else:
            print(f"Транзакция {transactions_result.transaction_id}: {transactions_result.amount} {transactions_result.currency}")
    else:
        print("Не удалось получить транзакции.")

    # Создаем платеж
    payment_url = await payok_instance.create_pay(
        amount=100.0,
        payment="order123",
        currency="RUB",
        desc="Оплата заказа",
        email="buyer@example.com",
        success_url="https://example.com/success",
        method="card",
        lang="RU",
        custom="custom_data"
    )

    if payment_url:
        print(f"Ссылка для оплаты: {payment_url}")
    else:
        print("Не удалось создать платеж.")

if __name__ == '__main__':
    asyncio.run(main())
```

## Документация

Подробную документацию по API можно найти [здесь](https://payok.io/cabinet/documentation/doc_main.php).

## Лицензия

Этот проект лицензирован по лицензии GNU GPLv3  - см. файл [LICENSE](https://github.com/BazZziliuS/payok_aio/blob/main/LICENSE) для подробностей.

Замените `your_api_key`, `your_api_id` и другие данные в соответствии с вашими реальными значениями. Этот `README.md` содержит простой пример использования и может быть дополнен дополнительной информацией в зависимости от ваших потребностей.