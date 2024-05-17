from pydantic import BaseModel


class Balance(BaseModel):
    """Payok API balance model"""

    balance: float
    ref_balance: float


class Transaction(BaseModel):
    """Payok API transaction model"""

    transaction: int
    email: str
    amount: float
    currency: str
    currency_amount: float
    comission_percent: float
    comission_fixed: float
    amount_profit: float
    method: str | None
    payment_id: int | str
    description: str
    date: str
    pay_date: str
    transaction_status: int
    custom_fields: str
    webhook_status: int
    webhook_amount: int
