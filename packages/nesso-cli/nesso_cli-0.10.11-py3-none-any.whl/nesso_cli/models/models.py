import copy
from enum import Enum
from pathlib import Path
from typing import Any, Literal, Optional, Tuple, Union

try:
    # dbt <= 1.3
    from dbt.contracts.graph.parsed import ColumnInfo
except Exception:
    # dbt > 1.3
    from dbt.contracts.graph.nodes import ColumnInfo

from pydantic import BaseModel, Field, create_model

from nesso_cli.models.common import (
    DbtProject,
    get_current_dbt_project_obj,
    get_db_table_columns,
    snakecase,
    yaml,
)
from nesso_cli.models.config import config


class BaseNessoModel(BaseModel):
    def to_dict(self):
        # Convert to dictionary, excluding fields with None values,
        # as dbt >= 1.5 doesn't accept None in the `tests` field.
        return self.dict(exclude_none=True, by_alias=True)


class ColumnMeta(BaseModel):
    name: str
    data_type: str
    description: str = ""
    quote: bool = True
    # Convert model to dictionary with `exclude_none=True` due to
    # dbt >= 1.5 not accepting None in 'tests' field.
    tests: Optional[list[str]] = None
    tags: list[str] = []


class Owner(BaseModel):
    type: str
    email: str = "None"


class SourceTable(BaseModel):
    name: str
    description: str = ""
    loaded_at_field: str = "_viadot_downloaded_at_utc::timestamp"
    tags: list[str] = []
    meta: dict[str, Any]
    columns: list[ColumnMeta]
    freshness: dict[str, dict[str, Union[int, str]]] = {
        "warn_after": {"count": 24, "period": "hour"},
        "error_after": {"count": 48, "period": "hour"},
    }


class Model(BaseModel):
    name: str
    description: str = ""
    meta: dict[str, Any]
    columns: list[ColumnMeta]


class Source(BaseModel):
    name: str
    schema_: str = Field(alias="schema")
    description: Optional[str] = None
    tables: list[SourceTable]


class SourceProperties(BaseNessoModel):
    version: int = 2
    sources: list[Source]


class ModelProperties(BaseNessoModel):
    version: int = 2
    models: list[Model]


class DBTDatabaseConfig(BaseModel):
    """Common DBT database configuration (for most databases)."""

    db_type: str = Field(default=None, alias="type")
    host: str = "localhost"
    schema_: str = Field(default="dbt_nesso_user", alias="schema")
    threads: int = 16
    retries: int = 1
    # connect_timeout: int = None


class DBTTrinoConfig(DBTDatabaseConfig):
    db_type: str = Field(default="trino", alias="type")
    port: int = 8080
    database: str = "default"
    user: str = "nesso_user"


class DBTPostgresConfig(DBTDatabaseConfig):
    db_type: str = Field(default="postgres", alias="type")
    port: int = 5432
    dbname: str = "postgres"
    user: str = "nesso_user"
    password: str = ""


class DBTRedshiftConfig(DBTPostgresConfig):
    db_type: str = Field(default="redshift", alias="type")


class DBTDatabricksConfig(DBTDatabaseConfig):
    db_type: str = Field(default="databricks", alias="type")
    http_path: str = "sql/protocolv1/o/<workspace-id>/<cluster-id>"
    token: str = ""
    session_properties: dict = {
        "query_max_planning_time": "2m",
        "query_max_run_time": "60m",
        "retry_initial_delay": "1s",
        "retry_max_delay": "30s",
        "late_materialization": True,
    }


class DBTSQLServerConfig(DBTDatabaseConfig):
    db_type: str = Field(default="sqlserver", alias="type")
    driver: str = "Microsoft ODBC Driver 17 for SQL Server"
    port: int = 1433
    database: str = "dbo"
    login_timeout: int = 10
    query_timeout: int = 3600
    user: str = "nesso_user"
    password: str = "nesso_password"


class DBTDuckDBConfig(BaseModel):
    db_type: str = Field(default="duckdb", alias="type")
    schema_: str = Field(default="main", alias="schema")
    path: str = "nesso.duckdb"
    threads: int = 16
    num_retries: int = 1


