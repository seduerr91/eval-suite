import unittest
import sys
import os
from unittest.mock import patch

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../src"))
)

from src.schemas.metrics import (
    SOAPStructureMetric,
    ClinicalSafetyMetric,
    MedicalTerminologyMetric,
)


class TestMetrics(unittest.TestCase):

    @patch("openai.OpenAI")
    def test_soap_structure_metric_init(self, mock_openai):
        # Act
        metric = SOAPStructureMetric()

        # Assert
        self.assertEqual(metric.name, "SOAP Structure Compliance [GEval]")
        self.assertIn(
            "Evaluate if the clinical note follows proper SOAP format", metric.criteria
        )
        self.assertEqual(metric.threshold, 0.8)

    @patch("openai.OpenAI")
    def test_clinical_safety_metric_init(self, mock_openai):
        # Act
        metric = ClinicalSafetyMetric()

        # Assert
        self.assertEqual(metric.name, "Clinical Safety Assessment [GEval]")
        self.assertIn("Evaluate potential patient safety risks", metric.criteria)
        self.assertEqual(metric.threshold, 0.7)

    @patch("openai.OpenAI")
    def test_medical_terminology_metric_init(self, mock_openai):
        # Act
        metric = MedicalTerminologyMetric()

        # Assert
        self.assertEqual(metric.name, "Medical Terminology Accuracy [GEval]")
        self.assertIn("Evaluate the use of medical terminology", metric.criteria)
        self.assertEqual(metric.threshold, 0.8)


if __name__ == "__main__":
    unittest.main()
