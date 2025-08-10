import os
from dotenv import load_dotenv
from typing import Literal, Optional, Any
from pydantic import BaseModel, Field
from utils.config_loader import load_config
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI


class ConfigLoader:
    def __init__(self):
        print("Loaded config.....")
        self.config = load_config()
    
    def __getitem__(self, key):
    # Called when you use square brackets [] to access an item from an object    
    # class MyConfig:
    # def __init__(self):
    #     self.config = {'mode': 'test'}

    # def __getitem__(self, key):
    #     return self.config[key]

    # cfg = MyConfig()
    # print(cfg['mode'])  # Calls cfg.__getitem__('mode') → returns 'test'
        return self.config[key]

class ModelLoader(BaseModel): # pydantic is like a dataclass. it doesn't need __init__. This class is just a data holder
    model_provider: Literal["groq", "openai"] = "openai"
    config: Optional[ConfigLoader] = Field(default=None, exclude=True)

    def model_post_init(self, __context: Any) -> None: 
        # load configuration
        self.config = ConfigLoader() # we define an object and then we treat it as a list/dict etc.
        # -> we can use [] because ConfigLoader has def __getitem__ method defined inside.
    # What is model_post_init?
    # This is a special Pydantic v2 hook (similar to a __post_init__ in dataclasses) that runs after the model is initialized.
    # It's where you can do additional setup (e.g., inject dependencies, load config files, etc.) without needing to write a custom __init__.
    
    # pydantic calls model_post_init with __context, thus we need to accept it
    # It's an optional value passed internally by Pydantic, containing information like the validation context or dependencies.
    class Config: # Pydantic uses the inner Config class to customize model behavior.
        arbitrary_types_allowed = True # allows Pydantic to accept non-Pydantic types, like your custom ConfigLoader, as valid field types.
    # Why it's needed:
    # By default, Pydantic expects fields to be:
    # basic Python types (like int, str, list, etc.)
    # or other Pydantic models.
    # Since ConfigLoader is a plain class (not a Pydantic model), this config option tells Pydantic:
    # "Hey, it's okay — I know this field isn't a Pydantic type, but allow it anyway."    
    def load_llm(self):
        """
        Load and return the LLM model.
        """
        print("LLM loading...")
        print(f"Loading model from provider: {self.model_provider}")
        if self.model_provider == "groq":
            print("Loading LLM from Groq..............")
            groq_api_key = os.getenv("GROQ_API_KEY")
            model_name = self.config["llm"]["groq"]["model_name"]
            llm=ChatGroq(model=model_name, api_key=groq_api_key)
        elif self.model_provider == "openai":
            print("Loading LLM from OpenAI..............")
            openai_api_key = os.getenv("OPENAI_API_KEY")
            model_name = self.config["llm"]["openai"]["model_name"]
            llm = ChatOpenAI(model_name=model_name, api_key=openai_api_key)
        
        return llm
    