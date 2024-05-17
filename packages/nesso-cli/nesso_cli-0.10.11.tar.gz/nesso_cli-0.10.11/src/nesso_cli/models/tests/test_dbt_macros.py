import shutil
from pathlib import Path

import nesso_cli.models.context as context
from conftest import TestData
from nesso_cli.models.common import call_shell, yaml
from nesso_cli.models.config import config

PROJECT_DIR = Path(__file__).parent.joinpath("dbt_projects", "postgres")
context.set("PROJECT_DIR", PROJECT_DIR)
TEST_BASE_MODELS_DIR_PATH = (
    PROJECT_DIR / "models" / config.SILVER_SCHEMA / "macro_tests"
)


def test_generate_model_yaml_boilerplate(setup_test_source):
    yml_path = (
        TEST_BASE_MODELS_DIR_PATH
        / f"{config.SILVER_SCHEMA_PREFIX}_test_table_account.yml"
    )
    TEST_BASE_MODELS_DIR_PATH.mkdir(parents=True, exist_ok=True)
    args = {
        "model_name": "test_table_account",
        "technical_owner": "test_technical_owner_overwritten",
        "business_owner": "test_business_owner_overwritten",
        "domains": ["test_domain"],
        "source_systems": ["test_source_system"],
        "base_model_prefix": config.SILVER_SCHEMA_PREFIX,
        "snakecase_columns": True,
    }

    generate_model_yaml_cmd = (
        f"""dbt -q run-operation generate_model_yaml --args '{args}'"""
    )

    base_model_yaml_content = call_shell(
        generate_model_yaml_cmd,
        print_logs=False,
    )
    with open(yml_path, "w") as file:
        file.write(base_model_yaml_content)

    # Test.
    with open(yml_path) as f:
        schema = yaml.load(f)

    # Creating an independent copy of the object.
    expected_schema = TestData.test_base_model_without_tests()

    # Applying changes to a copy of the object to reflect
    # the expected data changes after the test.
    expected_schema["models"][0]["meta"]["owners"][0][
        "email"
    ] = "test_technical_owner_overwritten"
    expected_schema["models"][0]["meta"]["owners"][1][
        "email"
    ] = "test_business_owner_overwritten"

    assert schema == expected_schema

    # Cleanup.
    shutil.rmtree(
        PROJECT_DIR.joinpath("models", config.SILVER_SCHEMA),
        ignore_errors=True,
    )
