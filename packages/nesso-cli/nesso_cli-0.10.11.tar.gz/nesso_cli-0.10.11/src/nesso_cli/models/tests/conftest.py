import os
import random
import shutil
from datetime import datetime
from enum import Enum
from pathlib import Path

import pandas as pd
import pytest
from dotenv import load_dotenv
from faker import Faker
from nesso_cli.models.common import yaml
from nesso_cli.models.config import config
from nesso_cli.models.models import (
    ColumnMeta,
    Model,
    ModelProperties,
    Owner,
    Source,
    SourceProperties,
    SourceTable,
)
from nesso_cli.models.tests.test_init import (
    TEST_EXAMPLE_PROFILES_PATH,
    TEST_PROJECT_FILE,
    TEST_PROJECT_PATH,
    TEST_TEMPLATE_FILE,
    TEST_TEMPLATE_FILE_TEMPLATED_FILENAME,
)
from nesso_cli.models.tests.test_seed import SEED_SCHEMA_PATH
from pydantic import BaseModel, Field
from sqlalchemy import create_engine

load_dotenv()

fake = Faker()

POSTGRES_HOST = os.environ.get("POSTGRES_HOST")
PROJECT_DIR = Path(__file__).parent.joinpath("dbt_projects", "postgres")

test_tables_nrows = 100

SAMPLE_TAG = ["uat"]


class Name(Enum):
    ID = "id"
    NAME = "name"
    EMAIL = "email"
    MOBILE = "mobile"
    COUNTRY = "country"
    DOWNLOADED_AT_UTC = "_viadot_downloaded_at_utc"


class DataType(Enum):
    BIGINT = "BIGINT"
    TIMESTAMP = "TIMESTAMP WITHOUT TIME ZONE"
    TEXT = "TEXT"


class Description(Enum):
    ID = "description_id"
    NAME = "description_name"
    EMAIL = "description_email"
    MOBILE = "description_mobile"
    COUNTRY = "description_country"
    DOWNLOADED_AT_UTC = "description_viadot_downloaded_at_utc"


class Test(Enum):
    NOT_NULL = ["not_null"]
    UNIQUE = ["unique"]
    UNIQUE_AND_NOT_NULL = ["unique", "not_null"]


