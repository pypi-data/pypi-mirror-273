import copy
import shutil
from pathlib import Path

import nesso_cli.models.context as context
import pytest
from conftest import TestData
from nesso_cli.models.base_model import check_if_base_model_exists
from nesso_cli.models.common import check_if_relation_exists, yaml
from nesso_cli.models.config import config
from nesso_cli.models.main import app
from nesso_cli.models.models import Model, ModelProperties
from typer.testing import CliRunner

PROJECT_DIR = Path(__file__).parent.joinpath("dbt_projects", "postgres")
context.set("PROJECT_DIR", PROJECT_DIR)
BASE_MODELS_DIR_PATH = PROJECT_DIR / "models" / config.SILVER_SCHEMA


runner = CliRunner()


# Base model
int_test_table_account_without_metadata = [
    Model(
        name="int_test_table_account",
        meta=TestData.DEFAULT_RESOURCE_METADATA,
        description="Base model of the `test_table_account` table.",
        columns=TestData.DEFAULT_COLUMNS,
    )
]
test_base_model_without_metadata = ModelProperties(
    models=int_test_table_account_without_metadata
)
# Convert to dictionary, excluding fields with None values,
# as dbt > 1.5 doesn't accept None in the `tests` field.
BASE_MODEL_TEST_DATA_DEFAULT_METADATA = test_base_model_without_metadata.dict(
    exclude_none=True, by_alias=True
)

SOURCE_TEST_DATA_DEFAULT_METADATA = TestData.default_source()
BASE_MODEL_TEST_DATA_WITHOUT_TESTS = TestData.test_base_model_without_tests()


def test_check_if_base_model_exists(TEST_TABLE_CONTACT_BASE_MODEL):
    # Assumptions.
    assert not check_if_base_model_exists(TEST_TABLE_CONTACT_BASE_MODEL)

    # Create the base model.
    base_model_dir_path = BASE_MODELS_DIR_PATH / TEST_TABLE_CONTACT_BASE_MODEL
    base_model_dir_path.mkdir(parents=True, exist_ok=True)

    base_model_sql_path = base_model_dir_path / f"{TEST_TABLE_CONTACT_BASE_MODEL}.sql"
    base_model_sql_path.touch()

    base_model_yaml_path = base_model_dir_path / f"{TEST_TABLE_CONTACT_BASE_MODEL}.yml"
    base_model_yaml_path.touch()

    # Test.
    assert check_if_base_model_exists(TEST_TABLE_CONTACT_BASE_MODEL)

    # Cleanup.
    shutil.rmtree(base_model_dir_path, ignore_errors=True)


def test_base_model_create(
    setup_test_source,
    postgres_connection,
    TEST_SOURCE,
    TEST_TABLE_ACCOUNT,
    TEST_TABLE_ACCOUNT_BASE_MODEL,
):
    # Assumptions.
    assert not check_if_base_model_exists(TEST_TABLE_ACCOUNT_BASE_MODEL)

    result = runner.invoke(
        app,
        [
            "base_model",
            "create",
            TEST_TABLE_ACCOUNT,
            "-s",
            TEST_SOURCE,
            "-p",
            PROJECT_DIR.name,
        ],
    )
    assert result.exit_code == 0
    assert check_if_base_model_exists(TEST_TABLE_ACCOUNT_BASE_MODEL)

    base_model_dir_path = BASE_MODELS_DIR_PATH / TEST_TABLE_ACCOUNT_BASE_MODEL
    base_model_schema_path = (
        base_model_dir_path / f"{TEST_TABLE_ACCOUNT_BASE_MODEL}.yml"
    )
    with open(base_model_schema_path) as f:
        schema = yaml.load(f)

    assert schema == BASE_MODEL_TEST_DATA_WITHOUT_TESTS

    # Check that comments are included in the schema file.
    with open(base_model_schema_path) as f:
        yaml_str = f.read()
    assert "# - unique" in yaml_str

    # Cleanup.
    shutil.rmtree(
        PROJECT_DIR.joinpath("models", config.SILVER_SCHEMA),
        ignore_errors=True,
    )
    postgres_connection.execute(f"DROP VIEW IF EXISTS {TEST_TABLE_ACCOUNT_BASE_MODEL};")


