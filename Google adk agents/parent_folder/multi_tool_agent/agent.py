import datetime
from zoneinfo import ZoneInfo

# Biblioteca fictícia utilizada pela Google ADK. Mantemos a mesma importação para compatibilidade.
from google.adk.agents import Agent

# ---------------------------------------------------------------------------
# Dados estáticos de exemplo
# ---------------------------------------------------------------------------

# Mapas de exemplo contendo algumas cidades brasileiras (e Nova Iorque para
# compatibilidade com a versão anterior). Caso deseje informações em tempo
# real basta substituir essas estruturas por chamadas a APIs externas.

WEATHER_DATA: dict[str, str] = {
    # Brasil
    "são paulo": "O clima em São Paulo está parcialmente nublado com temperatura de 27 °C.",
    "sao paulo": "O clima em São Paulo está parcialmente nublado com temperatura de 27 °C.",
    "rio de janeiro": "O clima no Rio de Janeiro está ensolarado com temperatura de 30 °C.",
    "brasília": "O clima em Brasília está ensolarado com temperatura de 26 °C.",
    "brasilia": "O clima em Brasília está ensolarado com temperatura de 26 °C.",
    "salvador": "O clima em Salvador está chuvoso com temperatura de 24 °C.",
    "manaus": "O clima em Manaus está nublado com temperatura de 29 °C.",
    "sinop": "O clima em Sinop está quente e ensolarado com temperatura de 32 °C.",
    

    # Estados Unidos – exemplo legado
    "new york": "The weather in New York is sunny with a temperature of 25 °C (77 °F).",
}

# Identificadores de timezone compatíveis com o módulo zoneinfo do Python 3.9+
TIMEZONE_MAP: dict[str, str] = {
    # Brasil (alguns exemplos)
    "são paulo": "America/Sao_Paulo",
    "sao paulo": "America/Sao_Paulo",
    "rio de janeiro": "America/Sao_Paulo",
    "brasília": "America/Sao_Paulo",
    "brasilia": "America/Sao_Paulo",
    "salvador": "America/Bahia",
    "manaus": "America/Manaus",
    "sinop": "America/Cuiaba",

    # Estados Unidos – exemplo legado
    "new york": "America/New_York",
}


# ---------------------------------------------------------------------------
# Ferramentas (functions) disponibilizadas ao agente
# ---------------------------------------------------------------------------


def get_weather(city: str) -> dict:
    """Obtém um relatório de clima para a cidade informada.

    Args:
        city: Nome da cidade.

    Returns:
        Um dicionário no formato {"status": "success", "report": str} ou
        {"status": "error", "error_message": str}.
    """

    report = WEATHER_DATA.get(city.lower())
    if report:
        return {"status": "success", "report": report}

    return {
        "status": "error",
        "error_message": f"Desculpe, não possuo informações de clima para '{city}'.",
    }


def get_current_time(city: str) -> dict:
    """Retorna a hora atual na cidade informada.

    Args:
        city: Nome da cidade.

    Returns:
        Um dicionário no formato {"status": "success", "report": str} ou
        {"status": "error", "error_message": str}.
    """

    tz_identifier = TIMEZONE_MAP.get(city.lower())
    if not tz_identifier:
        return {
            "status": "error",
            "error_message": f"Desculpe, não possuo informações de fuso horário para '{city}'.",
        }

    tz = ZoneInfo(tz_identifier)
    now = datetime.datetime.now(tz)
    report = (
        f"A hora atual em {city} é {now.strftime('%Y-%m-%d %H:%M:%S %Z%z')}"
    )
    return {"status": "success", "report": report}


# ---------------------------------------------------------------------------
# Definição do agente raiz
# ---------------------------------------------------------------------------

root_agent = Agent(
    name="agente_clima_horario",
    model="gemini-2.0-flash",
    description="Agente para responder perguntas sobre horário e clima em uma cidade.",
    instruction="Você é um agente prestativo que pode responder perguntas sobre horário e clima em uma cidade.",
    tools=[get_weather, get_current_time],
)