class TestData:
    """
    Class containing attributes and methods for generating test data.
    """

    TEST_COLUMNS = [
        ColumnMeta(
            name=Name.ID.value,
            data_type=DataType.BIGINT.value,
            description=Description.ID.value,
            tests=Test.NOT_NULL.value,
            tags=SAMPLE_TAG,
        ),
        ColumnMeta(
            name=Name.NAME.value,
            data_type=DataType.TEXT.value,
            description=Description.NAME.value,
            tests=Test.NOT_NULL.value,
            tags=SAMPLE_TAG,
        ),
        ColumnMeta(
            name=Name.EMAIL.value,
            data_type=DataType.TEXT.value,
            description=Description.EMAIL.value,
            tests=Test.UNIQUE_AND_NOT_NULL.value,
            tags=SAMPLE_TAG,
        ),
        ColumnMeta(
            name=Name.MOBILE.value,
            data_type=DataType.TEXT.value,
            description=Description.MOBILE.value,
            tags=SAMPLE_TAG,
        ),
        ColumnMeta(
            name=Name.COUNTRY.value,
            data_type=DataType.TEXT.value,
            description=Description.COUNTRY.value,
            tags=SAMPLE_TAG,
        ),
        ColumnMeta(
            name=Name.DOWNLOADED_AT_UTC.value,
            data_type=DataType.TIMESTAMP.value,
            description=Description.DOWNLOADED_AT_UTC.value,
            tags=SAMPLE_TAG,
        ),
    ]

    DEFAULT_COLUMNS = [
        ColumnMeta(
            name=Name.ID.value,
            data_type=DataType.BIGINT.value,
        ),
        ColumnMeta(
            name=Name.NAME.value,
            data_type=DataType.TEXT.value,
        ),
        ColumnMeta(
            name=Name.EMAIL.value,
            data_type=DataType.TEXT.value,
        ),
        ColumnMeta(
            name=Name.MOBILE.value,
            data_type=DataType.TEXT.value,
        ),
        ColumnMeta(
            name=Name.COUNTRY.value,
            data_type=DataType.TEXT.value,
        ),
        ColumnMeta(
            name=Name.DOWNLOADED_AT_UTC.value,
            data_type=DataType.TIMESTAMP.value,
        ),
    ]

    TEST_COLUMNS_WITHOUT_TESTS = [
        ColumnMeta(
            name=Name.ID.value,
            data_type=DataType.BIGINT.value,
            description=Description.ID.value,
            tags=SAMPLE_TAG,
        ),
        ColumnMeta(
            name=Name.NAME.value,
            data_type=DataType.TEXT.value,
            description=Description.NAME.value,
            tags=SAMPLE_TAG,
        ),
        ColumnMeta(
            name=Name.EMAIL.value,
            data_type=DataType.TEXT.value,
            description=Description.EMAIL.value,
            tags=SAMPLE_TAG,
        ),
        ColumnMeta(
            name=Name.MOBILE.value,
            data_type=DataType.TEXT.value,
            description=Description.MOBILE.value,
            tags=SAMPLE_TAG,
        ),
        ColumnMeta(
            name=Name.COUNTRY.value,
            data_type=DataType.TEXT.value,
            description=Description.COUNTRY.value,
            tags=SAMPLE_TAG,
        ),
        ColumnMeta(
            name=Name.DOWNLOADED_AT_UTC.value,
            data_type=DataType.TIMESTAMP.value,
            description=Description.DOWNLOADED_AT_UTC.value,
            tags=SAMPLE_TAG,
        ),
    ]

    OWNERS_LIST_TEST_USERS = [
        Owner(type="Technical owner", email="test_technical_owner"),
        Owner(type="Business owner", email="test_business_owner"),
    ]

    OWNERS_LIST_WITHOUT_USERS = [
        Owner(type="Technical owner"),
        Owner(type="Business owner"),
    ]

    METADATA = dict(
        owners=OWNERS_LIST_TEST_USERS,
        domains=["test_domain"],
        true_source=[],
        SLA="24 hours"
    )
    DEFAULT_RESOURCE_METADATA = dict(
        owners=OWNERS_LIST_WITHOUT_USERS, domains=[], true_source=[], SLA="24 hours"
    )
    DEFAULT_SOURCE_METADATA = dict(
        owners=OWNERS_LIST_WITHOUT_USERS, SLA="24 hours"
    )

    @staticmethod
    def test_source():
        table = [
            SourceTable(
                name="test_table_account",
                description="test_description",
                columns=TestData.TEST_COLUMNS,
                meta=TestData.METADATA,
            )
        ]
        source = [Source(name="staging", schema="staging", tables=table)]
        source_props = SourceProperties(sources=source)
        return source_props.to_dict()

    @staticmethod
    def default_source():
        table = [
            SourceTable(
                name="test_table_account",
                meta=TestData.DEFAULT_SOURCE_METADATA,
                columns=TestData.DEFAULT_COLUMNS,
            )
        ]
        source = [
            Source(
                name="staging",
                schema="staging",
                tables=table,
            )
        ]
        source_props = SourceProperties(sources=source)
        return source_props.to_dict()

    @staticmethod
    def test_base_model():
        model = [
            Model(
                name="int_test_table_account",
                description="Base model of the `test_table_account` table.",
                meta=TestData.METADATA,
                columns=TestData.TEST_COLUMNS,
            )
        ]
        model_props = ModelProperties(models=model)
        return model_props.to_dict()

    @staticmethod
    def test_base_model_without_tests():
        model = [
            Model(
                name="int_test_table_account",
                description="Base model of the `test_table_account` table.",
                meta=TestData.METADATA,
                columns=TestData.TEST_COLUMNS_WITHOUT_TESTS,
            )
        ]
        model_props = ModelProperties(models=model)
        return model_props.to_dict()

    @staticmethod
    def test_model():
        model = [
            Model(
                name="test_model",
                meta=TestData.METADATA,
                columns=TestData.TEST_COLUMNS
            )
        ]
        model_props = ModelProperties(models=model)
        return model_props.to_dict()

    @staticmethod
    def test_model_without_tests():
        model = [
            Model(
                name="test_model",
                meta=TestData.METADATA,
                columns=TestData.TEST_COLUMNS_WITHOUT_TESTS,
            )
        ]
        model_props = ModelProperties(models=model)
        return model_props.to_dict()


