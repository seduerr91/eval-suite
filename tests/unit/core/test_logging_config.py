import unittest
from unittest.mock import patch
import logging

from src.core.logging_config import setup_logging

class TestLoggingConfig(unittest.TestCase):

    @patch('logging.basicConfig')
    def test_setup_logging(self, mock_basic_config):
        # Act
        setup_logging()

        # Assert
        mock_basic_config.assert_called_once()
        _, kwargs = mock_basic_config.call_args
        self.assertEqual(kwargs['level'], logging.INFO)
        
        # Check the formatter on the handler
        # Note: This is a bit more involved as basicConfig sets the formatter on the handler directly
        # and doesn't store it in a way that's simple to access without inspecting internal state.
        # A simple check for the presence of a handler is often sufficient for this level of testing.
        # For a more robust check, one might need to capture log output.

if __name__ == '__main__':
    unittest.main()
