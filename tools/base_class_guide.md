
---

````markdown
# Tool Development Guide

This repo uses a **BaseAPITool** pattern so all tools follow the same architecture.

---

## 1. Pattern Overview

All tools:
- Load API keys from `.env`
- Initialize a service class that talks to the API
- Define one or more `@tool` functions inside `_setup_tools`
- Return the tools in a list

The **BaseAPITool** handles:
- `.env` loading
- API key retrieval
- Service class initialization

---

## 2. Base Class

```python
import os
from typing import List
from dotenv import load_dotenv

class BaseAPITool:
    def __init__(self, api_key_env: str, service_class):
        """
        Base class for API-powered LangChain tools.

        :param api_key_env: Name of the environment variable for API key.
        :param service_class: The class that handles API communication.
        """
        load_dotenv()
        self.api_key = os.environ.get(api_key_env)
        if not self.api_key:
            raise ValueError(f"API key not found for {api_key_env}")
        
        self.service = service_class(self.api_key)
        self.tool_list = self._setup_tools()

    def _setup_tools(self) -> List:
        """Override this to define @tool functions and return them in a list."""
        raise NotImplementedError
````

---

## 3. How to Create a New Tool

### Step 1: Subclass `BaseAPITool`

* Provide the environment variable name for your API key
* Provide the API service class

### Step 2: Override `_setup_tools`

* Define all your `@tool` functions inside
* Return them as a list

---

## 4. Example: Currency Converter

```python
from langchain.tools import tool
from utils.currency_converter import CurrencyConverter

class CurrencyConverterTool(BaseAPITool):
    def __init__(self):
        super().__init__("EXCHANGE_RATE_API_KEY", CurrencyConverter)

    def _setup_tools(self):
        @tool
        def convert_currency(amount: float, from_currency: str, to_currency: str):
            """Convert amount from one currency to another."""
            return self.service.convert(amount, from_currency, to_currency)
        return [convert_currency]
```

---

## 5. Example: Weather Info

```python
from langchain.tools import tool
from utils.weather_info import WeatherForecastTool

class WeatherInfoTool(BaseAPITool):
    def __init__(self):
        super().__init__("OPENWEATHERMAP_API_KEY", WeatherForecastTool)

    def _setup_tools(self):
        @tool
        def get_current_weather(city: str):
            """Get current weather for a city."""
            data = self.service.get_current_weather(city)
            if not data:
                return f"Could not fetch weather for {city}"
            temp = data.get('main', {}).get('temp', 'N/A')
            desc = data.get('weather', [{}])[0].get('description', 'N/A')
            return f"Current weather in {city}: {temp}°C, {desc}"

        @tool
        def get_weather_forecast(city: str):
            """Get weather forecast for a city."""
            forecast = self.service.get_forecast_weather(city)
            if not forecast or 'list' not in forecast:
                return f"Could not fetch forecast for {city}"
            return "\n".join([
                f"{item['dt_txt'].split(' ')[0]}: {item['main']['temp']}°C, {item['weather'][0]['description']}"
                for item in forecast['list']
            ])

        return [get_current_weather, get_weather_forecast]
```

---

## 6. Summary

When creating a new tool:

1. **Subclass `BaseAPITool`**
2. **Override `_setup_tools`** → define `@tool` functions
3. **Return them in a list**

✅ Consistent structure
✅ Easy to maintain
✅ Minimal boilerplate