def test_base_model_create_inherits_metadata(
    setup_test_source,
    postgres_connection,
    TEST_SOURCE,
    TEST_TABLE_ACCOUNT,
    TEST_TABLE_ACCOUNT_BASE_MODEL,
):
    """
    Test that the base model inherits table-level `meta` metadata
    from the source table.
    """
    # Assumptions.
    assert not check_if_base_model_exists(TEST_TABLE_ACCOUNT_BASE_MODEL)

    # Add some metadata to the test source table.
    source_schema_path = PROJECT_DIR.joinpath(
        "models", "sources", TEST_SOURCE, TEST_SOURCE + ".yml"
    )
    sources_schema = yaml.load(source_schema_path.read_text())
    source_table_schema = sources_schema["sources"][0]["tables"][0]
    source_table_meta = source_table_schema["meta"]

    # Set up test model-level metadata.
    source_table_meta["owners"] = [
        {"type": "Technical owner", "email": "technical_owner@example.com"},
        {"type": "Business owner", "email": "business_owner@example.com"},
    ]
    source_table_meta["domains"] = ["test_domain"]
    source_table_meta["SLA"] = "42 hours"

    with open(source_schema_path, "w") as f:
        yaml.dump(sources_schema, f)

    # Now create a base model.
    assert not check_if_base_model_exists(TEST_TABLE_ACCOUNT_BASE_MODEL)

    result = runner.invoke(
        app,
        [
            "base_model",
            "create",
            TEST_TABLE_ACCOUNT,
            "-s",
            TEST_SOURCE,
            "-p",
            PROJECT_DIR.name,
        ],
    )

    assert result.exit_code == 0
    assert check_if_base_model_exists(TEST_TABLE_ACCOUNT_BASE_MODEL)

    # Verify that it inherited the metadata.
    base_model_dir_path = BASE_MODELS_DIR_PATH / TEST_TABLE_ACCOUNT_BASE_MODEL
    base_model_schema_path = (
        base_model_dir_path / f"{TEST_TABLE_ACCOUNT_BASE_MODEL}.yml"
    )
    with open(base_model_schema_path) as f:
        base_model_schema = yaml.load(f)["models"][0]

    # Verify column-level metadata.
    base_model_meta = base_model_schema["meta"]
    assert base_model_meta["owners"] == source_table_meta["owners"]
    assert base_model_meta["domains"] == source_table_meta["domains"]
    assert base_model_meta["SLA"] == source_table_meta["SLA"]

    # Cleanup.
    shutil.rmtree(
        PROJECT_DIR.joinpath("models", config.SILVER_SCHEMA),
        ignore_errors=True,
    )
    postgres_connection.execute(f"DROP VIEW IF EXISTS {TEST_TABLE_ACCOUNT_BASE_MODEL};")


def test_base_model_rm(
    setup_test_source,
    postgres_connection,
    TEST_SOURCE,
    TEST_TABLE_ACCOUNT,
    TEST_TABLE_ACCOUNT_BASE_MODEL,
):
    # Assumptions.
    assert not check_if_base_model_exists(TEST_TABLE_ACCOUNT_BASE_MODEL)

    # Create a base model.
    result = runner.invoke(
        app,
        [
            "base_model",
            "create",
            TEST_TABLE_ACCOUNT,
            "-s",
            TEST_SOURCE,
            "-p",
            PROJECT_DIR.name,
        ],
    )
    assert result.exit_code == 0
    assert check_if_base_model_exists(TEST_TABLE_ACCOUNT_BASE_MODEL)

    # Remove it.
    runner.invoke(app, ["base_model", "rm", TEST_TABLE_ACCOUNT_BASE_MODEL])

    # Validate it worked.
    assert not check_if_base_model_exists(TEST_TABLE_ACCOUNT_BASE_MODEL)

    # Cleanup.
    postgres_connection.execute(f"DROP VIEW IF EXISTS {TEST_TABLE_ACCOUNT_BASE_MODEL};")


