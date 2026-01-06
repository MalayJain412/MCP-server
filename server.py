from mcp import Server, Tool
from schemas.lead import CreateLeadPayload
from schemas.errors import MCPError, MCPSuccess
from utils.audit import audit_log
from config import MCP_SERVER_NAME
from router import PROVIDERS
import uuid


server = Server(MCP_SERVER_NAME)


async def create_lead(provider: str, payload: dict, request_id: str = None):

    request_id = request_id or str(uuid.uuid4())

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

    # Validate payload schema
    try:
        CreateLeadPayload(**payload)
    except Exception as e:
        return MCPError(
            code="VALIDATION_ERROR",
            message=str(e),
            provider=provider,
            request_id=request_id
        ).dict()

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


server.add_tool(
    Tool(
        name="create_lead",
        description="Create a CRM lead in Zoho or Salesforce",
        input_schema={
            "type": "object",
            "properties": {
                "provider": {"type": "string"},
                "payload": {"type": "object"},
                "request_id": {"type": "string"}
            },
            "required": ["provider", "payload"]
        },
        func=create_lead
    )
)


if __name__ == "__main__":
    server.run()