def NessoDBTConfig(
    db_type: str, project_name: str = "my_nesso_project"
) -> "NessoDBTConfig":
    config_class = get_dbt_config_class(db_type)
    config = {"target": "dev", "outputs": {"dev": config_class()}}
    model = create_model(
        "NessoDBTConfig", **{project_name: (dict, {project_name: config})}
    )
    return model(**{project_name: config})


dbt_config_map = {
    "trino": DBTTrinoConfig,
    "postgres": DBTPostgresConfig,
    "redshift": DBTRedshiftConfig,
    "databricks": DBTDatabricksConfig,
    "sqlserver": DBTSQLServerConfig,
    "duckdb": DBTDuckDBConfig,
}


def get_dbt_config_class(dbt_db_type: str) -> DBTDatabaseConfig:
    """
    A factory method-ish helper for getting the correct dbt config class
    depending on the database used.

    Args:
        dbt_db_type (str): One of the supported dbt database types.

    Raises:
        NotImplementedError: If a non-supported database type is passed.

    Returns:
        DBTDatabaseConfig: The pydantic model for the configuration
            of the specified database.
    """

    if dbt_db_type not in dbt_config_map:
        raise NotImplementedError(f"Unsupported database type: '{dbt_db_type}'.")

    config_class = dbt_config_map[dbt_db_type]
    return config_class


class ModelColumnsMetadata(BaseModel):
    quote: bool
    data_type: str
    description: Optional[str]
    tests: Optional[list[str]]
    tags: list[str]


class DBTResourceType(Enum):
    SOURCE = "sources"
    MODEL = "models"


