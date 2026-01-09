from mcp.server import FastMCP
from schemas.lead import CreateLeadPayload
from schemas.responses import MCPError, MCPSuccess
from utils.audit import audit_log
from config import MCP_SERVER_NAME
from router import PROVIDERS
from pydantic import BaseModel
from typing import Optional
import uuid


class CreateLeadInput(BaseModel):
    provider: str
    payload: CreateLeadPayload
    request_id: Optional[str] = None


server = FastMCP(MCP_SERVER_NAME)


@server.tool()
async def create_lead(input: CreateLeadInput):

    provider = input.provider
    payload = input.payload.dict()
    request_id = input.request_id or str(uuid.uuid4())

    audit_log({
        "event": "request_received",
        "tool": "create_lead",
        "provider": provider,
        "request_id": request_id,
        "payload": payload
    })

    if provider not in PROVIDERS:
        return MCPError(
            code="INVALID_PROVIDER",
            message="Provider must be one of: zoho, salesforce",
            request_id=request_id
        ).dict()

    # Payload already validated by Pydantic

    provider_client = PROVIDERS[provider]

    res = provider_client.create_lead(payload)

    status = res.get("status_code")

    if status and 200 <= status < 300:
        audit_log({
            "event": "success",
            "provider": provider,
            "request_id": request_id
        })

        return MCPSuccess(
            provider=provider,
            request_id=request_id,
            data=res["json"]
        ).dict()

    return MCPError(
        code="API_ERROR",
        message="Provider rejected request",
        provider=provider,
        request_id=request_id,
        details=res
    ).dict()


if __name__ == "__main__":
    server.run()
