import argparse
import json
import logging
import os

from src.core.config import settings
from src.core.logging_config import setup_logging
from src.data_loader import load_data
from src.evaluation import run_evaluation

os.environ["OPENAI_API_KEY"] = settings.OPENAI_API_KEY
os.environ["CONFIDENT_API_KEY"] = settings.CONFIDENT_API_KEY


def main():
    """Main function to run the evaluation suite."""
    setup_logging()

    parser = argparse.ArgumentParser(
        description="Run the clinical AI evaluation suite."
    )
    parser.add_argument(
        "--full", action="store_true", help="Run evaluation on the full dataset."
    )
    args = parser.parse_args()

    limit = None if args.full else 2
    logging.info(
        f"Loading data... (limit: {'full dataset' if limit is None else limit})"
    )
    notes = load_data(limit=limit)

    if not notes:
        logging.warning("No data found. Exiting.")
        return

    logging.info(f"Loaded {len(notes)} notes. Running evaluations...")
    evaluation_results = run_evaluation(notes)

    # Save results to a file for the dashboard - this would be replaced by a database if we'd run a daily pipeline or inference service
    output_path = "data/evaluation_results.json"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w") as f:
        # Pydantic models need to be converted to dicts for JSON serialization
        json.dump([result.model_dump() for result in evaluation_results], f, indent=4)

    logging.info(f"Evaluation complete. Results saved to {output_path}")


if __name__ == "__main__":
    main()