def test_base_model_rm_drop_relation(
    setup_test_source,
    postgres_connection,
    TEST_SOURCE,
    TEST_SCHEMA,
    TEST_TABLE_ACCOUNT,
    TEST_TABLE_ACCOUNT_BASE_MODEL,
):
    """Test removing a base model together with dropping its relation."""
    # Assumptions.
    assert not check_if_base_model_exists(TEST_TABLE_ACCOUNT_BASE_MODEL)

    # Create a base model.
    result1 = runner.invoke(
        app,
        [
            "base_model",
            "create",
            TEST_TABLE_ACCOUNT,
            "-s",
            TEST_SOURCE,
            "-p",
            PROJECT_DIR.name,
        ],
    )
    assert result1.exit_code == 0
    assert check_if_base_model_exists(TEST_TABLE_ACCOUNT_BASE_MODEL)
    assert check_if_relation_exists(
        schema=TEST_SCHEMA, name=TEST_TABLE_ACCOUNT_BASE_MODEL
    )

    # Remove the YAML & drop the relation.
    result2 = runner.invoke(
        app, ["base_model", "rm", TEST_TABLE_ACCOUNT_BASE_MODEL, "--relation"]
    )

    # Validate it worked.
    assert result2.exit_code == 0
    assert not check_if_base_model_exists(TEST_TABLE_ACCOUNT_BASE_MODEL)
    assert not check_if_relation_exists(
        schema=TEST_SCHEMA, name=TEST_TABLE_ACCOUNT_BASE_MODEL
    )

    # Cleanup.
    postgres_connection.execute(
        f"DROP VIEW IF EXISTS {TEST_SCHEMA}.{TEST_TABLE_ACCOUNT_BASE_MODEL};"
    )


def test_base_model_bootstrap(TEST_TABLE_ACCOUNT, TEST_TABLE_ACCOUNT_BASE_MODEL):
    """
    Note that we specify intermediate schema prefix in the test config. Due to
    this, even though we pass `TEST_TABLE_ACCOUNT` as the name of the model to
    `base_model bootstrap`, the directory and file name will be prefixed.
    """
    # Assumptions.
    assert not check_if_base_model_exists(TEST_TABLE_ACCOUNT_BASE_MODEL)

    base_model_dir_path = BASE_MODELS_DIR_PATH / TEST_TABLE_ACCOUNT_BASE_MODEL
    base_model_sql_path = base_model_dir_path / f"{TEST_TABLE_ACCOUNT_BASE_MODEL}.sql"

    result = runner.invoke(
        app,
        [
            "base_model",
            "bootstrap",
            TEST_TABLE_ACCOUNT,
        ],
    )

    assert result.exit_code == 0
    assert base_model_sql_path.exists()

    # Cleanup.
    shutil.rmtree(base_model_dir_path, ignore_errors=True)


