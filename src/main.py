import argparse
import asyncio
import mlflow
import nest_asyncio
import warnings
from typing import Any

from src.data import DataLoader, DataPreprocessor
from src.llamaindex_pipeline import LlamaIndexRAGPipeline
from src.trainer import Trainer, Evaluator
from src.utils import Logger
from src.config_loader import load_config, create_arg_parser, validate_config

nest_asyncio.apply()
warnings.filterwarnings('ignore')

def main():
    parser = argparse.ArgumentParser(description="Tune RAG Model")
    parser.add_argument('--config_path', type=str, required=True, help="Path to the configuration file")
    args = parser.parse_args()

    config_data = load_config(args.config_path)
    config = validate_config(config_data)

    parser = create_arg_parser(config)
    args = parser.parse_args()

    logger = Logger.get_logger(__name__)

    # Load and preprocess data
    data_loader = DataLoader(data_dir=args.dataset_dir)
    documents = data_loader.load_data()
    data_preprocessor = DataPreprocessor(chunk_size=args.chunk_size)
    nodes = data_preprocessor.preprocess(documents)

    # Initialize pipeline with config
    pipeline = LlamaIndexRAGPipeline(config=config.dict(), args=args)
    
    constructed_pipeline = pipeline.get_pipeline()
    modules = pipeline.get_modules()
    llm = modules['llm']  # Assuming the first module is the LLM

    # Generate QA dataset
    from llama_index.core.evaluation import generate_question_context_pairs, EmbeddingQAFinetuneDataset
    qa_dataset = generate_question_context_pairs(
        nodes, llm=llm, num_questions_per_chunk=args.chunk_questions
    )

    qa_dataset.save_json(args.dataset_name)
    qa_dataset = EmbeddingQAFinetuneDataset.from_json(args.dataset_name)

    # Evaluate
    evaluator = Evaluator(retriever=modules['retriever'], metrics=["mrr", "hit_rate"])
    eval_results = await evaluator.evaluate(qa_dataset)
    hit_rate = eval_results["hit_rate"].mean()
    mrr = eval_results["mrr"].mean()

    # Log results
    trainer = Trainer(model=constructed_pipeline, data=nodes)
    trainer.log_results(hit_rate, mrr, vars(args), [args.dataset_name])

if __name__ == "__main__":
    asyncio.run(main())
