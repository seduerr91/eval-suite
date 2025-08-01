import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
import json
import os
import sys

from src.data_loader import load_data
from src.evaluation import run_evaluation
from src.schemas.models import EvaluationResult

class TestFullFlow(unittest.TestCase):

    def setUp(self):
        # Create a dummy data directory and test.json file
        self.test_data_dir = os.path.join(os.path.dirname(__file__), 'temp_data')
        os.makedirs(self.test_data_dir, exist_ok=True)
        self.test_file_path = os.path.join(self.test_data_dir, 'test.json')

        dummy_data = [
            {"patient_convo": "Patient feels dizzy.", "soap_notes": "S: Dizzy..."}
        ]
        with open(self.test_file_path, 'w') as f:
            json.dump(dummy_data, f)

        # Patch the path to the data file to use our dummy data
        self.path_patcher = patch('data_loader.os.path.join')
        self.mock_path_join = self.path_patcher.start()
        self.mock_path_join.return_value = self.test_file_path

    def tearDown(self):
        # Clean up the dummy data
        os.remove(self.test_file_path)
        os.rmdir(self.test_data_dir)
        self.path_patcher.stop()

    @patch('data_loader.generate_note')
    @patch('evaluation.evaluate')
    def test_load_and_evaluate(self, mock_evaluate, mock_generate_note):
        # Arrange
        mock_generate_note.return_value = 'AI generated note.'

        mock_metric_data = [
            MagicMock(name='Hallucination', score=0.1),
            MagicMock(name='Contextual Recall', score=0.9),
            MagicMock(name='Clinical Accuracy [GEval]', score=0.8),
            MagicMock(name='SOAP Structure Compliance [GEval]', score=1.0),
            MagicMock(name='Clinical Safety Assessment [GEval]', score=0.7),
            MagicMock(name='Medical Terminology Accuracy [GEval]', score=0.85)
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
        self.assertEqual(results[0].note.transcript, 'Patient feels dizzy.')
        self.assertEqual(results[0].overall_score, (0.1 + 0.9 + 0.8 + 1.0 + 0.7 + 0.85) / 6)

if __name__ == '__main__':
    unittest.main()
