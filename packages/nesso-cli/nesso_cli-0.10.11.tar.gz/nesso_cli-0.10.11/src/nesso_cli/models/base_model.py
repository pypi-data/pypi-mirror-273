import shutil
from pathlib import Path
from typing import Optional, Union

import typer
from rich import print
from rich.panel import Panel
from typing_extensions import Annotated

import nesso_cli.models.context as context
from nesso_cli.models.common import call_shell, drop, get_local_schema, options
from nesso_cli.models.config import config

app = typer.Typer()


def _get_default_base_dir_path(base_model_name: str) -> Path:
    dbt_project_dir = Path(context.get("PROJECT_DIR"))
    return dbt_project_dir / "models" / config.SILVER_SCHEMA / base_model_name


def check_if_base_model_exists(
    base_model_name: str, base_model_dir: Optional[Union[str, Path]] = None
) -> bool:
    """
    Check whether a base model exists. This means that both the SQL and YAML files
    for the base model exist.

    Args:
        base_model_name (str): The name of the base model.
        base_model_dir (Optional[Union[str, Path]], optional): The path to the
            directory holding the base model. Defaults to None (default directory).

    Returns:
        bool: Whether the base model exists.
    """
    if base_model_dir is None:
        base_model_dir = _get_default_base_dir_path(base_model_name)

    # Enforce `pathlib.Path` type.
    base_model_dir = Path(base_model_dir)

    sql_path = base_model_dir / f"{base_model_name}.sql"
    yml_path = base_model_dir / f"{base_model_name}.yml"

    both_files_exist = sql_path.exists() and yml_path.exists()
    none_files_exist = not sql_path.exists() and not yml_path.exists()

    fqn = f"[blue]{config.SILVER_SCHEMA}.{base_model_name}[/blue]"
    msg = f"""SQL or YML file for the base model {fqn} is missing.
    Please remove the remaining file."""
    assert both_files_exist or none_files_exist, msg

    return sql_path.exists()


@app.command()
def create(
    source_table_name: Annotated[
        str,
        typer.Argument(
            help="The name of the source table for which to generate the base model.",
            show_default=False,
        ),
    ],
    source: Annotated[
        Optional[str],
        typer.Option(
            "--source",
            "-s",
            help="The name of the source schema.",
        ),
    ] = config.BRONZE_SCHEMA,
    technical_owner: options.technical_owner = None,
    business_owner: options.business_owner = None,
    snakecase_columns: Annotated[
        Optional[bool],
        typer.Option(
            "--snakecase-columns",
            "-sc",
            help="""Whether to standardize column names to snakecase.""",
            is_flag=True,
        ),
    ] = True,
    project: options.project = context.get("PROJECT_NAME"),
    env: options.environment = config.DEFAULT_ENV,
    force: options.force("Whether to overwrite an existing model.") = False,
):
    """Creates a base model for the specified source table."""

    if not source:
        source = config.BRONZE_SCHEMA

    if config.SILVER_SCHEMA_PREFIX:
        base_model_name = f"{config.SILVER_SCHEMA_PREFIX}_{source_table_name}"
    else:
        base_model_name = source_table_name

    dbt_project_dir = Path(context.get("PROJECT_DIR"))

    base_dir = dbt_project_dir / "models" / config.SILVER_SCHEMA / base_model_name
    yml_path = base_dir / f"{base_model_name}.yml"
    sql_path = base_dir / f"{base_model_name}.sql"

    if not project:
        project = dbt_project_dir.name

    if not base_dir.exists():
        base_dir.mkdir(parents=True, exist_ok=True)

    fqn = f"{config.SILVER_SCHEMA}.{base_model_name}"
    fqn_fmt = f"[white]{fqn}[/white]"
    source_fqn = f"{source}.{source_table_name}"
    source_fqn_fmt = f"[white]{source_fqn}[/white]"

    base_model_exists = check_if_base_model_exists(
        base_model_name, base_model_dir=base_dir
    )
    if base_model_exists:
        if force:
            operation = "overwriting"
        else:
            print(f"Base model {fqn_fmt} already exists. Skipping...")
            return
    else:
        operation = "creating"

    operation_past_tenses = {"overwriting": "overwritten", "creating": "created"}
    operation_past_tense = operation_past_tenses[operation]

    # Generate SQL
    print(f"{operation.title()} base model {fqn_fmt} from {source_fqn_fmt}...")
    args = {
        "source_name": source,
        "table_name": source_table_name,
        "dbt_project": project,
        "snakecase_columns": snakecase_columns,
    }
    base_model_content = call_shell(
        f"""dbt -q run-operation generate_base_model --args '{args}'""",
        print_logs=False,
    )
    with open(sql_path, "w") as file:
        file.write(base_model_content)
    print(f"Base model {fqn_fmt} has been {operation_past_tense} successfully.")

    # Generate YAML
    print(f"{operation.title()} YAML template for base model {fqn}...")
    args = {
        "model_name": source_table_name,
        "technical_owner": technical_owner,
        "business_owner": business_owner,
        "base_model_prefix": config.SILVER_SCHEMA_PREFIX,
        "snakecase_columns": snakecase_columns,
    }
    generate_model_yaml_cmd = (
        f"""dbt -q run-operation generate_model_yaml --args '{args}' --target {env}"""
    )

    base_model_yaml_content = call_shell(
        generate_model_yaml_cmd,
        print_logs=False,
    )
    with open(yml_path, "w") as file:
        file.write(base_model_yaml_content)

    # Materialize the model.
    call_shell(f"dbt run --select {base_model_name}", print_logs=False)

    print(
        f"YAML template for base model {fqn_fmt} has been {operation_past_tense} successfully."  # noqa
    )


