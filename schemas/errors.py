from pydantic import BaseModel
from typing import Any, Optional

class MCPError(BaseModel):
    status: str = "error"
    code: str
    message: str
    provider: Optional[str] = None
    request_id: Optional[str] = None
    details: Optional[Any] = None


class MCPSuccess(BaseModel):
    status: str = "success"
    code: str = "OK"
    provider: str
    request_id: str
    data: Any
