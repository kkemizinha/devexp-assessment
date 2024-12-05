import yaml

class Config:
    def __init__(self, config_path="config.yaml"):
        """
        Reads the configuration file and loads settings.
        :param config_path: Path to the configuration file.
        """
        try:
            with open(config_path, "r") as file:
                config = yaml.safe_load(file)
        except FileNotFoundError:
            raise FileNotFoundError(f"Configuration file '{config_path}' not found.")

        self.api_key = config.get("api_key")
        self.base_url = config.get("base_url", "http://localhost:3000")
        self.timeout = config.get("timeout", 10)

        if not self.api_key:
            raise ValueError("API key is required in the configuration file.")
