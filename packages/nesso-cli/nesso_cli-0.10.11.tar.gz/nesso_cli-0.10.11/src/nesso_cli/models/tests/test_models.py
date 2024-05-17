import copy

import pytest
from conftest import TestData
from nesso_cli.models.common import yaml
from nesso_cli.models.models import DBTModel, DBTProperties, ModelProperties
from test_update import (
    COLUMNS_AFTER_DELETE,
    COLUMNS_AFTER_INSERT,
    YAML_SOURCE_COLUMNS,
    YAML_SOURCE_COLUMNS_METADATA,
)

BASE_MODEL_DEPENDENCY = "model.postgres.int_test_table_account"
BASE_MODEL_TEST_DATA_WITHOUT_TESTS = TestData.test_base_model_without_tests()

FIELD_NAME = "test_list"
UPSTREAM_VALUE = ["element4"]
META_FIELDS = {"test_list": ["element1", "element2", "element3"]}
META_FIELDS_OVERWRITE = {"test_list": ["element4"]}
META_FIELDS_APPEND = {"test_list": ["element1", "element2", "element3", "element4"]}


@pytest.fixture()
def dbt_properties(setup_test_source):
    dp = DBTProperties(file_path=setup_test_source)
    yield dp


@pytest.fixture()
def dbt_model(setup_model, MODEL):
    dm = DBTModel(
        model_name=MODEL,
        domains=["test_domain_2", "test_domain"],
        SLA="12 hours",
    )
    yield dm


@pytest.fixture()
def dbt_model_without_meta(setup_model, MODEL):
    dm = DBTModel(model_name=MODEL)
    yield dm


#####################
### DBTProperties ### # noqa
#####################


def test_set_yaml_content(dbt_properties):
    dbt_properties[dbt_properties.resource_type] = "test"
    dbt_properties.set_yaml_content()

    with open(dbt_properties.file_path, "r") as file:
        yaml_dict = yaml.load(file)

    assert yaml_dict == {"version": 2, dbt_properties.resource_type: "test"}


def test_set_columns_order(TEST_TABLE_ACCOUNT, dbt_properties):
    def _get_columns_order(path):
        with open(path, "r") as file:
            yaml_dict = yaml.load(file)

        columns = yaml_dict[dbt_properties.resource_type][0]["tables"][0]["columns"]
        columns_order = [col["name"] for col in columns]

        return columns_order

    initial_columns_order = [
        "id",
        "name",
        "email",
        "mobile",
        "country",
        "_viadot_downloaded_at_utc",
    ]

    columns_order = _get_columns_order(dbt_properties.file_path)

    assert columns_order == initial_columns_order

    desired_columns_order = [
        "id",
        "mobile",
        "country",
        "name",
        "_viadot_downloaded_at_utc",
        "email",
    ]
    dbt_properties.set_columns_order(
        desired_order=desired_columns_order, table_name=TEST_TABLE_ACCOUNT
    )

    columns_order = _get_columns_order(dbt_properties.file_path)

    assert columns_order == desired_columns_order


def test_get_yaml_table_columns(TEST_TABLE_ACCOUNT, dbt_properties):
    columns_metadata = dbt_properties.get_yaml_table_columns(
        table_name=TEST_TABLE_ACCOUNT,
    )
    assert columns_metadata == YAML_SOURCE_COLUMNS_METADATA


def test_dict_diff():
    # Test equal dictionaries
    dict1_equal = {"a": 1, "b": 2, "c": 3}
    dict2_equal = {"a": 1, "b": 2, "c": 3}
    result_equal = DBTProperties.dict_diff(dict1_equal, dict2_equal)
    assert result_equal == {}

    # Test differing dictionaries
    dict1_differ = {"a": 1, "b": 2, "c": 3}
    dict2_differ = {"a": 1, "b": 2, "c": 4}
    result_differ = DBTProperties.dict_diff(dict1_differ, dict2_differ)
    assert result_differ == {"c": 4}


def test_coherence_scan(TEST_SOURCE, TEST_TABLE_ACCOUNT, dbt_properties):
    diff, yaml_columns, db_columns = dbt_properties.coherence_scan(
        schema_name=TEST_SOURCE,
        table_name=TEST_TABLE_ACCOUNT,
    )
    assert not diff
    assert yaml_columns == YAML_SOURCE_COLUMNS_METADATA
    assert db_columns == YAML_SOURCE_COLUMNS


