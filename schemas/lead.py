from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class CreateLeadPayload(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    email: EmailStr
    company: Optional[str]
    phone: Optional[str]
