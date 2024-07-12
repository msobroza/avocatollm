import yaml
from pydantic import BaseModel, ValidationError
from typing import Dict, Any, List, Optional

class ComponentConfig(BaseModel):
    module: str
    class_: str
    params: Dict[str, Any]

    class Config:
        fields = {
            'class_': 'class'
        }

class DAGConfig(BaseModel):
    source: str
    destination: str
    source_key: Optional[str]
    dest_key: Optional[str]

class PipelineConfig(BaseModel):
    components: Dict[str, ComponentConfig]
    dag: List[DAGConfig]

class Config(BaseModel):
    pipeline: PipelineConfig

def load_config(config_path: str) -> Dict[str, Any]:
    """
    Load configuration from a YAML file.
    """
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
    return config

def validate_config(config_data: Dict[str, Any]) -> Config:
    """
    Validate the configuration data against the schema.
    """
    try:
        return Config(**config_data)
    except ValidationError as e:
        raise ValueError(f"Invalid configuration: {e}")

def create_arg_parser(config: Config):
    """
    Create an argument parser based on the configuration.
    """
    import argparse
    parser = argparse.ArgumentParser(description="Tune RAG Model")
    parser.add_argument('--config_path', type=str, required=True, help="Path to the configuration file")
    for name, component in config.pipeline.components.items():
        for param, value in component.params.items():
            parser.add_argument(f'--{name}_{param}', type=type(value), default=value, help=f'{param} for {name}')
    parser.add_argument('--dataset_dir', type=str, default="./data", help="Directory for the dataset")
    parser.add_argument('--chunk_size', type=int, default=512, help="Chunk size for splitting documents")
    parser.add_argument('--top_k', type=int, default=2, help="Top K similar nodes to retrieve")
    parser.add_argument('--dataset_name', type=str, default='pg_eval_dataset.json', help="Dataset name")
    parser.add_argument('--chunk_questions', type=int, default=1, help="Number of questions per chunk")
    return parser