def test_base_model_bootstrap_yaml(
    setup_test_source,
    postgres_connection,
    TEST_SCHEMA,
    TEST_SOURCE,
    TEST_TABLE_ACCOUNT,
    TEST_TABLE_ACCOUNT_BASE_MODEL,
):
    # Assumptions.
    assert not check_if_base_model_exists(TEST_TABLE_ACCOUNT_BASE_MODEL)

    base_model_dir_path = BASE_MODELS_DIR_PATH / TEST_TABLE_ACCOUNT_BASE_MODEL
    base_model_sql_path = base_model_dir_path / f"{TEST_TABLE_ACCOUNT_BASE_MODEL}.sql"
    base_model_sql_path.parent.mkdir(parents=True, exist_ok=True)
    base_model_sql_path.touch()

    table_fqn = f"{TEST_SOURCE}.{TEST_TABLE_ACCOUNT}"
    view_fqn = f"{TEST_SCHEMA}.{TEST_TABLE_ACCOUNT_BASE_MODEL}"
    postgres_connection.execute(f"CREATE SCHEMA IF NOT EXISTS {TEST_SCHEMA};")
    postgres_connection.execute(
        f"CREATE OR REPLACE VIEW {view_fqn} AS SELECT * FROM {table_fqn};"
    )

    base_model_yaml_path = base_model_dir_path / f"{TEST_TABLE_ACCOUNT_BASE_MODEL}.yml"

    result = runner.invoke(
        app,
        [
            "base_model",
            "bootstrap-yaml",
            TEST_TABLE_ACCOUNT,
        ],
    )

    with open(base_model_yaml_path) as f:
        schema = yaml.load(f)

    assert schema == BASE_MODEL_TEST_DATA_WITHOUT_TESTS
    assert result.exit_code == 0
    assert base_model_yaml_path.exists()
    assert check_if_base_model_exists(TEST_TABLE_ACCOUNT_BASE_MODEL)

    # Cleanup.
    postgres_connection.execute(f"DROP VIEW IF EXISTS {view_fqn};")
    shutil.rmtree(base_model_dir_path, ignore_errors=True)


def test_base_model_bootstrap_yaml_no_int_prefix(
    setup_test_source,
    postgres_connection,
    TEST_SCHEMA,
    TEST_SOURCE,
    TEST_TABLE_ACCOUNT,
):
    # Assumptions.
    assert not check_if_base_model_exists(TEST_TABLE_ACCOUNT)

    config.SILVER_SCHEMA_PREFIX = ""

    base_model_dir_path = BASE_MODELS_DIR_PATH / TEST_TABLE_ACCOUNT
    base_model_sql_path = base_model_dir_path / f"{TEST_TABLE_ACCOUNT}.sql"
    base_model_sql_path.parent.mkdir(parents=True, exist_ok=True)
    base_model_sql_path.touch()

    table_fqn = f"{TEST_SOURCE}.{TEST_TABLE_ACCOUNT}"
    view_fqn = f"{TEST_SCHEMA}.{TEST_TABLE_ACCOUNT}"
    postgres_connection.execute(f"CREATE SCHEMA IF NOT EXISTS {TEST_SCHEMA};")
    postgres_connection.execute(
        f"CREATE OR REPLACE VIEW {view_fqn} AS SELECT * FROM {table_fqn};"
    )

    base_model_yaml_path = base_model_dir_path / f"{TEST_TABLE_ACCOUNT}.yml"

    result = runner.invoke(
        app,
        [
            "base_model",
            "bootstrap-yaml",
            TEST_TABLE_ACCOUNT,
        ],
    )

    with open(base_model_yaml_path) as f:
        schema = yaml.load(f)

    # Creating an independent copy of the object
    expected_schema = copy.deepcopy(BASE_MODEL_TEST_DATA_WITHOUT_TESTS)

    # Applying changes to a copy of the object to reflect
    # the expected data changes after the test.
    expected_schema["models"][0]["name"] = "test_table_account"

    config.SILVER_SCHEMA_PREFIX = "int"

    assert schema == expected_schema
    assert result.exit_code == 0
    assert base_model_yaml_path.exists()
    assert check_if_base_model_exists(TEST_TABLE_ACCOUNT)

    # Cleanup.
    postgres_connection.execute(f"DROP VIEW IF EXISTS {view_fqn};")
    shutil.rmtree(base_model_dir_path, ignore_errors=True)


