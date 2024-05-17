from enum import Enum


class HTTPMethods(str, Enum):
    '''Available HTTP methods.'''

    POST = 'POST'
    GET = 'GET'

class Currencies(str, Enum):
    RUB = 'RUB'
    UAH = 'UAH'
    USD = 'USD'
    EUR = 'EUR'
    RUB2 = 'RUB2'

class ErrorCode(Enum):
    TECHNICAL_ERROR = 0
    NO_API_ID = 1
    NO_API_KEY = 2
    UNIDENTIFIABLE_API_ID = 3
    INVALID_API_KEY = 4
    UNAUTHORIZED_IP = 5
    INSUFFICIENT_API_PERMISSIONS = 6
    PAYOUTS_NOT_FOUND = 7
    NO_SHOP_NUMBER = 8
    SHOP_NOT_FOUND = 9
    TRANSACTIONS_NOT_FOUND = 10
    INVALID_PAYMENT_NUMBER = 24
    LIMIT_REACHED = 25
    INVALID_AMOUNT = 11
    INVALID_COMMISSION_TYPE = 12
    INVALID_METHOD = 13
    INVALID_URL = 14
    PAYOUTS_DISABLED = 15
    INSTANT_PAYOUTS_NOT_APPROVED = 16
    NO_INITIALS_SPECIFIED = 17
    NEGATIVE_AMOUNT = 18
    BELOW_MINIMUM_PAYOUT_AMOUNT = 19
    INSUFFICIENT_FUNDS = 20
    PAYOUT_METHOD_UNAVAILABLE = 21
    QIWI_STATUS_NOT_SUPPORTED = 23
    INVALID_DATA_FORMAT = 24

ERROR_MESSAGES = {
    ErrorCode.TECHNICAL_ERROR.value: 'Техническая ошибка, сообщение уже отправлено администратору на почту. Обратитесь в чат, чтобы ознакомиться с подробностями.',
    ErrorCode.NO_API_ID.value: 'Не указан идентификатор API; Параметр API_ID',
    ErrorCode.NO_API_KEY.value: 'Не указан API-ключ; Параметр API_KEY',
    ErrorCode.UNIDENTIFIABLE_API_ID.value: 'Не удалось идентифицировать API по этому ID',
    ErrorCode.INVALID_API_KEY.value: 'Неверный ключ API; Параметр API_KEY',
    ErrorCode.UNAUTHORIZED_IP.value: 'IP-Адрес "Значение" не добавлен в список разрешенных IP',
    ErrorCode.INSUFFICIENT_API_PERMISSIONS.value: 'У этого ключа API нет прав на выполнение этой операции.',
    ErrorCode.PAYOUTS_NOT_FOUND.value: 'Выплат не найдено',
    ErrorCode.NO_SHOP_NUMBER.value: 'Не указан номер магазина; Параметр shop',
    ErrorCode.SHOP_NOT_FOUND.value: 'Магазин не найден; Параметр shop',
    ErrorCode.TRANSACTIONS_NOT_FOUND.value: 'Транзакций не найдено',
    ErrorCode.INVALID_PAYMENT_NUMBER.value: 'Неверно указан номер платежа; Параметр payment',
    ErrorCode.LIMIT_REACHED.value: 'Сработал лимит. *Подробности*',
    ErrorCode.INVALID_AMOUNT.value: 'Неправильное значение суммы. Укажите сумму в числовом, либо в вещественном типе; Параметр amount',
    ErrorCode.INVALID_COMMISSION_TYPE.value: 'Неверное значение типа комиссии, он может только 2 значения.value: balance или payment; Параметр comission',
    ErrorCode.INVALID_METHOD.value: 'Неверное значение метода, узнайте все доступные методы для выплаты в документации; Параметр method',
    ErrorCode.INVALID_URL.value: 'Указан неверный URL, введите корректный URL или оставьте значение пустым; Параметр webhook_url',
    ErrorCode.PAYOUTS_DISABLED.value: 'Возможность делать выплаты приостановлена для вашего аккаунта. Обратитесь в чат',
    ErrorCode.INSTANT_PAYOUTS_NOT_APPROVED.value: 'Вам еще не одобрены моментальные выплаты. Обратитесь в чат за одобрением. Массовые выплаты не будут работать, если эта опция отключена.',
    ErrorCode.NO_INITIALS_SPECIFIED.value: 'Необходимо указать инициалы в личном кабинете для осуществления выводов на банковскую карту.',
    ErrorCode.NEGATIVE_AMOUNT.value: 'Отрицательное значение суммы выплаты.',
    ErrorCode.BELOW_MINIMUM_PAYOUT_AMOUNT.value: 'Минимальная сумма к получению для способа "Способ" - \'Количество\' Рублей. (Сумма ниже минимально возможной для выплаты этим способом)',
    ErrorCode.INSUFFICIENT_FUNDS.value: 'Недостаточно средств',
    ErrorCode.PAYOUT_METHOD_UNAVAILABLE.value: 'В данный момент этот способ вывода недоступен, воспользуйтесь другим.',
    ErrorCode.QIWI_STATUS_NOT_SUPPORTED.value: 'Статус QIWI-кошелька получателя не позволяет перевести ему деньги.',
    ErrorCode.INVALID_DATA_FORMAT.value: 'Неверный формат данных.',
}
