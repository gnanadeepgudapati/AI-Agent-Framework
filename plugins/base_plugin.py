from abc import ABC, abstractmethod 
from langchain_core.tools import BaseTool

class BasePlugin(ABC):
    """"
          Abstract base class for all service plugins.
    Every plugin (HRIS, ITSM, Facilities) must inherit from this.

   """

    @property
    @abstractmethod
    def name(self) -> str:
        """Name of the plugin."""
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        """Human-readable description of what this plugin handles."""
        pass
    
    @abstractmethod
    def get_tools(self) -> list[BaseTool]:
        """Returns all LangChain tools this plugin exposes to the agent.
        Every plugin must implement this."""
        pass
    def __repr__(self) -> str:
        return f"<Plugin: {self.name}>"