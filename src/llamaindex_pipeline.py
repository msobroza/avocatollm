from llama_index.core import QueryPipeline
from src.pipeline import RAGPipeline
from src.component_injector import PipelineComponentInjector
from typing import Any, Dict

class LlamaIndexRAGPipeline(RAGPipeline):
    def __init__(self, config: Dict[str, Any] = None, args: Any = None):
        self.pipeline = QueryPipeline(verbose=True)
        super().__init__(config=config, args=args)

    def _build_pipeline(self):
        """
        Build the LlamaIndex pipeline by adding modules and links.
        """
        injector = PipelineComponentInjector(self.config, self.args)
        self.modules = injector.inject_components()

        for name, module in self.modules.items():
            self.pipeline.add_modules({name: module})
        self._add_links()

    def _add_links(self):
        """
        Add links between modules in the pipeline based on configuration.
        """
        for link in self.config['pipeline']['dag']:
            self.pipeline.add_link(
                link['source'], 
                link['destination'], 
                source_key=link.get('source_key'), 
                dest_key=link.get('dest_key')
            )

    def add_module(self, name: str, module: Any):
        """
        Add a module to the pipeline.
        """
        self.pipeline.add_modules({name: module})
        self.modules[name] = module

    def add_link(self, source: str, destination: str, source_key: str = None, dest_key: str = None):
        """
        Add a link between modules in the pipeline.
        """
        self.pipeline.add_link(source, destination, source_key=source_key, dest_key=dest_key)

    def get_pipeline(self) -> QueryPipeline:
        """
        Get the constructed pipeline.
        """
        return self.pipeline
