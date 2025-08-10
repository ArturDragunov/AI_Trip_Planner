
---

# Tool Architecture Guide

All tools follow the **same structure** for consistency and maintainability:

## 1. **Purpose**

Each tool is a wrapper around an external API.
Its job:

* Load API keys from `.env`
* Initialize the API service object
* Define one or more `@tool` functions
* Return these tools in a list for use in LangChain

---

## 2. **Structure**

```python
class ExampleTool:
    def __init__(self):
        load_dotenv()
        self.api_key = os.environ.get("API_KEY_NAME")
        self.service = ExternalService(self.api_key)
        self.tool_list = self._setup_tools()

    def _setup_tools(self) -> List:
        @tool
        def example_tool_function(param1: str):
            """Description of what the tool does"""
            return self.service.some_method(param1)

        return [example_tool_function]
```

---

## 3. **Key Principles**

* **`_setup_tools`** → always define your `@tool` functions here.
* Each `@tool` function:

  * Has a **clear docstring** (LangChain uses this for descriptions).
  * Calls the service to fetch or process data.
  * Returns results in a clean, human-readable format.
* The `_setup_tools` method always returns a **list of tools**.
* Store API keys in `.env` — load them in `__init__`.

---

## 4. **Examples**

* **CurrencyConverterTool** → Converts currency via Exchange Rate API.
* **WeatherInfoTool** → Fetches current weather & forecast from OpenWeatherMap.

---
