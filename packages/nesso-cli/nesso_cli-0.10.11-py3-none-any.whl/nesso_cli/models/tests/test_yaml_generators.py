from conftest import TestData
from nesso_cli.models.yaml_generators import generate_model_yaml

test_model_without_tests = TestData.test_model_without_tests()
test_base_model_without_tests = TestData.test_base_model_without_tests()


def test_generate_model_yaml_silver_schema_model(setup_base_model, TEST_TABLE_ACCOUNT):
    test_base_model_without_tests["models"][0]["meta"]["owners"][0]["email"] = ""
    test_base_model_without_tests["models"][0]["meta"]["owners"][1]["email"] = ""
    test_base_model_without_tests["models"][0]["description"] = ""

    # Test.
    result = generate_model_yaml(TEST_TABLE_ACCOUNT, domains=["test_domain"])
    assert result == test_base_model_without_tests


def test_generate_model_yaml_gold_schema_model(setup_model, MODEL):
    test_model_without_tests["models"][0]["meta"]["owners"][0]["email"] = ""
    test_model_without_tests["models"][0]["meta"]["owners"][1]["email"] = ""

    # Test.
    result = generate_model_yaml(MODEL, base_model_prefix=None)
    assert result == test_model_without_tests
