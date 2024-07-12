from abc import ABC, abstractmethod
from typing import Any, Dict

class RAGPipeline(ABC):
    def __init__(self, config: Dict[str, Any] = None, args: Any = None):
        """
        Initialize the pipeline with configuration and arguments.
        """
        self.modules = {}
        if config:
            self.config = config
            self.args = args
            self._build_pipeline()

    @abstractmethod
    def _build_pipeline(self):
        """
        Abstract method to build the pipeline.
        """
        pass

    @abstractmethod
    def add_module(self, name: str, module: Any):
        """
        Add a module to the pipeline.
        """
        pass

    @abstractmethod
    def add_link(self, source: str, destination: str, source_key: str = None, dest_key: str = None):
        """
        Add a link between modules in the pipeline.
        """
        pass

    @abstractmethod
    def get_pipeline(self) -> Any:
        """
        Get the constructed pipeline.
        """
        pass

    def get_modules(self) -> Dict[str, Any]:
        """
        Get the instantiated modules in the pipeline.
        """
        return self.modules