def test_base_model_bootstrap_yaml_selected_columns(
    setup_test_source,
    postgres_connection,
    TEST_SCHEMA,
    TEST_SOURCE,
    TEST_TABLE_ACCOUNT,
    TEST_TABLE_ACCOUNT_BASE_MODEL,
):
    # Assumptions.
    assert not check_if_base_model_exists(TEST_TABLE_ACCOUNT_BASE_MODEL)

    base_model_dir_path = BASE_MODELS_DIR_PATH / TEST_TABLE_ACCOUNT_BASE_MODEL
    base_model_sql_path = base_model_dir_path / f"{TEST_TABLE_ACCOUNT_BASE_MODEL}.sql"
    base_model_sql_path.parent.mkdir(parents=True, exist_ok=True)
    base_model_sql_path.touch()

    table_fqn = f"{TEST_SOURCE}.{TEST_TABLE_ACCOUNT}"
    view_fqn = f"{TEST_SCHEMA}.{TEST_TABLE_ACCOUNT_BASE_MODEL}"
    postgres_connection.execute(f"CREATE SCHEMA IF NOT EXISTS {TEST_SCHEMA};")
    postgres_connection.execute(
        f"""CREATE OR REPLACE VIEW {view_fqn} AS
        SELECT id, name, 'test_value'::text AS test_column FROM {table_fqn};"""
    )

    base_model_yaml_path = base_model_dir_path / f"{TEST_TABLE_ACCOUNT_BASE_MODEL}.yml"

    result = runner.invoke(
        app,
        [
            "base_model",
            "bootstrap-yaml",
            TEST_TABLE_ACCOUNT,
        ],
    )

    with open(base_model_yaml_path) as f:
        schema = yaml.load(f)

    # Creating an independent copy of the object
    expected_schema = copy.deepcopy(BASE_MODEL_TEST_DATA_WITHOUT_TESTS)

    # Applying changes to a copy of the object to reflect
    # the expected data changes after the test.
    del expected_schema["models"][0]["columns"][2:]
    expected_schema["models"][0]["name"] = TEST_TABLE_ACCOUNT_BASE_MODEL
    expected_schema["models"][0]["columns"].append(
        {
            "name": "test_column",
            "data_type": "TEXT",
            "description": "",
            "quote": True,
            "tags": [],
        }
    )

    assert schema == expected_schema
    assert result.exit_code == 0
    assert base_model_yaml_path.exists()
    assert check_if_base_model_exists(TEST_TABLE_ACCOUNT_BASE_MODEL)

    # Cleanup.
    postgres_connection.execute(f"DROP VIEW IF EXISTS {view_fqn};")
    shutil.rmtree(base_model_dir_path, ignore_errors=True)


@pytest.mark.parametrize(
    "setup_test_source", [SOURCE_TEST_DATA_DEFAULT_METADATA], indirect=True
)
def test_base_model_create_without_metadata(
    setup_test_source,
    postgres_connection,
    TEST_SOURCE,
    TEST_TABLE_ACCOUNT,
    TEST_TABLE_ACCOUNT_BASE_MODEL,
):
    # Assumptions.
    assert not check_if_base_model_exists(TEST_TABLE_ACCOUNT_BASE_MODEL)

    result = runner.invoke(
        app,
        [
            "base_model",
            "create",
            TEST_TABLE_ACCOUNT,
            "-s",
            TEST_SOURCE,
            "-p",
            PROJECT_DIR.name,
        ],
    )

    assert result.exit_code == 0
    assert check_if_base_model_exists(TEST_TABLE_ACCOUNT_BASE_MODEL)

    base_model_dir_path = BASE_MODELS_DIR_PATH / TEST_TABLE_ACCOUNT_BASE_MODEL
    base_model_schema_path = (
        base_model_dir_path / f"{TEST_TABLE_ACCOUNT_BASE_MODEL}.yml"
    )
    with open(base_model_schema_path) as f:
        schema = yaml.load(f)

    assert schema == BASE_MODEL_TEST_DATA_DEFAULT_METADATA

    # Check that comments are included in the schema file.
    with open(base_model_schema_path) as f:
        yaml_str = f.read()
    assert "# - unique" in yaml_str

    # Cleanup.
    shutil.rmtree(
        PROJECT_DIR.joinpath("models", config.SILVER_SCHEMA),
        ignore_errors=True,
    )
    postgres_connection.execute(f"DROP VIEW IF EXISTS {TEST_TABLE_ACCOUNT_BASE_MODEL};")
