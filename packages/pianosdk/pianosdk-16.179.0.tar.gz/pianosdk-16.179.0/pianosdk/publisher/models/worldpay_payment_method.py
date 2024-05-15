from datetime import date, datetime
from pydantic.main import BaseModel
from typing import Optional
from typing import List


class WorldpayPaymentMethod(BaseModel):
    card: Optional[List[str]] = None
    apm: Optional[List[str]] = None


WorldpayPaymentMethod.model_rebuild()
