import unittest
from unittest.mock import patch
import os

from src.core.config import Settings


class TestConfig(unittest.TestCase):

    @patch.dict(
        os.environ,
        {
            "OPENAI_API_KEY": "test_openai_key",
            "CONFIDENT_API_KEY": "test_confident_key",
        },
    )
    def test_settings_load_from_env(self):
        # Arrange
        settings = Settings()

        # Assert
        self.assertEqual(settings.OPENAI_API_KEY, "test_openai_key")
        self.assertEqual(settings.CONFIDENT_API_KEY, "test_confident_key")


if __name__ == "__main__":
    unittest.main()
