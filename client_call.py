from client_utils import all_available_tools, invoke_mcp_server
import asyncio

if __name__ == "__main__":
    # Fetch all tools without filtering and without input schemas
    # result = asyncio.run(all_available_tools(client_name='nobroker'))
    # function_calls = [{"id": 1, "function": {"name": "send_property_detail_to_tenant", "arguments": {"propertyId": "8a9fae849707f8910197083521d60e85", "userId": "8a9ffe8389a7267c0189a76e333127d2", "message": "Enjoy"}}}, 
    #                   {"id": 2, "function": {"name": "send_property_detail_to_tenant", "arguments": {"propertyId": "8a9fae849707f8910197083521d60e85", "userId": "8a9ffe8389a7267c0189a76e333127d2", "message": "Enjoy"}}}]

    # result = asyncio.run(invoke_mcp_server(function_calls=function_calls, client_name="nobroker"))
    result = asyncio.run(all_available_tools(client_name=None))
    print(result)
