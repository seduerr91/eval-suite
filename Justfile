# Justfile for the project

# Install dependencies using uv
install:
    uv pip install -r requirements.txt

# Download the dataset
setup-data:
    ./scripts/download_data.sh

api:
    uv run python -m src.api

# Run the main evaluation script on a small sample (2 notes)
run:
    uv run python -m src.main

# Run the main evaluation script on the full dataset
run-full:
    uv run python -m src.main --full

# Run the streamlit dashboard
dashboard:
    uv run streamlit run src/dashboard.py

# Run tests
test:
    uv run pytest

# Set up a virtual environment with uv
env:
    uv venv .venv

# run pre-commit
pre-commit:
    uv run pre-commit run --all-files

# install pre-commit
pre-commit-install:
    uv run pre-commit install

# activate virtual environment
activate:
    source .venv/bin/activate

# clean Python cache files
clean:
    find . -type d -name "__pycache__" -exec rm -rf {} +;
    find . -name "*.pyc" -delete
    find . -name "*.pyo" -delete
    find . -name "*.pyd" -delete
    find . -name ".pytest_cache" -exec rm -rf {} +;
    find . -name "*.egg-info" -exec rm -rf {} +;
    find . -name "*.egg" -exec rm -rf {} +;