class DBTProperties(dict):
    def __init__(self, file_path: Union[str, Path]):
        self.file_path = file_path
        self.__resource_type = None
        self._load_properties()
        self.__modification_time = self.file_path.stat().st_mtime

    def _load_properties(self):
        """Loads dbt properties from the specified YAML file
        and saves it to the object."""
        with open(self.file_path, "r") as file:
            yaml_dict = yaml.load(file)

        for key in yaml_dict:
            if key not in self.keys():
                self[key] = yaml_dict[key]

    @property
    def resource_type(self):
        """Determines the resource type based on the content of the file."""
        if DBTResourceType.SOURCE.value in self:
            self.__resource_type = DBTResourceType.SOURCE.value
            return self.__resource_type
        elif DBTResourceType.MODEL.value in self:
            self.__resource_type = DBTResourceType.MODEL.value
            return self.__resource_type
        else:
            msg = "Unsupported dbt resource type (must be either a source or a model)."
            raise ValueError(msg)

    def set_yaml_content(self):
        """Write the content of a dictionary to a YAML file."""
        with open(self.file_path, "w") as file:
            yaml.dump(dict(self), file)

        self.__modification_time = self.file_path.stat().st_mtime

    def set_columns_order(
        self,
        desired_order: list[str],
        table_name: str,
    ) -> None:
        """
        Reorders columns in a specified table in a YAML file.

        Args:
            desired_order (list[str]): List of column names in the desired order.
            table_name (str): Name of the table to reorder columns in.
        """

        def custom_sort(item):
            return desired_order.index(item["name"])

        for content in self[self.resource_type]:
            if self.resource_type == DBTResourceType.SOURCE.value:
                for table in content["tables"]:
                    if table["name"] == table_name:
                        table["columns"] = sorted(table["columns"], key=custom_sort)
            elif self.resource_type == DBTResourceType.MODEL.value:
                content["columns"] = sorted(content["columns"], key=custom_sort)

        self.set_yaml_content()

    def get_yaml_table_columns(
        self,
        table_name: str,
    ) -> dict[str, ModelColumnsMetadata]:
        """
        Retrieve column information for a specific table from a YAML file.

        Args:
            table_name (str): The name of the table for which to retrieve column names.

        Returns:
            columns_dict_metadata (dict[str, ModelColumnsMetadata]): A dictionary
                containing columns and their metadata.
        """
        # Checks the validity of dbt properties
        if self.__modification_time != self.file_path.stat().st_mtime:
            raise ValueError("The file was modified during the processing.")

        def create_metadata_dict(
            column: dict[str, Any]
        ) -> dict[str, ModelColumnsMetadata]:
            # Creates a dict with only metadata (without column name).
            column_metadata = column.copy()
            del column_metadata["name"]
            # Verifies if metadata types align with those specified in
            # ModelColumnsMetadata.
            ModelColumnsMetadata.validate(column_metadata)
            return column_metadata

        columns_dict_metadata = {}
        for content in self[self.resource_type]:
            if self.resource_type == DBTResourceType.SOURCE.value:
                for table in content["tables"]:
                    if table["name"] == table_name:
                        for column in table["columns"]:
                            column_metadata = create_metadata_dict(column)
                            # Creates a dictionary with column names and their metadata,
                            # for example: {column_name: {metadata}}
                            columns_dict_metadata.update(
                                {column["name"]: column_metadata}
                            )

            elif self.resource_type == DBTResourceType.MODEL.value:
                for column in content["columns"]:
                    column_metadata = create_metadata_dict(column)
                    # Creates a dictionary with column names and their metadata,
                    # for example: {column_name: {metadata}}
                    columns_dict_metadata.update({column["name"]: column_metadata})

        return columns_dict_metadata

    @staticmethod
    def dict_diff(dict1: dict[Any, Any], dict2: dict[Any, Any]) -> dict[Any, Any]:
        """
        Finds the differences between two dictionaries. Performs unions difference
        of two sets operation.

        Args:
            dict1 (dict[Any, Any]): The first dictionary.
            dict2 (dict[Any, Any]): The second dictionary.

        Returns:
            dict[Any, Any]:
                If the dictionaries are not equal, returns a dictionary containing
                the differing key-value pairs.
                If the dictionaries are equal, returns empty dictionary.
        """
        if dict1 != dict2 or dict2 != dict1:
            result = dict(dict1.items() - dict2.items())
            result2 = dict(dict2.items() - dict1.items())
            final_result = result | result2

            return final_result

        return {}

    def coherence_scan(
        self,
        table_name: str,
        schema_name: Optional[str] = None,
        env: Optional[str] = None,
    ) -> Tuple[dict[str, str], dict[str, ModelColumnsMetadata], dict[str, str]]:
        """
        Scan for differences between the model metadata in the YAML file
            and the database.

        Args:
            table_name (str): Name of the table to compare.
            schema_name (Optional[str], optional): Name of the schema.
                Required when scanning source. Defaults to None.
            env (Optional[str], optional): The name of the environment.
                Defaults to None.

        Returns:
            Tuple[dict[str, str], dict[str, ModelColumnsMetadata], dict[str, str]]:
                A tuple containing three dictionaries:
                    1. diff (dict[str, str]): A dictionary containing
                        differences between database columns and YAML columns,
                        or False if no differences are found.
                    2. yaml_columns_metadata (dict[str, ModelColumnsMetadata]):
                        A dictionary containing columns and their metadata
                        from the YAML file.
                    3. db_columns (dict[str, str]): A dictionary representing columns
                        from the database.
        """
        yaml_columns_metadata = self.get_yaml_table_columns(table_name=table_name)

        db_columns = get_db_table_columns(
            schema_name=schema_name, table_name=table_name, env=env
        )

        # Normalize the dictionary in order to compare to the metadata retrieved
        # from the database.
        yaml_columns = {
            col: meta["data_type"] for col, meta in yaml_columns_metadata.items()
        }
        diff = DBTProperties.dict_diff(db_columns, yaml_columns)

        return diff, yaml_columns_metadata, db_columns

    def add_column(
        self,
        table_name: str,
        column_name: str,
        index: int,
        data_type: str,
        description: str = "",
        tags: list[str] = [],
        quote: bool = True,
        tests: Optional[list[str]] = None,
    ) -> None:
        """
        Add a new column to a model in a YAML file.

        Args:
            table_name (str): Name of the table to which the column will be added.
            column_name (str): Name of the new column.
            index (int): Index at which the new column will be inserted.
            data_type (str): Data type of the new column.
            description (str, optional): Description for the new column.
                Defaults to "".
            tags (list[str], optional): Tags associated with the new column.
                Defaults to [].
            quote (bool, optional): Whether the name of the column should be quoted.
                Defaults to True.
            tests (list[str] or None, optional): List of tests associated
                with the column. Defaults to None.
        """
        metadata = {
            "name": column_name,
            "quote": quote,
            "data_type": data_type,
            "description": description,
            "tags": tags,
        }

        # Do not add the "tests" key at all if tests are not specified.
        if tests:
            metadata.update({"tests": tests})

        for content in self[self.resource_type]:
            if self.resource_type == DBTResourceType.SOURCE.value:
                for table in content["tables"]:
                    if table["name"] == table_name:
                        table["columns"].insert(index, metadata)
            elif self.resource_type == DBTResourceType.MODEL.value:
                content["columns"].insert(index, metadata)

        self.set_yaml_content()

    def delete_column(
        self,
        table_name: str,
        column_name: str,
    ) -> None:
        """
        Delete a column from a table in the YAML file.

        Args:
            table_name (str): Name of the table from which the column will be deleted.
            column_name (str): Name of the column to be deleted.
        """

        for content in self[self.resource_type]:
            if self.resource_type == DBTResourceType.SOURCE.value:
                for table in content["tables"]:
                    if table["name"] == table_name:
                        columns = table["columns"]

                        for column in columns:
                            if column["name"] == column_name:
                                columns.remove(column)

            elif self.resource_type == DBTResourceType.MODEL.value:
                for column in content["columns"]:
                    if column["name"] == column_name:
                        content["columns"].remove(column)

        self.set_yaml_content()

    def update_column(
        self,
        table_name: str,
        column_name: str,
        index: int,
        data_type: str,
        description: str,
        tags: list[str],
        quote: bool,
        tests: Optional[list[str]],
    ) -> None:
        """
        Updates a column in a YAML file by deleting the existing column
        and adding a new column in its place.

        Args:
            table_name (str): The name of the table from which the column
                will be updated.
            column_name (str): The name of the column to be updated.
            index (int): The index where the new column should be added.
            data_type (str): The data type of the new column.
            description (str, optional): Description for the new column.
                Defaults to "".
            tags (list[str], optional): Tags associated with the new column.
                Defaults to [].
            quote (bool, optional): Whether the name of the column should be quoted.
                Defaults to True.
            tests (list[str] or None, optional): List of tests associated
                with the column. Defaults to None.
        """
        self.delete_column(
            table_name=table_name,
            column_name=column_name,
        )
        self.add_column(
            table_name=table_name,
            column_name=column_name,
            index=index,
            data_type=data_type,
            description=description,
            tags=tags,
            quote=quote,
            tests=tests,
        )

    def synchronize_columns(
        self,
        diff: dict[str, str],
        yaml_columns: dict[str, ModelColumnsMetadata],
        db_columns: dict[str, str],
        table_name: str,
    ) -> None:
        """
        Synchronizes columns between a YAML schema definition and a database table.

        Args:
            diff (dict[str, str]): Dictionary of column names and data types
                from YAML vs database.
            yaml_columns (dict[str, ModelColumnsMetadata]): Columns and metadata
                from YAML schema.
            db_columns (dict[str, str]): Columns and data types from
                the database schema.
            table_name (str): Name of the table being synchronized.
        """
        db_column_names = list(db_columns.keys())

        for column_name, column_data_type in diff.items():
            db_column_data_type = db_columns.get(column_name)
            # In the database but not in YAML.
            if column_name not in yaml_columns:
                self.add_column(
                    table_name=table_name,
                    column_name=column_name,
                    index=db_column_names.index(column_name),
                    data_type=column_data_type,
                )

            # In the YAML but not in the database.
            elif column_name in yaml_columns and column_name not in db_columns:
                self.delete_column(
                    table_name=table_name,
                    column_name=column_name,
                )

            # Data type has changed.
            elif (
                db_column_data_type is not None
                and db_column_data_type != column_data_type
            ):
                self.update_column(
                    table_name=table_name,
                    column_name=column_name,
                    index=db_column_names.index(column_name),
                    data_type=db_column_data_type,
                    description=yaml_columns[column_name].get("description"),
                    tags=yaml_columns[column_name].get("tags"),
                    quote=yaml_columns[column_name].get("quote"),
                    tests=yaml_columns[column_name].get("tests"),
                )

        # Overwrites `yaml_columns` with the current state of the columns
        # from the YAML file.
        yaml_columns = self.get_yaml_table_columns(table_name=table_name)
        db_columns_list = list(db_columns.keys())
        yaml_columns_list = list(yaml_columns.keys())

        # Reorder columns in the YAML to match the schema in the database.
        if yaml_columns_list != db_columns_list:
            self.set_columns_order(
                desired_order=db_columns_list,
                table_name=table_name,
            )