@app.command()
def rm(
    name: Annotated[
        str,
        typer.Argument(
            help="The name of the base model to remove.", show_default=False
        ),
    ],
    relation: Annotated[
        Optional[bool],
        typer.Option(
            "--relation",
            "-r",
            help="Whether to remove the model's relation as well.",
            is_flag=True,
        ),
    ] = False,
    env: options.environment = config.DEFAULT_ENV,
):
    """Removes a base model (YAML and optionally the relation)."""

    dbt_project_dir = Path(context.get("PROJECT_DIR"))
    base_model_dir = dbt_project_dir / "models" / config.SILVER_SCHEMA / name

    shutil.rmtree(base_model_dir, ignore_errors=True)

    if relation:
        if env == "prod":
            schema = config.SILVER_SCHEMA
        else:
            schema = get_local_schema(target=env)
        drop(name=name, schema=schema)


@app.command()
def bootstrap(
    base_model_name: Annotated[
        str, typer.Argument(help="The name of the base model.", show_default=False)
    ],
):
    """Generate an empty [bright_black]{base_model_name}/{base_model_name}.sql[/] file
    in the silver schema.
    """

    prefix = config.SILVER_SCHEMA_PREFIX

    if prefix and base_model_name.startswith(prefix + "_"):
        base_model_name = base_model_name.replace(prefix + "_", "")

    if prefix:
        base_model_name_prefixed = f"{prefix}_{base_model_name}"
    else:
        base_model_name_prefixed = base_model_name

    dbt_project_dir = Path(context.get("PROJECT_DIR"))

    base_dir = (
        dbt_project_dir / "models" / config.SILVER_SCHEMA / base_model_name_prefixed
    )
    sql_path = base_dir / f"{base_model_name_prefixed}.sql"

    if not base_dir.exists():
        base_dir.mkdir(parents=True, exist_ok=True)

    fqn = f"{config.SILVER_SCHEMA}.{base_model_name_prefixed}"

    base_model_exists = check_if_base_model_exists(
        base_model_name_prefixed, base_model_dir=base_dir
    )
    if base_model_exists:
        print(f"Base model {fqn} already exists. Skipping...")
        return

    sql_path_short = Path(
        "models",
        config.SILVER_SCHEMA,
        base_model_name_prefixed,
        base_model_name_prefixed + ".sql",
    )

    sql_path.touch(exist_ok=True)

    print(
        f"File [bright_black]{sql_path_short}[/bright_black] has been created [green]successfully[/green]."  # noqa
    )

    print("Base model bootstrapping is [green]complete[/green].")

    sql_path_clickable = dbt_project_dir.name / sql_path_short
    print(
        Panel(
            f"""Once you populate the base model file ([link={sql_path}]{sql_path_clickable}[/link]),
you can materialize it with [bright_black]nesso models run -s {base_model_name_prefixed}[/bright_black], and then generate a YAML
template for it with [bright_black]nesso models base_model bootstrap-yaml {base_model_name}[/bright_black].""",  # noqa
            width=100,
        )
    )


@app.command()
def bootstrap_yaml(
    base_model_name: Annotated[
        str, typer.Argument(help="The name of the base model.", show_default=False)
    ],
    env: options.environment = config.DEFAULT_ENV,
    technical_owner: options.technical_owner = None,
    business_owner: options.business_owner = None,
    snakecase_columns: Annotated[
        Optional[bool],
        typer.Option(
            "--snakecase-columns",
            "-sc",
            help="""Whether to standardize column names to snakecase.""",
            is_flag=True,
        ),
    ] = True,
):
    """
    Bootstrap the YAML file for a base model.

    The base model must already be materialized with `dbt run`.
    """

    dbt_project_dir = Path(context.get("PROJECT_DIR"))

    prefix = config.SILVER_SCHEMA_PREFIX

    if prefix and base_model_name.startswith(prefix):
        raise ValueError("Please specify the model name without prefix.")

    if config.SILVER_SCHEMA_PREFIX:
        base_model_name = f"{prefix}_{base_model_name}"

    base_dir = dbt_project_dir / "models" / config.SILVER_SCHEMA / base_model_name
    yml_path = base_dir / f"{base_model_name}.yml"

    yaml_path_short = Path(
        "models",
        config.SILVER_SCHEMA,
        base_model_name,
        base_model_name + ".yaml",
    )

    if prefix:
        base_model_name_no_prefix = base_model_name.replace(prefix + "_", "")
    else:
        base_model_name_no_prefix = base_model_name

    args = {
        "model_name": base_model_name_no_prefix,
        "technical_owner": technical_owner,
        "business_owner": business_owner,
        "snakecase_columns": snakecase_columns,
        "base_model_prefix": prefix,
        "bootstrapped_base_model": True,
    }
    generate_model_yaml_cmd = (
        f"""dbt -q run-operation generate_model_yaml --args '{args}' --target {env}"""
    )
    base_model_yaml_content = call_shell(
        generate_model_yaml_cmd,
        print_logs=False,
    )
    with open(yml_path, "w") as file:
        file.write(base_model_yaml_content)

    print(
        f"YAML template for base model {yaml_path_short} has been crated successfully."  # noqa
    )


if __name__ == "__main__":
    app()
