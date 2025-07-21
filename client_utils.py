import asyncio
import time
import json
from typing import Optional, Tuple, List, Dict, Any

from fastmcp import Client
from fastmcp.client.transports import StreamableHttpTransport


transport = StreamableHttpTransport(url="http://127.0.0.1:8000/mcp/")
global_client = Client(transport=transport)


async def all_available_tools(client_name: Optional[str]) -> List[Any]:
    """
    Lists all available tools from MCP Server with optional filtering by client name
    and optional extraction of input schemas.

    Args:
        client_name: Optional client name prefix to filter tools.
        input_schema: If True, returns input schemas of the tools.

    Returns:
        A tuple containing the list of tools and (optionally) their input schemas.
    """
    async with global_client:
        start_time = time.time()
        tools = await global_client.list_tools()

        if client_name:
            tools = [tool for tool in tools if tool.name.startswith(client_name.lower())]

        end_time = time.time()
        total_time_ms = (end_time - start_time) * 1000
        print(f"Total client request time: {total_time_ms:.2f} ms")

        return tools


async def invoke_mcp_server(
    function_calls: List[Dict[str, Any]],
    client_name: Optional[str]
) -> List[Dict[str, Any]]:
    """
    Calls MCP Server tools concurrently based on given function calls.

    Args:
        function_calls: List of function call dicts with keys 'id', 'function'.
        client_name: Optional prefix to modify tool names.

    Returns:
        A list of result dictionaries mapping tool_id, name, and result.
    """
    async with global_client:
        tasks = []
        start_time = time.time()

        for tool_call in function_calls:
            tool_id = tool_call['id']
            func_data = tool_call['function']
            name = func_data['name']

            if client_name:
                name = f"{client_name.lower()}_{name}"

            args = func_data['arguments']

            if isinstance(args, str):
                args = json.loads(args)

            tasks.append(global_client.call_tool(name, args, raise_on_error=False))

        results_raw = await asyncio.gather(*tasks)
        end_time = time.time()
        total_time_ms = (end_time - start_time) * 1000
        print(f"Total invocation time: {total_time_ms:.2f} ms")

        # Mapping tool_id, name, and result
        results = []
        for idx, tool_call in enumerate(function_calls):
            result_entry = {
                "tool_id": tool_call['id'],
                "name": (f"{client_name.lower()}_" if client_name else "") + tool_call['function']['name'],
                "result": results_raw[idx].data
            }
            results.append(result_entry)

        return results
