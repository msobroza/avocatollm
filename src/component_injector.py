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
            params = self._update_params(component.params, name)
            components[name] = ComponentFactory.create_component(component.module, component.class_, params)
        return components

    def _update_params(self, params: Dict[str, Any], component_name: str) -> Dict[str, Any]:
        """
        Update parameters based on command-line arguments.
        """
        for key, value in self.args.__dict__.items():
            if key.startswith(f'{component_name}__'):
                # Split the argument name into parts
                parts = key.split('__')
                # Remove the component name part
                parts.pop(0)
                # Recursively update the nested parameter
                self._set_nested_param(params, parts, value)
        return params

    def _set_nested_param(self, params: Dict[str, Any], parts: list, value: Any):
        """
        Recursively set the nested parameter.
        """
        part = parts.pop(0)
        if len(parts) == 0:
            params[part] = value
        else:
            if part not in params:
                params[part] = {}
            self._set_nested_param(params[part], parts, value)

