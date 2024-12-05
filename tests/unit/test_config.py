import unittest
from sdk.config import Config
import yaml
import os

class TestConfig(unittest.TestCase):
    def setUp(self):
        """
        Set up a temporary config file for testing.F
        """
        self.config_data = {
            "api_key": "test_api_key",
            "base_url": "https://api.test.com",
            "timeout": 20
        }
        self.config_path = "tests/config_test/test_config.yaml"

        # Create a temporary YAML file with the test data
        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
        with open(self.config_path, "w") as file:
            yaml.dump(self.config_data, file)

    def test_config_loads_expects_correct_values(self):
        """
        Test if the Config class loads the correct values from the YAML file.
        """
        config = Config(config_path=self.config_path)
        self.assertEqual(config.api_key, "test_api_key")
        self.assertEqual(config.base_url, "https://api.test.com")
        self.assertEqual(config.timeout, 20)

    def test_config_loads_expects_default_base_url(self):
        """
        Test if the Config class uses default values when base_url is missing.
        """
        # Remove base_url from the config data
        del self.config_data["base_url"]

        # Update the config file
        with open(self.config_path, "w") as file:
            yaml.dump(self.config_data, file)

        config = Config(config_path=self.config_path)
        self.assertEqual(config.api_key, "test_api_key")
        self.assertEqual(config.base_url, "http://localhost:3000")
        self.assertEqual(config.timeout, 20)

    def test_missing_api_key_raises_value_error(self):
        """
        Test if a missing API key raises a ValueError.
        """
        # Remove the api_key from the config data
        del self.config_data["api_key"]

        # Update the config file
        with open(self.config_path, "w") as file:
            yaml.dump(self.config_data, file)

        with self.assertRaises(ValueError):
            Config(config_path=self.config_path)

    def test_missing_config_file_expects_file_not_found_error(self):
        """
        Test if a missing configuration file raises a FileNotFoundError.
        """
        with self.assertRaises(FileNotFoundError):
            Config(config_path="non_existent_config.yaml")

if __name__ == "__main__":
    unittest.main()
