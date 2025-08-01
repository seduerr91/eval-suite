# Clinical Note Evaluation Suite

This project provides a comprehensive suite for evaluating AI-generated clinical SOAP notes, which are structured medical documents used by healthcare providers to record patient information in a clear and organized manner.
It leverages `deepeval` to assess the quality of generated notes against a ground-truth dataset, providing a robust framework for ensuring clinical accuracy and safety.

## SOAP Note Structure

- **Subjective**: The patient's symptoms, complaints, and concerns.
- **Objective**: The physical examination findings and medical history.
- **Assessment**: The diagnosis and treatment plan.
- **Plan**: The treatment plan.

## Key Features

- **Automated Evaluation**: Measures the quality of clinical notes based on critical metrics.
- **Clinical Safety**: Identifies missing critical findings and hallucinated or unsupported facts.
- **Interactive Dashboard**: Visualizes evaluation results for in-depth analysis.
- **Extensible Framework**: Easily adaptable for different models and datasets.

## How It Works

The pipeline follows these steps:
1.  **Data Loading**: Loads patient conversations and ground-truth SOAP notes.
2.  **Note Generation**: Generates a clinical note from each conversation transcript using an LLM.
3.  **Evaluation**: Compares the generated note to the ground-truth note using `deepeval` (pypi).
4.  **Visualization**: Displays the results in an interactive Streamlit dashboard.

## Dashboard Overview

The interactive dashboard provides a comprehensive view of the evaluation results, with aggregate metrics and the ability to drill down into individual notes.

![Clinical AI Eval Dashboard Overview](docs/Clinical%20AI%20Eval%20Dashboard%20Overview.png)

## Tech Stack

- **Python** with `uv` for package management
- **`deepeval`** for LLM evaluation
- **`pydantic`** for data validation
- **`streamlit`** for the interactive dashboard
- **`just`** as a command runner
- **Docker** for containerization
- **Terraform** for infrastructure as code (AWS ECS)
- **`pre-commit`** for code quality
- ...

## Getting Started

### Prerequisites

Install the necessary tools using Homebrew:

```bash
# Install Just, Python, and other tools
brew install just python wget

# Install Docker and Terraform
brew install --cask docker
brew tap hashicorp/tap
brew install hashicorp/tap/terraform
```
*Note: Ensure Docker Desktop is running before proceeding.*

### Installation & Setup

1.  **Set up Environment Variables:**
    ```bash
    cp .env.template .env
    ```
    Fill in the required API keys in the `.env` file.

2.  **Install Dependencies:**
    ```bash
    just install
    ```

3.  **Download the Dataset:**
    This project uses a dedicated test set to ensure an unbiased evaluation.
    ```bash
    just setup-data
    ```

## Usage

1.  **Run Evaluations:**
    - For a small sample (2 notes):
      ```bash
      just run
      ```
    - For the full dataset:
      ```bash
      just run-full
      ```

2.  **Visualize Results:**
    Launch the interactive dashboard to explore the results:
    ```bash
    just dashboard
    ```

## Evaluation Frameworks Comparison

For a detailed comparison of various LLM evaluation frameworks and tools, please see the [Evaluation Suites Comparison](./docs/eval_suites_comparison.md) document. This was created to provide context and aid in the selection of the most appropriate tools.

## Next Steps

- Ensure transcripts fit into the context window or implement a chunking strategy.
- Deploy the service and integrate it with real-time processing of patient-provider conversations.
- Account for concepts such as model drift, data drift, and model selection/updates.

## Disclaimer

This evaluation pipeline was directed by Seb and utilized AI to generate code and documentation.
