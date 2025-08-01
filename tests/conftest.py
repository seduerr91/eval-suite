import os
import pytest
from unittest.mock import patch, MagicMock


# Set dummy API key for all tests
@pytest.fixture(autouse=True)
def mock_env_variables():
    with patch.dict(os.environ, {"OPENAI_API_KEY": "dummy-api-key-for-testing"}):
        yield


# Mock the OpenAI client for all tests
@pytest.fixture(autouse=True)
def mock_openai():
    mock_client = MagicMock()
    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message.content = "Mocked response"
    mock_client.chat.completions.create.return_value = mock_response

    with patch("openai.OpenAI", return_value=mock_client):
        yield mock_client


# Mock deepeval's evaluate function
@pytest.fixture(autouse=True)
def mock_deepeval_evaluate():
    mock_metric = MagicMock()
    mock_metric.name = "Mocked Metric"
    mock_metric.score = 0.9

    mock_test_result = MagicMock()
    mock_test_result.metrics_data = [mock_metric]

    mock_evaluation_output = MagicMock()
    mock_evaluation_output.test_results = [mock_test_result]

    with patch("deepeval.evaluate", return_value=mock_evaluation_output):
        yield mock_evaluation_output
