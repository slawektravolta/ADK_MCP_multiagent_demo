import sys
from typing import Any, cast

from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from mcp.client.stdio import StdioServerParameters

def _build_toolset() -> MCPToolset:
    return MCPToolset(
        connection_params=StdioConnectionParams(
            server_params=StdioServerParameters(
                command=sys.executable,
                args=["-m", "multi_tool_agent.mcp_wheather_math_server_fast"],
            )
        ),
        # tool_filter=["dew_point","heat_index","beaufort_scale","c_to_f"],
    )

_mcp_wheather_math_toolset = _build_toolset()

# ↓ przerwanie cyklu typów: traktuj toolset jako Any dla Pylance
_tools: list[Any] = [cast(Any, _mcp_wheather_math_toolset)]

wheather_math_agent = LlmAgent(
    name="wheather_math_agent",
    model=LiteLlm(model="openai/gpt-4o-mini"),
    description="Agent specialized in weather arithmetic via MCPToolset.",
    instruction="Use MCP tools (dew_point, heat_index, beaufort_scale, c_to_f). Return only numeric results where relevant.",
    tools=_tools,
)
