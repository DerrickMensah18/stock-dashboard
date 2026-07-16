from pydantic import BaseModel
from typing import Optional

class Stock(BaseModel):
  ticker: str
  name: str
  price: float
  volume: float
  market_cap: Optional[float] = None