from datetime import datetime

from elemental_tools.pydantic import BaseModel, Field




class TransactionSchema(BaseModel):
    currency_from: str = "BRL"
    currency_to: str = "USDT"
    price: float = None
    amount_from: float = None
    amount_to: float = None