class DBTModel:

    def __init__(
        self,
        model_name: str,
        dbt_project: Optional[DbtProject] = None,
        env: str = config.DEFAULT_ENV,
        meta_config: Optional[dict[str, Any]] = None,
        **meta,
    ) -> None:
        """
        Initialize a DBTModel object with specified parameters.

        Args:
            model_name (str): The name of the model.
            dbt_project (Optional[DbtProject], optional): The associated dbt project.
                Defaults to None.
            env (str, optional): The environment for fetching the DBT project.
                Defaults to config.DEFAULT_ENV.
            meta_config (dict[str, Any], optional): Dictionary containing configuration
                of meta fields. Defaults to None.
            meta (dict[str, Any], optional): Keyword arguments specifying metadata
                fields.
        """
        self.model_name = model_name
        if not dbt_project:
            dbt_project = get_current_dbt_project_obj(target=env, recompile=True)
        self.dbt_project = dbt_project
        self.manifest = self.dbt_project.manifest
        if not meta_config:
            # Workaround until https://github.com/dyvenia/nesso-cli/issues/5 is merged.
            meta_config = {
                "owners": {
                    "enabled": True,
                    "default": [
                        {"type": "Technical owner", "email": ""},
                        {"type": "Business owner", "email": ""},
                    ],
                    "inheritance_strategy": "skip",
                },
                "domains": {
                    "enabled": True,
                    "default": [],
                    "inheritance_strategy": "append",
                },
                "true_source": {
                    "enabled": True,
                    "default": [],
                    "inheritance_strategy": "append",
                },
                "SLA": {
                    "enabled": True,
                    "default": "24 hours",
                    "inheritance_strategy": "skip",
                },
            }
        self.meta_config = meta_config
        self.meta = meta

    def get_model_upstream_dependencies(self) -> list[str]:
        """
        Retrieve the upstream dependencies of a given model one level deep.

        Raises:
            ValueError: If the dependencies for model were not found in the manifest.

        Returns:
            list[str]: A list of model dependencies names.
        """
        for node in self.manifest.nodes.values():
            if node.name == self.model_name:
                return node.depends_on.nodes
        raise ValueError(f"Dependencies for model '{self.model_name}' were not found.")

    def _convert_node_columns_to_pydantic_model(
        self, columns: dict[str, ColumnInfo]
    ) -> list[ColumnMeta]:
        """
        Convert columns metadata from dbt.ColumnInfo object into
            Pydantic model ColumnMeta.

        Args:
            columns (dict[str, ColumnInfo]): Dictionary containing column information.

        Returns:
            list[ColumnMeta]: List of ColumnMeta objects.
        """
        columns_values = list(columns.values())
        columns_metadata = [
            ColumnMeta(
                name=col.name,
                data_type=col.data_type,
                description=col.description,
                quote=col.quote,
                tags=col.tags,
            )
            for col in columns_values
        ]
        return columns_metadata

    def get_node_metadata(self, node_name: str) -> Union[SourceTable, Model]:
        """
        Retrieve metadata for a given node.

        Args:
            node_name (str): dbt project node name. Example of node name format
                "source.postgres.staging.test_table_account".

        Raises:
            ValueError: If the node is not found.

        Returns:
            Union[SourceTable, Model]: Metadata for the given node.
        """
        node_name_fqn = node_name.split(".")
        node_type = node_name_fqn[0]
        node_table_name = node_name_fqn[-1]
        if node_type == "source":
            for node in self.manifest.sources.values():
                if node.name == node_table_name:
                    metadata = SourceTable(
                        name=node.name,
                        description=node.description,
                        meta=node.meta,
                        columns=self._convert_node_columns_to_pydantic_model(
                            columns=node.columns
                        ),
                    )
                    return metadata
        elif node_type == "model":
            for node in self.manifest.nodes.values():
                if node.name == node_table_name:
                    metadata = Model(
                        name=node.name,
                        description=node.description,
                        meta=node.meta,
                        columns=self._convert_node_columns_to_pydantic_model(
                            columns=node.columns
                        ),
                    )
                    return metadata
        else:
            raise ValueError(f"Node '{node_name}' was not found.")

    def get_upstream_metadata(
        self, upstream_dependencies: Optional[list[str]] = None
    ) -> list[Union[SourceTable, Model]]:
        """Retrieve metadata for upstream dependencies.

        Args:
            upstream_dependencies (Optional[list[str]], optional): List of upstream
                dependencies. Defaults to None.

        Returns:
            list[Union[SourceTable, Model]]: List of metadata objects
                for given dependencies.
        """
        if upstream_dependencies is None:
            upstream_dependencies = self.get_model_upstream_dependencies()

        upstream_metadata = [
            self.get_node_metadata(node_name=dependency)
            for dependency in upstream_dependencies
        ]

        return upstream_metadata

    def get_columns(self, snakecase_columns: bool = True) -> list[ColumnMeta]:
        """Retrieves columns for the model from the database.

        Args:
            snakecase_columns (bool, optional): Whether to standardize columns
                names to snakecase in the model. Defaults to True.

        Raises:
            ValueError: If the specified model node cannot be found.

        Returns:
            list[ColumnMeta]: List of ColumnMeta objects.
        """

        node = self.dbt_project.get_ref_node(target_model_name=self.model_name)

        if node is None:
            raise ValueError(f"Could not find node for table '{self.model_name}'.")

        columns_list, *_ = self.dbt_project.get_columns_in_node(node)

        columns_metadata = []
        for column in columns_list:
            columns_metadata.append(
                ColumnMeta(
                    name=(snakecase(column.name) if snakecase_columns else column.name),
                    data_type=column.data_type.upper(),
                )
            )

        return columns_metadata

    def resolve_columns_metadata(
        self,
        upstream_metadata: Optional[list[Union[SourceTable, Model]]] = None,
        snakecase_columns: bool = True,
    ) -> list[ColumnMeta]:
        """Inherit column metadata from upstream resource(s).

        In case of multiple upstream resources, inherits on a "first come, first served"
        basis.

        Args:
            upstream_metadata (Optional[list[Union[SourceTable, Model]]], optional):
                List of upstream metadata. Defaults to None.
            snakecase_columns (bool, optional): Whether to standardize columns
                names to snakecase in the model. Defaults to True.

        Returns:
            list[ColumnMeta]: List of resolved model column metadata.
        """
        if not upstream_metadata:
            upstream_metadata = self.get_upstream_metadata()

        model_columns = self.get_columns(snakecase_columns=snakecase_columns)

        for model_column in model_columns:
            for dependency in upstream_metadata:
                upstream_column = next(
                    (
                        col
                        for col in dependency.columns
                        if col.name == model_column.name
                    ),
                    None,
                )
                if upstream_column:
                    self._resolve_column_values(model_column, upstream_column)

        return model_columns

    def _resolve_column_values(
        self, model_column: ColumnMeta, upstream_column: ColumnMeta
    ):
        """Resolve column metadata.

        In case of a `None` value, inherit the first encountered upstream column value
        for that field.

        Args:
            model_column (ColumnMeta): Model column metadata to be overwritten if empty.
            upstream_column (ColumnMeta): Upstream model column metadata to be used to
                overwrite model column fields.
        """
        for attribute in model_column.__fields__:
            value = getattr(model_column, attribute)
            if attribute != "tests" and not value:
                setattr(model_column, attribute, getattr(upstream_column, attribute))

    def _set_meta_value(
        self,
        meta: dict[str, Any],
        field_name: str,
        upstream_value: Any,
        inheritance_strategy: Literal["overwrite", "skip", "append"],
        default_value: Any,
    ) -> dict[str, Any]:
        """Set a meta field to a value based on the specified inheritance strategy.

        There are three available strategies:
        - append: extend upstream values with new values specified in `self.meta`. Only
            supported for meta keys of type `list`.
        - skip: do not inherit from upstream values, ie. take user-specified value or
            the default
        - overwrite: use upstream metadata over user-specified values

        Args:
            meta (dict[str, Any]): Dictionary with data to set.
            field_name (str): Filed name to update.
            upstream_value (Any): Upstream value for specified `field_name`.
            inheritance_strategy (Literal[overwrite, skip, append]): One of three
                possible inheritance strategies.
            default_value (Any): Default value for specified `field_name`.

        Raises:
            ValueError: If unknown inheritance strategy was specified.

        Returns:
            dict[str, Any]: Updated dictionary with meta fields.
        """
        if inheritance_strategy == "append":
            if isinstance(upstream_value, list):
                meta[field_name].extend(upstream_value)
            else:
                meta[field_name].append(upstream_value)
        elif inheritance_strategy == "overwrite":
            meta[field_name] = upstream_value
        elif inheritance_strategy == "skip":
            if meta[field_name] != default_value:
                pass
            else:
                meta[field_name] = default_value
        else:
            raise ValueError(f"Unknown inheritance strategy: '{inheritance_strategy}'.")

        return meta

    def _resolve_resource_level_metadata_values(
        self,
        upstream_metadata: list[Union[SourceTable, Model]],
    ) -> dict[str, Any]:
        """Resolve resource-level (as opposed to column-level) metadata.

        Resolve resource metadata with its upstream metadata using the inheritance
        strategy specified in the nesso-cli config.

        Args:
            upstream_metadata (list[Union[SourceTable, Model]]): List of upstream
                metadata objects.

        Returns:
            dict[str, Any]: Dictionary containing resolved metadata.
        """

        # Selects parameters from self.meta corresponding to those from the Meta model.
        meta = copy.deepcopy(self.meta)

        # If a meta key is not specified, take the default value from config.
        for key in self.meta_config.keys():
            if key not in meta:
                meta[key] = self.meta_config[key]["default"]

        # Set values in meta fields based on meta_config.
        for dependency in upstream_metadata:
            for key, value in dependency.meta.items():
                inheritance_strategy = self.meta_config[key]["inheritance_strategy"]
                default_value = self.meta_config[key]["default"]
                if key in meta:
                    meta = self._set_meta_value(
                        meta=meta,
                        field_name=key,
                        inheritance_strategy=inheritance_strategy,
                        upstream_value=value,
                        default_value=default_value,
                    )

        # Delete duplicates from meta fields.
        for key, value in meta.items():
            if isinstance(value, list):
                if not any(isinstance(item, dict) for item in value):
                    meta[key] = list(dict.fromkeys(value))

        return meta

    def resolve_model_metadata(self, snakecase_columns: bool = True) -> Model:
        """Inherit metadata from upstream resource.

        Args:
            snakecase_columns (bool, optional): Whether to standardize columns
                names to snakecase in the model. Defaults to True.

        Returns:
            Model: Pydantic object with metadata.
        """

        upstream_metadata = self.get_upstream_metadata()
        resource_metadata = self._resolve_resource_level_metadata_values(
            upstream_metadata
        )
        column_metadata = self.resolve_columns_metadata(
            upstream_metadata=upstream_metadata, snakecase_columns=snakecase_columns
        )

        return Model(
            name=self.model_name, meta=resource_metadata, columns=column_metadata
        )
