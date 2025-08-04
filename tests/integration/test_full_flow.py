import unittest
from unittest.mock import patch, MagicMock
import json
import os

from src.data_loader import load_data
from src.evaluation import run_evaluation
from src.schemas.models import EvaluationResult


class TestFullFlow(unittest.TestCase):

    def setUp(self):
        # Create a dummy data directory and test.json file
        self.test_data_dir = os.path.join(os.path.dirname(__file__), "temp_data")
        os.makedirs(self.test_data_dir, exist_ok=True)
        self.test_file_path = os.path.join(self.test_data_dir, "test.json")

        dummy_data = [
            {"patient_convo": "Patient feels dizzy.", "soap_notes": "S: Dizzy..."}
        ]
        with open(self.test_file_path, "w") as f:
            json.dump(dummy_data, f)

        # Patch the path to the data file to use our dummy data
        self.path_patcher = patch("src.data_loader.os.path.join")
        self.mock_path_join = self.path_patcher.start()
        self.mock_path_join.return_value = self.test_file_path

    def tearDown(self):
        # Clean up the dummy data
        os.remove(self.test_file_path)
        os.rmdir(self.test_data_dir)
        self.path_patcher.stop()

    @patch("openai.OpenAI")
    @patch("src.evaluation.evaluate")
    @patch("src.data_loader.generate_note")
    def test_load_and_evaluate(self, mock_generate_note, mock_evaluate, mock_openai):
        # Arrange
        mock_generate_note.return_value = "AI generated note."

        # Create mock metrics with exact names that match what run_evaluation looks for
        mock_hallucination = MagicMock()
        mock_hallucination.name = "Hallucination"
        mock_hallucination.score = 0.1

        mock_accuracy = MagicMock()
        mock_accuracy.name = "Clinical Accuracy [GEval]"
        mock_accuracy.score = 0.8

        mock_soap = MagicMock()
        mock_soap.name = "SOAP Structure Compliance [GEval]"
        mock_soap.score = 1.0

        mock_safety = MagicMock()
        mock_safety.name = "Clinical Safety Assessment [GEval]"
        mock_safety.score = 0.7

        mock_terminology = MagicMock()
        mock_terminology.name = "Medical Terminology Accuracy [GEval]"
        mock_terminology.score = 0.85

        mock_metric_data = [
            mock_hallucination,
            mock_accuracy,
            mock_soap,
            mock_safety,
            mock_terminology,
        ]
        mock_test_result = MagicMock(metrics_data=mock_metric_data)
        mock_evaluation_output = MagicMock(test_results=[mock_test_result])
        mock_evaluate.return_value = mock_evaluation_output

        # Act
        notes = load_data()
        results = run_evaluation(notes)

        # Assert
        self.assertEqual(len(results), 1)
        self.assertIsInstance(results[0], EvaluationResult)
        self.assertEqual(results[0].note.transcript, "Patient feels dizzy.")
        self.assertAlmostEqual(
            results[0].overall_score, (0.1 + 0.8 + 1.0 + 0.7 + 0.85) / 5
        )


if __name__ == "__main__":
    unittest.main()
