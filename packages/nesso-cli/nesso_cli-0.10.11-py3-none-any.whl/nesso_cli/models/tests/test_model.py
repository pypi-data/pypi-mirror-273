import copy
import shutil
from pathlib import Path

import nesso_cli.models.context as context
from conftest import TestData
from nesso_cli.models.common import yaml
from nesso_cli.models.config import config
from nesso_cli.models.main import app
from typer.testing import CliRunner

PROJECT_DIR = Path(__file__).parent.joinpath("dbt_projects", "postgres")
context.set("PROJECT_DIR", PROJECT_DIR)
TEST_DBT_TARGET = "dev"
TEST_MODEL_WITHOUT_TESTS = TestData.test_model_without_tests()

runner = CliRunner()


def test_model_bootstrap(MODEL, MODEL_PATH, MART):
    # Assumptions.
    assert not MODEL_PATH.exists()

    # Test.
    result = runner.invoke(app, ["model", "bootstrap", MODEL, "--subdir", MART])

    assert result.exit_code == 0
    assert MODEL_PATH.exists()

    # Cleaning up after the test
    MODEL_PATH.unlink()


def test_model_bootstrap_yaml(
    setup_model,
    postgres_connection,
    MODEL,
    TEST_SOURCE,
    TEST_TABLE_ACCOUNT_BASE_MODEL,
    MODEL_YAML_PATH,
):
    # Deletes the created `MODEL.yml` file through the pytest fixture `setup_model`.
    setup_model.unlink()

    # Assumption.
    assert not MODEL_YAML_PATH.exists()

    # Bootstrap YAML for the model.
    result = runner.invoke(
        app,
        [
            "model",
            "bootstrap-yaml",
            MODEL,
            "-t",
            "test_technical_owner@example.com",
            "-b",
            "test_bussiness_owner@example.com",
            "-e",
            TEST_DBT_TARGET,
        ],
    )

    # Checks whether the correct file structure has been created.
    assert result.exit_code == 0
    assert MODEL_YAML_PATH.exists()
    assert setup_model.exists()

    # Creating an independent copy of the object.
    expected_schema = copy.deepcopy(TEST_MODEL_WITHOUT_TESTS)

    # Applying changes to a copy of the object to reflect
    # the expected data changes after the test.
    expected_schema["models"][0]["meta"]["owners"][0][
        "email"
    ] = "test_technical_owner@example.com"
    expected_schema["models"][0]["meta"]["owners"][1][
        "email"
    ] = "test_bussiness_owner@example.com"

    with open(setup_model) as f:
        schema = yaml.load(f)

    assert schema == expected_schema

    # Check that comments are included in the schema file.
    with open(setup_model) as f:
        yaml_str = f.read()
    assert "# - unique" in yaml_str

    # Cleanup.
    postgres_connection.execute(f"DROP VIEW IF EXISTS {MODEL};")
    postgres_connection.execute(f"DROP VIEW IF EXISTS {TEST_TABLE_ACCOUNT_BASE_MODEL};")

    shutil.rmtree(
        PROJECT_DIR.joinpath("models", "sources", TEST_SOURCE),
        ignore_errors=True,
    )
    shutil.rmtree(
        PROJECT_DIR.joinpath("models", config.SILVER_SCHEMA),
        ignore_errors=True,
    )


def test_model_bootstrap_yaml_inherits_owners_metadata(
    setup_model,
    postgres_connection,
    MODEL,
    TEST_SOURCE,
    TEST_TABLE_ACCOUNT_BASE_MODEL,
    MODEL_YAML_PATH,
):
    # Deletes the created `MODEL.yml` file through the pytest fixture `setup_model`.
    setup_model.unlink()

    # Assumption.
    assert not MODEL_YAML_PATH.exists()

    # Bootstrap YAML for the model.
    result = runner.invoke(
        app,
        [
            "model",
            "bootstrap-yaml",
            MODEL,
            "-e",
            TEST_DBT_TARGET,
        ],
    )

    # Checks whether the correct file structure has been created.
    assert result.exit_code == 0
    assert MODEL_YAML_PATH.exists()
    assert setup_model.exists()

    with open(setup_model) as f:
        schema = yaml.load(f)

    assert schema == TEST_MODEL_WITHOUT_TESTS

    # Check that comments are included in the schema file.
    with open(setup_model) as f:
        yaml_str = f.read()
    assert "# - unique" in yaml_str

    # Cleanup.
    postgres_connection.execute(f"DROP VIEW IF EXISTS {MODEL};")
    postgres_connection.execute(f"DROP VIEW IF EXISTS {TEST_TABLE_ACCOUNT_BASE_MODEL};")

    shutil.rmtree(
        PROJECT_DIR.joinpath("models", "sources", TEST_SOURCE),
        ignore_errors=True,
    )
    shutil.rmtree(
        PROJECT_DIR.joinpath("models", config.SILVER_SCHEMA),
        ignore_errors=True,
    )