@pytest.fixture(params=[TestData.test_source()])
def setup_test_source(request, TEST_SOURCE):
    schema_file_name = TEST_SOURCE + ".yml"
    schema_path = PROJECT_DIR / "models" / "sources" / TEST_SOURCE / schema_file_name
    schema_path.parent.mkdir(parents=True, exist_ok=True)

    with open(schema_path, "w") as file:
        yaml.dump(request.param, file)

    yield schema_path

    shutil.rmtree(schema_path.parent, ignore_errors=True)


@pytest.fixture(params=[TestData.test_base_model()])
def setup_base_model(
    request,
    setup_test_source,
    postgres_connection,
    TEST_SOURCE,
    TEST_SCHEMA,
    TEST_TABLE_ACCOUNT,
    TEST_TABLE_ACCOUNT_BASE_MODEL,
):
    base_model_path = (
        PROJECT_DIR / "models" / config.SILVER_SCHEMA / TEST_TABLE_ACCOUNT_BASE_MODEL
    )
    base_model_file_yml = base_model_path / f"{TEST_TABLE_ACCOUNT_BASE_MODEL}.yml"
    base_model_file_sql = base_model_path / f"{TEST_TABLE_ACCOUNT_BASE_MODEL}.sql"
    base_model_path.mkdir(parents=True, exist_ok=True)

    with open(base_model_file_sql, "w") as f:
        f.write(
            f"select * from {{{{ source('{TEST_SOURCE}', '{TEST_TABLE_ACCOUNT}') }}}}"
        )
    table_fqn = f"{TEST_SOURCE}.{TEST_TABLE_ACCOUNT}"
    view_fqn = f"{TEST_SCHEMA}.{TEST_TABLE_ACCOUNT_BASE_MODEL}"
    postgres_connection.execute(f"CREATE SCHEMA IF NOT EXISTS {TEST_SCHEMA};")
    postgres_connection.execute(
        f"CREATE OR REPLACE VIEW {view_fqn} AS SELECT * FROM {table_fqn};"
    )

    with open(base_model_file_yml, "w") as file:
        yaml.dump(request.param, file)

    yield base_model_file_yml

    shutil.rmtree(base_model_path, ignore_errors=True)
    postgres_connection.execute(f"DROP SCHEMA IF EXISTS {TEST_SCHEMA} CASCADE;")


@pytest.fixture(params=[TestData.test_model()])
def setup_model(
    request,
    setup_base_model,
    postgres_connection,
    TEST_SCHEMA,
    TEST_TABLE_ACCOUNT_BASE_MODEL,
    MODEL,
    MODEL_BASE_DIR,
):
    model_file_yml = MODEL_BASE_DIR / f"{MODEL}.yml"
    model_file_sql = MODEL_BASE_DIR / f"{MODEL}.sql"
    MODEL_BASE_DIR.mkdir(parents=True, exist_ok=True)

    with open(model_file_sql, "w") as f:
        f.write(f"select * from {{{{ ref('{TEST_TABLE_ACCOUNT_BASE_MODEL}') }}}}")

    base_model_fqn = f"{TEST_SCHEMA}.{TEST_TABLE_ACCOUNT_BASE_MODEL}"
    model_fqn = f"{TEST_SCHEMA}.{MODEL}"
    postgres_connection.execute(f"CREATE SCHEMA IF NOT EXISTS {TEST_SCHEMA};")
    postgres_connection.execute(
        f"CREATE OR REPLACE VIEW {model_fqn} AS SELECT * FROM {base_model_fqn};"
    )
    with open(model_file_yml, "w") as file:
        yaml.dump(request.param, file)

    yield model_file_yml

    shutil.rmtree(MODEL_BASE_DIR, ignore_errors=True)
    postgres_connection.execute(f"DROP SCHEMA IF EXISTS {TEST_SCHEMA} CASCADE;")


