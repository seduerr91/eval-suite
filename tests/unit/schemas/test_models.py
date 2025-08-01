import unittest
from pydantic import ValidationError

from src.schemas.models import ClinicalNote, EvaluationResult


class TestModels(unittest.TestCase):

    def test_clinical_note_creation(self):
        # Arrange
        data = {
            "transcript": "Patient interview transcript.",
            "note": "Clinician SOAP note.",
            "generated_note": "AI-generated SOAP note.",
        }

        # Act
        note = ClinicalNote(**data)

        # Assert
        self.assertEqual(note.transcript, data["transcript"])
        self.assertEqual(note.ground_truth_note, data["note"])
        self.assertEqual(note.generated_note, data["generated_note"])

    def test_clinical_note_missing_fields(self):
        # Arrange
        data = {"transcript": "Only transcript is provided."}

        # Act & Assert
        with self.assertRaises(ValidationError):
            ClinicalNote(**data)

    def test_evaluation_result_creation(self):
        # Arrange
        note_data = {
            "transcript": "Patient interview transcript.",
            "note": "Clinician SOAP note.",
            "generated_note": "AI-generated SOAP note.",
        }
        clinical_note = ClinicalNote(**note_data)
        result_data = {
            "note": clinical_note,
            "hallucination_score": 0.1,
            "missing_info_score": 0.9,
            "clinical_accuracy_score": 0.8,
            "soap_structure_score": 1.0,
            "clinical_safety_score": 0.7,
            "medical_terminology_score": 0.85,
            "overall_score": 0.89,
        }

        # Act
        result = EvaluationResult(**result_data)

        # Assert
        self.assertEqual(result.note, clinical_note)
        self.assertEqual(result.overall_score, 0.89)

    def test_evaluation_result_invalid_type(self):
        # Arrange
        note_data = {
            "transcript": "Patient interview transcript.",
            "note": "Clinician SOAP note.",
            "generated_note": "AI-generated SOAP note.",
        }
        clinical_note = ClinicalNote(**note_data)
        result_data = {
            "note": clinical_note,
            "hallucination_score": "not-a-float",
            "missing_info_score": 0.9,
            "clinical_accuracy_score": 0.8,
            "soap_structure_score": 1.0,
            "clinical_safety_score": 0.7,
            "medical_terminology_score": 0.85,
            "overall_score": 0.89,
        }

        # Act & Assert
        with self.assertRaises(ValidationError):
            EvaluationResult(**result_data)


if __name__ == "__main__":
    unittest.main()
