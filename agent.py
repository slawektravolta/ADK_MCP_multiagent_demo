import datetime
from zoneinfo import ZoneInfo
from typing import Any, Dict, TYPE_CHECKING

from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm
from google.adk.tools.agent_tool import AgentTool

if TYPE_CHECKING:
    # Tylko do typowania – nie uruchamia importów w czasie wykonania
    from google.adk.agents import LlmAgent as _LlmAgent

def get_weather(city: str) -> Dict[str, Any]:
    if city.lower() == "new york":
        return {"status": "success",
                "report": "The weather in New York is sunny with 25°C (77°F)."}
    return {"status": "error",
            "error_message": f"Weather information for '{city}' is not available."}

def get_current_time(city: str) -> Dict[str, Any]:
    if city.lower() != "new york":
        return {"status": "error",
                "error_message": f"Sorry, I don't have timezone information for {city}."}
    now = datetime.datetime.now(ZoneInfo("America/New_York"))
    return {"status": "success",
            "report": now.strftime("The current time in New York is %Y-%m-%d %H:%M:%S %Z%z")}

def _build_math_agent_tool() -> AgentTool:
    # Opóźniony import – dopiero tu wczytujemy sub-agenta.
    # WAŻNE: moduł 'wheather_math_agent' nie może importować 'multi_tool_agent.agent'.
    from .wheather_math_agent import wheather_math_agent as _math_subagent
    return AgentTool(agent=_math_subagent)

# Tworzymy narzędzie sub-agenta po definicjach funkcji
_wheather_math_agent_tool = _build_math_agent_tool()

root_agent = LlmAgent(
    name="weather_time_agent",
    model=LiteLlm(model="openai/gpt-4o-mini"),
    description="Answers time/weather; delegates arithmetic to math_agent.",
    instruction=(
        "Answer time and weather directly. For any arithmetic, call the 'math_agent' tool "
        "and return its result."
    ),
    tools=[get_weather, get_current_time, _wheather_math_agent_tool],
)