@pytest.fixture(scope="session", autouse=True)
def setup_and_teardown(postgres_connection, TEST_SOURCE):
    # fix https://github.com/dbt-labs/dbt-utils/issues/627
    shutil.rmtree(
        PROJECT_DIR.joinpath(
            "dbt_packages",
            "dbt_utils",
            "tests",
        ),
        ignore_errors=True,
    )

    shutil.rmtree(PROJECT_DIR.joinpath("target"), ignore_errors=True)

    postgres_connection.execute(f"DROP SCHEMA IF EXISTS {TEST_SOURCE} CASCADE;")
    postgres_connection.execute("DROP SCHEMA IF EXISTS test_schema CASCADE;")

    postgres_connection.execute(f"CREATE SCHEMA {TEST_SOURCE};")

    working_dir = os.getcwd()

    os.chdir(PROJECT_DIR)

    shutil.rmtree(PROJECT_DIR.joinpath("models", "sources"), ignore_errors=True)
    shutil.rmtree(
        PROJECT_DIR.joinpath("models", config.SILVER_SCHEMA),
        ignore_errors=True,
    )
    shutil.rmtree(
        PROJECT_DIR.joinpath("models", config.GOLD_LAYER_NAME),
        ignore_errors=True,
    )

    yield

    shutil.rmtree(PROJECT_DIR.joinpath("models", "sources"), ignore_errors=True)
    shutil.rmtree(
        PROJECT_DIR.joinpath("models", config.SILVER_SCHEMA),
        ignore_errors=True,
    )
    shutil.rmtree(
        PROJECT_DIR.joinpath("models", config.GOLD_LAYER_NAME),
        ignore_errors=True,
    )
    SEED_SCHEMA_PATH.unlink(missing_ok=True)

    os.chdir(working_dir)

    postgres_connection.execute(f"DROP SCHEMA IF EXISTS {TEST_SOURCE} CASCADE;")
    postgres_connection.execute("DROP SCHEMA IF EXISTS test_schema CASCADE;")

    shutil.rmtree(PROJECT_DIR.joinpath("target"), ignore_errors=True)

    shutil.rmtree(
        PROJECT_DIR.joinpath(
            "dbt_packages",
            "dbt_utils",
            "tests",
        ),
        ignore_errors=True,
    )

    shutil.rmtree(
        TEST_PROJECT_PATH,
        ignore_errors=True,
    )

    TEST_EXAMPLE_PROFILES_PATH.unlink(missing_ok=True)
    TEST_PROJECT_FILE.unlink(missing_ok=True)
    TEST_TEMPLATE_FILE.unlink(missing_ok=True)
    TEST_TEMPLATE_FILE_TEMPLATED_FILENAME.unlink(missing_ok=True)


@pytest.fixture(scope="session")
def postgres_connection():
    connection = create_engine(
        f"postgresql://user:password@{POSTGRES_HOST}:5432/db",
        connect_args={"connect_timeout": 5},
    )
    yield connection
    connection.dispose()


@pytest.fixture(scope="session")
def MART():
    yield "test_mart"


@pytest.fixture(scope="session")
def MODEL():
    yield "test_model"


@pytest.fixture(scope="session")
def PROJECT():
    yield "test_project"


@pytest.fixture(scope="session")
def MODEL_BASE_DIR(MART, MODEL):
    yield PROJECT_DIR / "models" / config.GOLD_LAYER_NAME / MART / MODEL


@pytest.fixture(scope="session")
def MODEL_PATH(MODEL_BASE_DIR, MODEL):
    yield MODEL_BASE_DIR.joinpath(MODEL + ".sql")


@pytest.fixture(scope="session")
def MODEL_YAML_PATH(MODEL_BASE_DIR, MODEL):
    yield MODEL_BASE_DIR.joinpath(MODEL + ".yml")


@pytest.fixture(scope="session")
def TEST_SOURCE():
    yield config.BRONZE_SCHEMA


