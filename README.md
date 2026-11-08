# langchain-course: rama `search-agent`

Agente de LangChain que contesta con Gemini (`gemini-3.5-flash-lite`) y busca en internet con Tavily. Todo el código está en `main.py`, y por ahora le manda una sola pregunta escrita directo en el código: buscar 3 vacantes de AI engineer con LangChain en Monterrey.

## Cómo correrlo

Necesitas [uv](https://docs.astral.sh/uv/) y Python 3.12 (uv lo instala si te falta).

```powershell
uv sync
uv run main.py
```

Ojo con `uv run langchain-course`: ese comando apunta a `src/langchain_course/__init__.py`, que sigue siendo la plantilla de uv y solo imprime un saludo.

## Qué va en el `.env`

Crea un `.env` en la raíz del repo. Git lo ignora, así que al clonar de nuevo tendrás que volver a crearlo.

```env
# Obligatorias
GOOGLE_API_KEY=tu_api_key_de_google
TAVILY_API_KEY=tu_api_key_de_tavily

# Opcionales, para ver las trazas en LangSmith
LANGSMITH_TRACING=true
LANGSMITH_ENDPOINT=https://api.smith.langchain.com
LANGSMITH_API_KEY=tu_api_key_de_langsmith
LANGSMITH_AGENT_ID=tu_agent_id
LANGSMITH_AGENT_ENVIRONMENT=tu_environment
```

`ChatGoogleGenerativeAI` toma `GOOGLE_API_KEY` y `TavilySearch` toma `TAVILY_API_KEY`, ambas del entorno, por eso `load_dotenv()` va antes de crearlos. Las `LANGSMITH_*` las tienes en tu `.env` actual, pero `main.py` no lee ninguna directamente.

## Cómo funciona

`create_agent` recibe el modelo y la lista de tools, y el modelo decide cuándo llamar a la búsqueda. `agent.invoke()` devuelve un diccionario con toda la conversación, incluidas las llamadas a tools, y la respuesta final es el último mensaje:

```python
result["messages"][-1].text
```

Usa `.text` en lugar de `.content`, porque con Gemini `.content` puede llegar como una lista de bloques en vez de un string.

## Las dos versiones de la búsqueda

La versión actual usa `TavilySearch` de `langchain-tavily`, ya lista para pasarse como tool.

La primera versión era una tool escrita a mano con `@tool` sobre `TavilyClient`. Sigue en el commit `825b57c`, y la ves con:

```powershell
git show 825b57c:main.py
```

## Pendientes

- Quitar el import de `tool` en `main.py`, que ya no se usa desde el cambio a `TavilySearch`.
- Sacar la pregunta del código para poder pasarla como argumento.
