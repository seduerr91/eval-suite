import unittest
from unittest.mock import patch, mock_open
import pandas as pd

from src import dashboard


class TestApp(unittest.TestCase):

    @patch("src.dashboard.open", new_callable=mock_open)
    def test_load_results_file_not_found(self, mocked_file):
        # Arrange
        mocked_file.side_effect = FileNotFoundError

        # Act
        # We test the wrapped function to bypass the @st.cache_data decorator
        result = dashboard.load_results.__wrapped__()

        # Assert
        self.assertIsNone(result)

    @patch("src.dashboard.open")
    @patch("src.dashboard.json.load")
    def test_load_results_success(self, mock_json_load, mock_open):
        # Arrange
        mock_data = [
            {
                "overall_score": 0.8,
                "clinical_safety_score": 0.9,
                "soap_structure_score": 1,
                "clinical_accuracy_score": 0.85,
                "medical_terminology_score": 0.95,
                "hallucination_score": 0.1,
                "missing_info_score": 0.05,
                "note": {
                    "transcript": "a",
                    "ground_truth_note": "b",
                    "generated_note": "c",
                },
            }
        ]
        mock_json_load.return_value = mock_data

        # Act
        df = dashboard.load_results.__wrapped__()

        # Assert
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(len(df), 1)
        self.assertEqual(df.iloc[0]["overall_score"], 0.8)


if __name__ == "__main__":
    unittest.main()
