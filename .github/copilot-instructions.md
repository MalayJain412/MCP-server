**Core Flow**
- [server.py](server.py) hosts an mcp.server.FastMCP named crm-mcp and registers the create_lead tool with @server.tool() decorator.
- create_lead takes a CreateLeadInput Pydantic model (containing provider, payload as CreateLeadPayload, and optional request_id), validates input, emits audit_log entries, checks provider validity, and returns MCPError or MCPSuccess responses.
- Pydantic models in [schemas/lead.py](schemas/lead.py) enforce email validation and optional contact fields; no manual validation needed in handlers.

**Providers**
- CRMProvider abstract base in [providers/base.py](providers/base.py) defines create_lead contract returning dict with status_code and json.
- [providers/zoho.py](providers/zoho.py) and [providers/salesforce.py](providers/salesforce.py) POST to external FastAPI endpoints with timeout from config.
- Provider instances are instantiated in [router.py](router.py) PROVIDERS dict for stateless operation.

**Schemas and Errors**
- Response models in [schemas/responses.py](schemas/responses.py) standardize MCP-compatible error/success payloads with status, code, and data/details fields.
- Use MCPSuccess for 2xx responses, MCPError for failures with appropriate codes (INVALID_PROVIDER, VALIDATION_ERROR, API_ERROR).

**Logging and Observability**
- [utils/audit.py](utils/audit.py) prints structured JSON events (request_received, success) to stdout for monitoring.
- Network calls use requests with config timeouts; consider safe_request wrapper in [utils/http.py](utils/http.py) for error handling.

**Configuration**
- Constants in [config.py](config.py) centralize base URLs, server name, and timeouts; update here for environment changes.
- External APIs are deployed FastAPI services; coordinate URL updates with provider implementations.

**Runtime**
- Activate venv and install requirements.txt (includes mcp, pydantic[email], requests, FastAPI, uvicorn).
- Run MCP server with python server.py; communicates via stdio for MCP protocol.
- Test with [test_mcp.py](test_mcp.py) using MCP client libraries to verify tool registration and execution.

**Extending**
- Add new CRM providers by implementing CRMProvider, adding to router.py PROVIDERS, and updating config URLs.
- Register tools with @server.tool() decorator on async functions taking Pydantic-typed inputs.
- Preserve MCPError codes for automation; emit audit events for all request paths following request_received/success pattern.