def test_add_column(TEST_TABLE_ACCOUNT, dbt_properties):
    dbt_properties.add_column(
        table_name=TEST_TABLE_ACCOUNT,
        column_name="new_column_name",
        index=6,
        data_type="CHARACTER VARYING(255)",
    )

    yaml_columns_metadata = dbt_properties.get_yaml_table_columns(
        table_name=TEST_TABLE_ACCOUNT
    )

    assert yaml_columns_metadata == COLUMNS_AFTER_INSERT


def test_delete_column(TEST_TABLE_ACCOUNT, dbt_properties):
    dbt_properties.delete_column(
        table_name=TEST_TABLE_ACCOUNT, column_name="_viadot_downloaded_at_utc"
    )
    yaml_columns_metadata = dbt_properties.get_yaml_table_columns(
        table_name=TEST_TABLE_ACCOUNT
    )

    assert yaml_columns_metadata == COLUMNS_AFTER_DELETE


##################
#### DBTModel #### noqa
##################


def test_dbt_model_get_model_upstream_dependencies(dbt_model):
    model_nodes = dbt_model.get_model_upstream_dependencies()
    assert model_nodes == [BASE_MODEL_DEPENDENCY]


def test_dbt_model_get_node_metadata(dbt_model):
    node_metadata = dbt_model.get_node_metadata(node_name=BASE_MODEL_DEPENDENCY)
    node_metadata_properties = ModelProperties(models=[node_metadata]).dict(
        exclude_none=True, by_alias=True
    )
    assert node_metadata_properties == BASE_MODEL_TEST_DATA_WITHOUT_TESTS


def test_dbt_model_get_upstream_metadata(dbt_model):
    base_model_metadata = dbt_model.get_upstream_metadata()
    base_model_properties = ModelProperties(models=base_model_metadata).dict(
        exclude_none=True, by_alias=True
    )
    assert base_model_properties == BASE_MODEL_TEST_DATA_WITHOUT_TESTS


def test_dbt_model_get_columns(dbt_model):
    columns = dbt_model.get_columns()
    assert columns == TestData.DEFAULT_COLUMNS


def test_dbt_model_resolve_columns_metadata(dbt_model):
    model_columns = dbt_model.resolve_columns_metadata()
    assert model_columns == TestData.TEST_COLUMNS_WITHOUT_TESTS


def test_dbt_model__resolve_column_values(dbt_model):
    model_column = copy.deepcopy(TestData.DEFAULT_COLUMNS)[0]
    upstream_column = copy.deepcopy(TestData.TEST_COLUMNS_WITHOUT_TESTS)[0]
    dbt_model._resolve_column_values(
        model_column=model_column,
        upstream_column=upstream_column,
    )
    assert model_column.dict() == upstream_column.dict()


@pytest.mark.parametrize(
    "inheritance_strategy, expected",
    [
        ("append", META_FIELDS_APPEND),
        ("skip", META_FIELDS),
        ("overwrite", META_FIELDS_OVERWRITE),
    ],
)
def test__set_meta_value(dbt_model, inheritance_strategy, expected):
    meta = dbt_model._set_meta_value(
        meta=META_FIELDS,
        field_name=FIELD_NAME,
        upstream_value=UPSTREAM_VALUE,
        inheritance_strategy=inheritance_strategy,
        default_value=META_FIELDS[FIELD_NAME],
    )
    assert meta == expected


def test_dbt_model_resolve_model_metadata(dbt_model):
    test_model_without_tests = TestData.test_model_without_tests()
    test_model_without_tests["models"][0]["meta"]["domains"] = [
        "test_domain_2",
        "test_domain",
    ]
    test_model_without_tests["models"][0]["meta"]["SLA"] = "12 hours"
    test_model_without_tests["models"][0]["meta"]["owners"][0]["email"] = ""
    test_model_without_tests["models"][0]["meta"]["owners"][1]["email"] = ""

    # Test.
    model_metadata = dbt_model.resolve_model_metadata()
    model_metadata_properties = ModelProperties(models=[model_metadata]).dict(
        exclude_none=True, by_alias=True
    )

    assert model_metadata_properties == test_model_without_tests


def test_dbt_model_resolve_model_metadata_without_meta_fields(dbt_model_without_meta):
    test_model_without_tests = TestData.test_model_without_tests()
    test_model_without_tests["models"][0]["meta"]["domains"] = [
        "test_domain",
    ]
    test_model_without_tests["models"][0]["meta"]["owners"][0]["email"] = ""
    test_model_without_tests["models"][0]["meta"]["owners"][1]["email"] = ""

    # Test.
    model_metadata = dbt_model_without_meta.resolve_model_metadata()
    model_metadata_properties = ModelProperties(models=[model_metadata]).dict(
        exclude_none=True, by_alias=True
    )

    assert model_metadata_properties == test_model_without_tests
