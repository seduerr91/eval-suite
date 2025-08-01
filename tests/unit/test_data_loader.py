import unittest
from unittest.mock import patch, MagicMock
import pandas as pd

from src.data_loader import generate_note, load_data
from src.schemas.models import ClinicalNote

class TestDataLoader(unittest.TestCase):

    @patch('src.data_loader.client.chat.completions.create')
    def test_generate_note_success(self, mock_create):
        # Arrange
        mock_response = MagicMock()
        mock_response.choices[0].message.content = 'Generated SOAP note.'
        mock_create.return_value = mock_response
        transcript = 'Patient complains of a headache.'

        # Act
        result = generate_note(transcript)

        # Assert
        self.assertEqual(result, 'Generated SOAP note.')
        mock_create.assert_called_once()

    @patch('data_loader.client.chat.completions.create')
    def test_generate_note_api_error(self, mock_create):
        # Arrange
        mock_create.side_effect = Exception('API Error')
        transcript = 'Patient complains of a headache.'

        # Act
        result = generate_note(transcript)

        # Assert
        self.assertEqual(result, '')

    @patch('data_loader.pd.read_json')
    @patch('data_loader.generate_note')
    @patch('os.path.exists')
    def test_load_data_success(self, mock_exists, mock_generate_note, mock_read_json):
        # Arrange
        mock_exists.return_value = True
        mock_data = {'patient_convo': ['Test transcript'], 'soap_notes': ['Test SOAP note']}
        mock_df = pd.DataFrame(mock_data)
        mock_read_json.return_value = mock_df
        mock_generate_note.return_value = 'Generated note.'

        # Act
        result = load_data()

        # Assert
        self.assertEqual(len(result), 1)
        self.assertIsInstance(result[0], ClinicalNote)
        self.assertEqual(result[0].transcript, 'Test transcript')
        self.assertEqual(result[0].note, 'Test SOAP note')
        self.assertEqual(result[0].generated_note, 'Generated note.')

    @patch('data_loader.pd.read_json')
    @patch('data_loader.generate_note')
    @patch('os.path.exists')
    def test_load_data_limit(self, mock_exists, mock_generate_note, mock_read_json):
        # Arrange
        mock_exists.return_value = True
        mock_data = {'patient_convo': ['t1', 't2', 't3'], 'soap_notes': ['s1', 's2', 's3']}
        mock_df = pd.DataFrame(mock_data)
        mock_read_json.return_value = mock_df
        mock_generate_note.return_value = 'Generated note.'

        # Act
        result = load_data(limit=2)

        # Assert
        self.assertEqual(len(result), 2)

    @patch('os.path.exists')
    def test_load_data_file_not_found(self, mock_exists):
        # Arrange
        mock_exists.return_value = False

        # Act
        result = load_data()

        # Assert
        self.assertEqual(result, [])

if __name__ == '__main__':
    unittest.main()
