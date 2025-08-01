import unittest
from unittest.mock import patch, MagicMock
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

from src.evaluation import run_evaluation
from src.schemas.models import ClinicalNote, EvaluationResult

class TestEvaluation(unittest.TestCase):

    @patch('openai.OpenAI')
    @patch('src.evaluation.evaluate')
    def test_run_evaluation_success(self, mock_evaluate, mock_openai):
        # Arrange
        notes = [
            ClinicalNote(
                transcript='transcript1',
                note='ground_truth1',
                generated_note='generated1'
            )
        ]

        # Create mock metrics with exact names that match what run_evaluation looks for
        mock_hallucination = MagicMock()
        mock_hallucination.name = "Hallucination"
        mock_hallucination.score = 0.1
        
        mock_recall = MagicMock()
        mock_recall.name = "Contextual Recall"
        mock_recall.score = 0.9
        
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
            mock_recall,
            mock_accuracy,
            mock_soap,
            mock_safety,
            mock_terminology
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

    @patch('openai.OpenAI')
    @patch('src.evaluation.evaluate')
    def test_run_evaluation_no_results(self, mock_evaluate, mock_openai):
        # Arrange
        notes = [ClinicalNote(transcript='t', note='gt', generated_note='g')]
        mock_evaluation_output = MagicMock(test_results=[])
        mock_evaluate.return_value = mock_evaluation_output

        # Act & Assert
        with self.assertRaises(ValueError):
            run_evaluation(notes)

    @patch('openai.OpenAI')
    @patch('src.evaluation.evaluate')
    def test_run_evaluation_missing_metrics(self, mock_evaluate, mock_openai):
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
