# LangChain Course

This branch contains a small Python project for practicing LangChain
integrations. The main example uses Google Gemini to generate a short summary
and two interesting facts from a block of information.

## Requirements

- Python 3.12 or newer
- [uv](https://docs.astral.sh/uv/)
- A Google Gemini API key
- A LangSmith API key (optional, for tracing)

The required Python version is recorded in [.python-version](./.python-version).

## Setup

From the `langchain-course` directory, install the project dependencies:

```powershell
uv sync
```

`uv` creates and uses the project virtual environment in `.venv`.

## Environment variables

Create a file named `.env` in the project root, next to `main.py` and
`pyproject.toml`:

```env
GOOGLE_API_KEY=your_google_gemini_api_key_here

# Optional LangSmith tracing
LANGSMITH_TRACING=true
LANGSMITH_API_KEY=your_langsmith_api_key_here
LANGSMITH_PROJECT=your_langsmith_project_name
```

The application calls `load_dotenv()` when it starts, so the variable is
available to `ChatGoogleGenerativeAI`. Replace the placeholder with your real
key, but never commit or share the real value. The `.gitignore` file already
excludes `.env`.

When LangSmith tracing is enabled, LangChain sends the application's traces to
the LangSmith project specified by `LANGSMITH_PROJECT`. Set
`LANGSMITH_TRACING=false` when you do not want to send traces.

The minimum `.env` for the main example is:

```env
GOOGLE_API_KEY=your_google_gemini_api_key_here
```

The complete `.env` template, including optional LangSmith tracing, is:

```env
GOOGLE_API_KEY=your_google_gemini_api_key_here
LANGSMITH_TRACING=true
LANGSMITH_API_KEY=your_langsmith_api_key_here
LANGSMITH_PROJECT=your_langsmith_project_name
```

## Running the main example

Run the application through `uv` so it uses the dependencies from `.venv`:

```powershell
uv run python main.py
```

The program creates a `PromptTemplate`, sends the information about a person
to the `gemini-3.5-flash-lite` model, and prints the generated response.

## Debugging

To debug `main.py` in VS Code:

1. Select the project interpreter from `.venv\Scripts\python.exe`.
2. Open `main.py` and add a breakpoint.
3. Open **Run and Debug** and start the Python debugger, or press `F5`.

If you prefer to start the program from the terminal and attach VS Code:

```powershell
uv run python -m debugpy --listen 5678 --wait-for-client main.py
```

Then attach a Python debugger to `localhost:5678`.

## Exercise

`Exercise/example.py` is a separate educational exercise about LangChain-Groq
model switching. It uses mock classes and does not make a real Groq request.
The exercise includes a TODO for setting the `GROQ_API_KEY` environment
variable:

```python
def implement_set_api_key(api_key):
    os.environ["GROQ_API_KEY"] = api_key
```

Run it with:

```powershell
uv run python Exercise/example.py
```

## Project structure

```text
langchain-course/
├── .env                  # Local API keys; never commit
├── .python-version       # Required Python version
├── Exercise/
│   └── example.py        # Mock Groq model-switching exercise
├── main.py               # Gemini/LangChain example
├── pyproject.toml        # Project metadata and dependencies
├── README.md             # Project documentation
├── src/
│   └── langchain_course/
│       └── __init__.py   # Package entry point
└── uv.lock               # Locked dependency versions
```

## Security notes

- Keep API keys only in `.env` or another local secret store.
- Do not paste real keys into source files, commits, screenshots, or chat.
- If a key is exposed, revoke it and create a replacement.
