from src.utils import dynamic_import
from typing import Dict, Any

class ComponentFactory:
    @staticmethod
    def create_component(module_name: str, class_name: str, params: Dict[str, Any]) -> Any:
        """
        Create an instance of a component with the given parameters.
        """
        cls = dynamic_import(module_name, class_name)
        for key, value in params.items():
            if isinstance(value, dict) and 'module' in value and 'class' in value:
                params[key] = ComponentFactory.create_component(value['module'], value['class'], value.get('params', {}))
        return cls(**params)