from pydantic import BaseModel, constr
from typing import Optional, Literal

class Creative(BaseModel):
    text: constr(max_length=100)
    cta: str
    music_id: Optional[str]

class AdPayload(BaseModel):
    campaign_name: constr(min_length=3)
    objective: Literal["Traffic", "Conversions"]
    creative: Creative
