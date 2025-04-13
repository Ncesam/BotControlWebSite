from pydantic import BaseModel


class Price(BaseModel):
    high_price: float
    low_price: float
    average_price: float
