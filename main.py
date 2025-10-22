from fastmcp import FastMCP
import requests
import os

JAEGER_URL = os.getenv("JAEGER_URL", "http://localhost:16686")
LISTENING_PROTOCOL = os.getenv("LISTENING_PROTOCOL", "http")
LISTENING_IP = os.getenv("LISTENING_IP", "0.0.0.0")
LISTENING_PORT = os.getenv("LISTENING_PORT", 8000)

mcp = FastMCP(name="Jaeger MCP server")

@mcp.tool(name="get_services", description="List all services from Jaeger")
def get_services() -> list[str]:
    resp = requests.get(f"{JAEGER_URL}/api/v3/services")
    resp.raise_for_status()
    return resp.json().get("data", [])

@mcp.tool(name="get_operations", description="List operations by service")
def get_operations(service: str, spanKind: str = None) -> list[dict]:
    params = {"service": service}
    if spanKind:
        params["spanKind"] = spanKind
    resp = requests.get(f"{JAEGER_URL}/api/v3/operations", params=params)
    resp.raise_for_status()
    return resp.json().get("data", [])

@mcp.tool(name="get_trace", description="Retrieve spans for a trace ID")
def get_trace(traceId: str, startTime: str = None, endTime: str = None) -> dict:
    params = {}
    if startTime: params["start"] = startTime
    if endTime: params["end"] = endTime
    resp = requests.get(f"{JAEGER_URL}/api/v3/traces/{traceId}", params=params)
    resp.raise_for_status()
    return resp.json().get("data", [])

@mcp.tool(name="find_traces", description="Search for traces by parameters")
def find_traces(service: str, operation: str = None, startTime: str = None, endTime: str = None) -> list[dict]:
    payload = {"service": service}
    if operation: payload["operation"] = operation
    if startTime: payload["start"] = startTime
    if endTime: payload["end"] = endTime
    resp = requests.post(f"{JAEGER_URL}/api/v3/traces", json=payload)
    resp.rasie_for_status()
    return resp.json().get("data", [])

if __name__ == "__main__":
    mcp.run(transport=f"{LISTENING_PROTOCOL}", host=f"{LISTENING_IP}", port=f"{LISTENING_PORT}", path="/mcp")
