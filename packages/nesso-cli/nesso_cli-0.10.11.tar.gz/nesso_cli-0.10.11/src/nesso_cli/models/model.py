from pathlib import Path

import typer
from rich import print
from rich.panel import Panel
from typing_extensions import Annotated

from nesso_cli.models import context
from nesso_cli.models.common import call_shell, options
from nesso_cli.models.config import config

app = typer.Typer()


def _get_model_dir(model_name: str) -> Path:
    """
    Retrieve the directory where a model (SQL file) is located.

    Args:
        model_name (str): The name of the model to retrieve.

    Raises:
        FileNotFoundError: If the specified model is not found.

    Returns:
        Path: The path to the model directory.
    """
    dbt_project_dir = Path(context.get("PROJECT_DIR"))
    models_path = dbt_project_dir.joinpath("models", config.GOLD_LAYER_NAME)
    for path in models_path.rglob(model_name):
        if path.is_dir():
            return path
    raise FileNotFoundError(f"Model '{model_name}' not found in directory tree.")


@app.command()
def bootstrap(
    model: Annotated[
        str, typer.Argument(help="The name of the model.", show_default=False)
    ],
    subdir: Annotated[
        str,
        typer.Option(
            "-s",
            "--subdir",
            help="Subdirectory inside the gold layer where the model should be located.",  # noqa
        ),
    ] = None,
):
    """
    Generates an empty <MODEL_NAME>/<MODEL_NAME>.sql file in the `models` directory.
    """
    nesso_project_dir = Path(context.get("PROJECT_DIR"))
    project_dir = nesso_project_dir.joinpath(
        "models", config.GOLD_LAYER_NAME, subdir or ""
    )
    model_dir = project_dir.joinpath(model)

    if not model_dir.exists():
        model_dir.mkdir(parents=True, exist_ok=True)

    sql_path = model_dir.joinpath(model + ".sql")

    sql_path.touch(exist_ok=True)
    sql_path_short = Path(
        "models", config.GOLD_LAYER_NAME, subdir or "", model, model + ".sql"
    )
    print(
        f"File [bright_black]{sql_path_short}[/bright_black] has been created [green]successfully[/green]."  # noqa
    )

    print("Model bootstrapping is [green]complete[/green].")

    sql_path_clickable = nesso_project_dir.name / sql_path_short
    print(
        Panel(
            f"""Once you populate the model file ([link={sql_path}]{sql_path_clickable}[/link]),
you can materialize it with [bright_black]nesso models run -s {model}[/bright_black], and then generate a YAML
template for it with [bright_black]nesso models model bootstrap-yaml {model}[/bright_black].""",  # noqa
            width=100,
        )
    )


@app.command()
def bootstrap_yaml(
    model: Annotated[
        str, typer.Argument(help="The name of the model.", show_default=False)
    ],
    technical_owner: options.technical_owner = None,
    business_owner: options.business_owner = None,
    domains: options.domains = None,
    env: options.environment = config.DEFAULT_ENV,
):
    """
    Bootstrap the YAML file for a particular model*.

    *The model must already be materialized.
    """

    model_dir = _get_model_dir(model_name=model)

    print(f"Creating YAML for model [blue]{model}[/blue]...")
    yml_path = model_dir.joinpath(model + ".yml")

    args = {
        "model_name": model,
        "technical_owner": technical_owner,
        "business_owner": business_owner,
        "domains": domains,
        "upstream_metadata": True,
        "snakecase_columns": False,
    }
    generate_model_yaml_text_command = (
        f"""dbt -q run-operation generate_model_yaml --args '{args}' --target {env}"""
    )

    model_yaml_text = call_shell(generate_model_yaml_text_command, print_logs=False)

    with open(yml_path, "w") as file:
        file.write(model_yaml_text)

    print(
        f"YAML template for model [blue]{model}[/] has been created [green]successfully[/]."  # noqa
    )


if __name__ == "__main__":
    app()
