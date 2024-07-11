from pathlib import Path
from pydantic import BaseModel
from strictyaml import YAML, load

# Project Directories
#PACKAGE_ROOT = Path(mro.__file__).resolve().parent
PACKAGE_ROOT = Path(__file__).resolve().parent.parent
print(PACKAGE_ROOT)
#ROOT = PACKAGE_ROOT.parent
CONFIG_FILE_PATH = PACKAGE_ROOT / "conf/config.yml"
DATASET_DIR = PACKAGE_ROOT / "data"
SQL_DIR = PACKAGE_ROOT / "sql"
TRAINED_MODEL_DIR = PACKAGE_ROOT / "src/models"


class ModelConfig(BaseModel):
    """
    All configuration relevant to feature engineering and monthly predictions.
    """

    bu_key: int
    bu_code: str
    model_label: str
    model_month_label : str
    current_month_model_flag : int
    run_type: str
    current_month_flag: int
    specified_month_idnt: int
    specified_month_name: str
    period_length: int


def find_config_file() -> Path:

    """Locate the configuration file."""

    if CONFIG_FILE_PATH.is_file():
        return CONFIG_FILE_PATH
    raise Exception(f"Config not found at {CONFIG_FILE_PATH!r}")


def fetch_config_from_yaml(cfg_path: Path = None) -> YAML:

    """Parse YAML containing the package configuration."""

    if not cfg_path:
        cfg_path = find_config_file()

    if cfg_path:
        with open(cfg_path, "r") as conf_file:
            parsed_config = load(conf_file.read())
            return parsed_config
    raise OSError(f"Did not find config file at path: {cfg_path}")


def create_and_validate_config(parsed_config: YAML = None) -> ModelConfig:
    """Run validation on config values."""

    if parsed_config is None:
        parsed_config = fetch_config_from_yaml()

    model_config_instance = ModelConfig(**parsed_config.data)

     # specify the data attribute from the strictyaml YAML type.
    # _config = Config(
    #      model_config=ModelConfig(**parsed_config.data),
    # )

    return model_config_instance


config = create_and_validate_config()