from mcp.server.fastmcp import FastMCP
import statistics
import math

from mcp.server.fastmcp import FastMCP

# Tworzę serwer MCP z funkcjami meteorologicznymi
app = FastMCP("weather-analytics-mcp")

@app.tool(description="Oblicz punkt rosy (dew point) na podstawie temperatury i wilgotności")
def dew_point(temp_c: float, humidity: float) -> float:
    """Zwraca punkt rosy w °C zgodnie z przybliżonym wzorem Magnusa."""
    a, b = 17.27, 237.7
    alpha = (a * temp_c / (b + temp_c)) + math.log(humidity / 100)
    return round((b * alpha) / (a - alpha), 2)

@app.tool(description="Oblicz odczuwalną temperaturę (heat index) na podstawie temperatury i wilgotności")
def heat_index(temp_c: float, humidity: float) -> float:
    """Zwraca odczuwalną temperaturę w °C zgodnie z równaniem NOAA."""
    t = temp_c
    rh = humidity
    hi = 0.5 * (t + 61.0 + ((t - 68.0) * 1.2) + (rh * 0.094))
    if hi >= 80:
        hi = -8.784695 + 1.61139411 * t + 2.338549 * rh - 0.14611605 * t * rh
    return round(hi, 2)

@app.tool(description="Oblicz prędkość wiatru w skali Beauforta")
def beaufort_scale(wind_speed_kmh: float) -> int:
    """Zwraca przybliżony stopień w skali Beauforta dla danej prędkości wiatru (km/h)."""
    thresholds = [1, 6, 12, 20, 29, 39, 50, 62, 75, 89, 103, 118]
    for i, t in enumerate(thresholds):
        if wind_speed_kmh < t:
            return i
    return 12

@app.tool(description="Convert Celsius to Fahrenheit")
def c_to_f(celsius: float) -> float:
    return (celsius * 9 / 5) + 32

@app.tool(description="Compute average of a list of numbers")
def average(values: list[float]) -> float:
    return statistics.mean(values)

@app.tool(description="Find min and max of a list of numbers")
def min_max(values: list[float]) -> dict:
    return {"min": min(values), "max": max(values)}

_RESOURCE_STORE = {
    "mem://kb/weather/tips": {"mime": "text/markdown", "content": "# Tips..."},
    "mem://kb/weather/constants": {"mime": "application/json", "content": {"k": 273.15}},
}
_PROMPTS = {
    "warn_heat": {"template": "Write a short heat warning for T={t}°C and RH={rh}%"}
}

@app.tool(description="List available resource URIs")
def list_resources() -> list[str]:
    return list(_RESOURCE_STORE.keys())

@app.tool(description="Get resource by URI (returns {uri,mime,content})")
def get_resource(uri: str) -> dict:
    if uri not in _RESOURCE_STORE:
        raise ValueError("Unknown resource")
    return {"uri": uri, **_RESOURCE_STORE[uri]}

@app.tool(description="Render a named prompt with args")
def render_prompt(name: str, args: dict) -> str:
    if name not in _PROMPTS:
        raise ValueError("Unknown prompt")
    return _PROMPTS[name]["template"].format(**args)

if __name__ == "__main__":
    app.run()