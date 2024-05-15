from datetime import date, datetime
from pydantic.main import BaseModel
from typing import Optional


class PromotionFixedDiscountt(BaseModel):
    fixed_discount_id: Optional[str] = None
    currency: Optional[str] = None
    amount: Optional[str] = None


PromotionFixedDiscountt.model_rebuild()
