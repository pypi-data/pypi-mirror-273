from nesso_cli.models.config import config
from nesso_cli.models.models import DBTModel, ModelProperties


def generate_model_yaml(
    model_name: str,
    target: str = config.DEFAULT_ENV,
    snakecase_columns: bool = True,
    base_model_prefix: str | None = config.SILVER_SCHEMA_PREFIX,
    **meta,
) -> dict[str, ModelProperties]:
    """
    Generate model YAML template.

    Args:
        model_name (str): The name of the model for which to generate the template.
        target (str): The name of the dbt target to use.
            Defaults to`config.DEFAULT_ENV`.
        snakecase_columns (bool, optional): Whether to standardize upstream column names
            to snakecase in the model. Defaults to True.
        base_model_prefix (str, optional): Prefix to apply to the name of
            the base model. Defaults to `config.SILVER_SCHEMA_PREFIX`.
        meta (dict[str, Any], optional): Keyword arguments specifying metadata
            fields.

    Returns:
        dict[str, ModelProperties]: Pydantic model dictionary `ModelProperties`.
    """

    if base_model_prefix is None:
        base_model_prefix = ""
    else:
        if base_model_prefix and not base_model_prefix.endswith("_"):
            base_model_prefix = f"{base_model_prefix}_"

        model_name = f"{base_model_prefix}{model_name}"

    dbt_model = DBTModel(model_name=model_name, env=target, **meta)
    model_metadata = dbt_model.resolve_model_metadata(
        snakecase_columns=snakecase_columns
    )
    models_list = [model_metadata]
    model_properties = ModelProperties(models=models_list)

    return model_properties.dict(exclude_none=True, by_alias=True)
