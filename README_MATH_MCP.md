Real MCP “Wheather + Math” Server (FastMCP) + Agents
---------------------------------------------------

Co zawiera ten katalog
- `mcp_wheather_math_server_fast.py`: serwer MCP (FastMCP) z narzędziami pogodowo‑obliczeniowymi:
  - `dew_point(temp_c, humidity)` – punkt rosy (Magnus), °C
  - `heat_index(temp_c, humidity)` – temperatura odczuwalna (NOAA), °C
  - `beaufort_scale(wind_speed_kmh)` – stopień skali Beauforta (0–12)
  - `c_to_f(celsius)` – konwersja °C → °F
  - `average(values: list[float])` – średnia z listy
  - `min_max(values: list[float])` – słownik `{min, max}`
- `wheather_math_agent.py`: agent ADK z MCPToolset (ADK‑native), łączy się z serwerem MCP przez stdio.
- `agent.py`: agent główny (root) z lokalnymi narzędziami (czas/pogoda). Opcjonalnie dołącza pod‑agenta jako „Agent‑as‑a‑Tool”, jeśli klasa `AgentTool` jest dostępna.

Instalacja
- Zainstaluj MCP SDK w tej samej wirtualnej env co ADK Web: `pip install mcp`
- Upewnij się, że masz ADK z modułem `google.adk` oraz klasą `MCPToolset` i (opcjonalnie) `AgentTool`.

Uruchomienie serwera ręcznie (opcjonalne)
- `python -m multi_tool_agent.mcp_wheather_math_server_fast`
- Serwer działa na stdio; MCPToolset może go sam uruchamiać przy starcie agenta.

Użycie w agentach (ADK‑native)
- `wheather_math_agent.py` tworzy MCPToolset:
  - Komenda: `sys.executable`
  - Argumenty: `-m multi_tool_agent.mcp_wheather_math_server_fast`
  - Następnie przekazuje `[_mcp_wheather_math_toolset]` w `tools` – LLM widzi narzędzia MCP jak zwykłe toolsy.
- `agent.py` (root): zawiera lokalne narzędzia (czas/pogoda). Jeżeli środowisko ma `AgentTool`, root dołącza pod‑agenta jako narzędzie (agent‑as‑a‑tool).

Wskazówki
- STDIO jest najprostszym transportem MCP w dev.
- Ograniczanie narzędzi: użyj `tool_filter` w `MCPToolset`, aby udostępniać tylko wybrane metody.
- Jeżeli ADK Web „nie widzi” agentów, najczęściej brakuje pakietów (np. `mcp`) w tej samej env – doinstaluj zależności i przeładuj okno.
