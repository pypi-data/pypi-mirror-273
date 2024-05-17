from ruamel.yaml import YAML

from nesso_cli.models import context

yaml = YAML()


class NessoConfig:
    def __getattr__(self, key):
        return self.get(key)

    def __setattr__(self, key, value):
        self.set(key, value)

    @staticmethod
    def get(key: str):
        path = context.get("PROJECT_DIR") / ".nesso/config.yml"
        if not path.exists():
            if key in globals():
                # Return the default value, specified below in this file.
                return globals()[key]
            raise ValueError(f"Config file '{path}' does not exist.")
        with open(path) as f:
            config = yaml.load(f)
            return config.get(key)

    @staticmethod
    def set(key: str, value: str) -> None:
        path = context.get("PROJECT_DIR") / ".nesso/config.yml"
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path) as f:
            config = yaml.load(f)
            config[key] = value
        with open(path, "w") as f:
            yaml.dump(config, f)


PROJECT_NAME = "my_nesso_project"
DATABASE_TYPE = "trino"
BRONZE_SCHEMA = "staging"
SILVER_SCHEMA = "intermediate"
SILVER_SCHEMA_PREFIX = "int"
GOLD_LAYER_NAME = "marts"
DATA_ARCHITECTURE = "marts"
ENABLE_LUMA_INTEGRATION = True
MACROS_PATH = "dbt_packages/nesso_macros/macros"
DEFAULT_ENV = "dev"

config = NessoConfig()
