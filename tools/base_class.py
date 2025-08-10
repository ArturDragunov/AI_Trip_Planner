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
        """
        Override this method to define @tool functions.
        Must return a list of tool functions.
        """
        raise NotImplementedError("Subclasses must implement _setup_tools()")
