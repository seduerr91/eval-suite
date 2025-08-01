import unittest
from unittest.mock import patch, MagicMock
import sys
import os

from src.main import main

class TestMain(unittest.TestCase):

    @patch('main.setup_logging')
    @patch('main.load_data')
    @patch('main.run_evaluation')
    @patch('main.argparse.ArgumentParser')
    @patch('main.open', new_callable=unittest.mock.mock_open)
    @patch('main.json.dump')
    def test_main_full_run(self, mock_json_dump, mock_open, mock_arg_parser, mock_run_evaluation, mock_load_data, mock_setup_logging):
        # Arrange
        mock_args = MagicMock()
        mock_args.full = True
        mock_arg_parser.return_value.parse_args.return_value = mock_args

        mock_notes = [{'id': 1, 'text': 'Test note'}]
        mock_load_data.return_value = mock_notes

        mock_evaluation_results = [MagicMock()]
        mock_run_evaluation.return_value = mock_evaluation_results

        # Act
        main()

        # Assert
        mock_setup_logging.assert_called_once()
        mock_load_data.assert_called_once_with(limit=None)
        mock_run_evaluation.assert_called_once_with(mock_notes)
        mock_open.assert_called_once_with('data/evaluation_results.json', 'w')
        mock_json_dump.assert_called_once()

    @patch('main.setup_logging')
    @patch('main.load_data')
    @patch('main.run_evaluation')
    @patch('main.argparse.ArgumentParser')
    @patch('main.open', new_callable=unittest.mock.mock_open)
    @patch('main.json.dump')
    def test_main_limited_run(self, mock_json_dump, mock_open, mock_arg_parser, mock_run_evaluation, mock_load_data, mock_setup_logging):
        # Arrange
        mock_args = MagicMock()
        mock_args.full = False
        mock_arg_parser.return_value.parse_args.return_value = mock_args

        mock_notes = [{'id': 1, 'text': 'Test note'}]
        mock_load_data.return_value = mock_notes

        mock_evaluation_results = [MagicMock()]
        mock_run_evaluation.return_value = mock_evaluation_results

        # Act
        main()

        # Assert
        mock_setup_logging.assert_called_once()
        mock_load_data.assert_called_once_with(limit=2)
        mock_run_evaluation.assert_called_once_with(mock_notes)
        mock_open.assert_called_once_with('data/evaluation_results.json', 'w')
        mock_json_dump.assert_called_once()

    @patch('main.setup_logging')
    @patch('main.load_data')
    @patch('main.run_evaluation')
    def test_main_no_data(self, mock_run_evaluation, mock_load_data, mock_setup_logging):
        # Arrange
        mock_load_data.return_value = []

        # Act
        main()

        # Assert
        mock_setup_logging.assert_called_once()
        mock_load_data.assert_called_once()
        mock_run_evaluation.assert_not_called()

if __name__ == '__main__':
    unittest.main()
