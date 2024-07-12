from src.config_loader import Config, validate_config
from src.component_factory import ComponentFactory
from typing import Dict, Any

class PipelineComponentInjector:
    def __init__(self, config_data: Dict[str, Any], args: Any):
        """
        Initialize the component injector with configuration data and arguments.
        """
        self.config = validate_config(config_data)
        self.args = args

    def inject_components(self) -> Dict[str, Any]:
        """
        Inject dependencies and create component instances.
        """
        components = {}
        for name, component in self.config.pipeline.components.items():
            params = component.params
            if self.args:
                for param in params:
                    arg_value = getattr(self.args, f'{name}_{param}', None)
                    if arg_value is not None:
                        params[param] = arg_value
            components[name] = ComponentFactory.create_component(component.module, component.class_, params)
        return components
