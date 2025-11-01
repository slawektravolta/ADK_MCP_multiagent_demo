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

if __name__ == "__main__":
    app.run()