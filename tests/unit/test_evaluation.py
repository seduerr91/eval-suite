import unittest
from unittest.mock import patch, MagicMock
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

from src.evaluation import run_evaluation
from src.schemas.models import ClinicalNote, EvaluationResult

class TestEvaluation(unittest.TestCase):

    @patch('evaluation.evaluate')
    def test_run_evaluation_success(self, mock_evaluate):
        # Arrange
        notes = [
            ClinicalNote(
                transcript='transcript1',
                note='ground_truth1',
                generated_note='generated1'
            )
        ]

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
        results = run_evaluation(notes)

        # Assert
        self.assertEqual(len(results), 1)
        self.assertIsInstance(results[0], EvaluationResult)
        self.assertEqual(results[0].hallucination_score, 0.1)
        self.assertAlmostEqual(results[0].overall_score, (0.1 + 0.9 + 0.8 + 1.0 + 0.7 + 0.85) / 6)

    @patch('evaluation.evaluate')
    def test_run_evaluation_no_results(self, mock_evaluate):
        # Arrange
        notes = [ClinicalNote(transcript='t', note='gt', generated_note='g')]
        mock_evaluation_output = MagicMock(test_results=[])
        mock_evaluate.return_value = mock_evaluation_output

        # Act & Assert
        with self.assertRaises(ValueError):
            run_evaluation(notes)

    @patch('evaluation.evaluate')
    def test_run_evaluation_missing_metrics(self, mock_evaluate):
        # Arrange
        notes = [ClinicalNote(transcript='t', note='gt', generated_note='g')]
        mock_test_result = MagicMock(metrics_data=None)
        mock_evaluation_output = MagicMock(test_results=[mock_test_result])
        mock_evaluate.return_value = mock_evaluation_output

        # Act
        results = run_evaluation(notes)

        # Assert
        self.assertEqual(len(results), 0)

if __name__ == '__main__':
    unittest.main()