@pytest.fixture(scope="function")
def SOURCE_SCHEMA_PATH(TEST_SOURCE):
    schema_file_name = TEST_SOURCE + ".yml"
    schema_path = PROJECT_DIR / "models" / "sources" / TEST_SOURCE / schema_file_name
    schema_path.parent.mkdir(parents=True, exist_ok=True)

    yield schema_path

    shutil.rmtree(schema_path.parent, ignore_errors=True)


@pytest.fixture(scope="session")
def TEST_TABLE_CONTACT():
    yield "test_table_contact"


@pytest.fixture(scope="session")
def TEST_TABLE_ACCOUNT():
    yield "test_table_account"


@pytest.fixture(scope="session")
def TEST_TABLE_CONTACT_BASE_MODEL():
    prefix = config.SILVER_SCHEMA_PREFIX
    table_name = "test_table_contact"
    yield f"{prefix}_{table_name}" if prefix else table_name


@pytest.fixture(scope="session")
def TEST_TABLE_ACCOUNT_BASE_MODEL():
    prefix = config.SILVER_SCHEMA_PREFIX
    table_name = "test_table_account"
    yield f"{prefix}_{table_name}" if prefix else table_name


@pytest.fixture(scope="session")
def TEST_SCHEMA():
    yield "test_schema"


@pytest.fixture(autouse=True)
def create_contacts_table(
    postgres_connection, setup_and_teardown, TEST_SOURCE, TEST_TABLE_CONTACT
):
    fqn = f"{TEST_SOURCE}.{TEST_TABLE_CONTACT}"
    postgres_connection.execute(f"DROP TABLE IF EXISTS {fqn} CASCADE;")

    class Contact(BaseModel):
        Id: int = Field(default_factory=lambda: i)
        AccountId: str = Field(
            default_factory=lambda: random.randint(1, test_tables_nrows)
        )
        FirstName: str = Field(default_factory=fake.first_name)
        LastName: str = Field(default_factory=fake.last_name)
        ContactEMail: str = Field(default_factory=fake.email)
        MailingCity: str = Field(default_factory=fake.city)
        Country: str = Field(default_factory=fake.country)
        # Pydantic doesn't support fields starting with an underscore so we use aliases
        viadot_downloaded_at_utc: datetime = Field(
            default_factory=datetime.utcnow, alias="_viadot_downloaded_at_utc"
        )

    contacts = []

    for i in range(1, test_tables_nrows + 1):
        contacts.append(Contact(Id=i).dict(by_alias=True))
    contacts_df_pandas = pd.DataFrame(contacts)

    contacts_df_pandas.to_sql(
        TEST_TABLE_CONTACT,
        postgres_connection,
        schema=TEST_SOURCE,
        if_exists="replace",
        index=False,
    )

    yield

    postgres_connection.execute(f"DROP TABLE IF EXISTS {fqn} CASCADE;")


@pytest.fixture(autouse=True)
def create_accounts_table(
    postgres_connection, setup_and_teardown, TEST_SOURCE, TEST_TABLE_ACCOUNT
):
    fqn = f"{TEST_SOURCE}.{TEST_TABLE_ACCOUNT}"
    postgres_connection.execute(f"DROP TABLE IF EXISTS {fqn} CASCADE;")

    class Account(BaseModel):
        id: int = Field(default_factory=lambda: i)
        name: str = Field(default_factory=fake.company)
        email: str = Field(default_factory=fake.email)
        mobile: str = Field(default_factory=fake.phone_number)
        country: str = Field(default_factory=fake.country)
        # Pydantic doesn't support fields starting with an underscore so we use aliases
        viadot_downloaded_at_utc: datetime = Field(
            default_factory=datetime.utcnow, alias="_viadot_downloaded_at_utc"
        )

    accounts = []

    for i in range(1, test_tables_nrows + 1):
        accounts.append(Account(id=i).dict(by_alias=True))
    accounts_df_pandas = pd.DataFrame(accounts)

    accounts_df_pandas.to_sql(
        TEST_TABLE_ACCOUNT,
        postgres_connection,
        schema=TEST_SOURCE,
        if_exists="replace",
        index=False,
    )

    yield

    postgres_connection.execute(f"DROP TABLE IF EXISTS {fqn} CASCADE;")
