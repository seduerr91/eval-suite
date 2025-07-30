# Justfile for the project

# Install dependencies using uv
install:
    uv pip install -r requirements.txt

# Download the dataset
setup-data:
    ./scripts/download_data.sh

# Run the main evaluation script on a small sample (5 notes)
run:
    uv run python -m src.main

# Run the main evaluation script on the full dataset
run-full:
    uv run python -m src.main --full

# Run the streamlit dashboard
dashboard:
    uv run streamlit run src/app.py

# Run tests
test:
    uv run pytest

# Set up a virtual environment with uv
env:
    uv venv .venv