from .constants import (
    SUPPORTED_AUTHENTITACTION_METHODS,
    ACCOUNT_IDENTIFIER_ENV_VAR,
    DATABASE_ENV_VAR,
    SCHEMA_ENV_VAR,
    WAREHOUSE_ENV_VAR,
    USER_ENV_VAR,
    OAUTH_HOST_ENV_VAR,
    OAUTH_TOKEN_ENV_VAR,
)
from .exceptions import (
    MultipleAuthMethodsSpecified,
    AuthenticatorNotSupported,
    ConstructorArgumentMissing,
    DependencyNotInstalled,
    InvalidReturnType,
    InvalidFetchStrategy,
)


class Snowflake:
    """
    Snowflake connector wrapper.
    APIs are designed to make it as easy as possible to do the following from Metaflow tasks and Outerbounds workstations:
        1. move data from Snowflake tables into Arrow tables or Pandas DataFrames.
        2. move data from Arrow tables or Pandas DataFrames into Snowflake tables.
    """

    def __init__(self, **kwargs):
        import os

        self.kwargs = kwargs

        # Check if required arguments are provided, or if they are in the environment.
        if "account" not in self.kwargs:
            try:
                self.kwargs["account"] = os.environ[ACCOUNT_IDENTIFIER_ENV_VAR]
            except KeyError as e:
                raise ConstructorArgumentMissing(
                    f"Snowflake account neither provided in {ACCOUNT_IDENTIFIER_ENV_VAR} environment variable nor Connector constructor."
                )
        if "user" not in self.kwargs:
            try:
                self.kwargs["user"] = os.environ[USER_ENV_VAR]
            except KeyError as e:
                raise ConstructorArgumentMissing(
                    f"Snowflake user neither provided in {USER_ENV_VAR} environment variable nor Connector constructor."
                )

        # TODO: Should `role` be a required argument?

        # Check if optional args are provided.
        for arg_name, env_var in [
            ("database", DATABASE_ENV_VAR),
            ("schema", SCHEMA_ENV_VAR), 
            ("warehouse", WAREHOUSE_ENV_VAR),
        ]:
            if arg_name in self.kwargs:
                continue
            try:
                self.kwargs[arg_name] = os.environ[env_var]
            except KeyError as e:
                pass

        # Set the authentication method and corresponding arguments.
        try: 
            env_has_oauth_vars = os.environ[OAUTH_HOST_ENV_VAR] is not None and os.environ[OAUTH_TOKEN_ENV_VAR] is not None
            self.kwargs["authenticator"] = 'oauth'
        except KeyError as e:
            pass
        if "authenticator" in self.kwargs and self.kwargs["authenticator"] == 'oauth':
            # Ensure single auth method is specified.
            if "password" in self.kwargs:
                raise MultipleAuthMethodsSpecified(
                    "`password` and `authenticator` cannot both be set in snowflake.connector args."
                )

            # OAuth needs host and token to be set.
            if "host" not in self.kwargs:
                try:
                    self.kwargs["host"] = os.environ[OAUTH_HOST_ENV_VAR]
                except KeyError as e:
                    raise ConstructorArgumentMissing(
                        f"Snowflake OAuth host neither provided in {OAUTH_HOST_ENV_VAR} environment variable nor Connector constructor."
                    )
            if "token" not in self.kwargs:
                try:
                    self.kwargs["token"] = os.environ[OAUTH_TOKEN_ENV_VAR]
                except KeyError as e:
                    raise ConstructorArgumentMissing(
                        f"Snowflake OAuth token neither provided in {OAUTH_TOKEN_ENV_VAR} environment variable nor Connector constructor."
                    )

        else:
            if "password" not in self.kwargs:
                try:
                    self.kwargs["password"] = os.environ["SNOWFLAKE_PASSWORD"]
                except KeyError as e:
                    raise ConstructorArgumentMissing(
                        "Snowflake password neither provided in SNOWFLAKE_PASSWORD environment variable nor Connector constructor."
                    )

        self._cursor = self.conn.cursor()
        self._snowpark_session = None

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        self._cursor.close()
        if self._snowpark_session:
            self._snowpark_session.close()

    def close(self):
        self._cursor.close()
        if self._snowpark_session:
            self._snowpark_session.close()

    @property
    def conn(self):
        """
        Returns a connection object.
        https://docs.snowflake.com/en/developer-guide/python-connector/python-connector-connect
        """
        try:
            import snowflake.connector

            return snowflake.connector.connect(**self.kwargs)
        except ModuleNotFoundError as e:
            raise DependencyNotInstalled('Snowflake', 'snowflake-connector-python')

    @property
    def session(self):
        if not self._snowpark_session:
            try:
                from snowflake.snowpark import Session
                self._snowpark_session = Session.builder.configs(self.kwargs).create()
            except ModuleNotFoundError as e:
                raise DependencyNotInstalled('Snowpark', 'snowflake-snowpark-python')
        return self._snowpark_session

    def execute(self, command, run_async=False, return_cursor=True, **kwargs):
        """
        Execute a SQL statement. Minimal wrapper around Snowflake's execute method.

        :param command: SQL command to execute.
        :param async: If True, execute the query asynchronously.

        :return: cursor object if return_cursor is True else None.
        """
        if run_async:
            self._cursor.execute_async(command, **kwargs)
        else:
            self._cursor.execute(command, **kwargs)
        if return_cursor:
            return self._cursor

    def get(self, command, return_type="arrow", fetch_strategy="all", **kwargs):
        """
        Execute a SQL statement.
        https://docs.snowflake.com/en/developer-guide/python-connector/python-connector-api#execute

        :param command: SQL command to execute.
        :param fetch_strategy: Fetch strategy to use. Must be one of: all, one, many.
        :param kwargs: Additional parameters to pass to the execute method.

        :return: Query results.
        """
        if return_type not in ["arrow", "pandas"]:
            raise InvalidReturnType()
        if fetch_strategy not in ["all", "batches"]:
            raise InvalidFetchStrategy()
        self._cursor.execute(command, **kwargs)
        if fetch_strategy == "all" and return_type == "arrow":
            res = self._cursor.fetch_arrow_all()
        elif fetch_strategy == "all" and return_type == "pandas":
            res = self._cursor.fetch_pandas_all()
        elif fetch_strategy == "batches" and return_type == "arrow":
            res = self._cursor.fetch_arrow_batches()
        elif fetch_strategy == "batches" and return_type == "pandas":
            res = self._cursor.fetch_pandas_batches()
        else:
            raise NotImplementedError()
        return res

    def put(self, df, table_name, **kwargs):
        """
        Put a DataFrame into a Snowflake table.
        Wrapper around Snowflake's write_pandas method.
        """
        from snowflake.connector.pandas_tools import write_pandas
        return write_pandas(self.conn, df, table_name, **kwargs)

    def execute_multi_statement(self, command, **kwargs):
        """
        Execute a Snowflake query with multiple statements.

        This is not supported by default in Snowflake's Python connector.
        So we need to split the statements and execute them one by one.
        """
        statements = command.split(';')
        for statement in statements:
            lines = statement.split('\n')
            clean_statement = ""
            for line in lines:
                line = line.strip()
                if not line.startswith("--"):
                    clean_statement += line + '\n'
            self.execute(clean_statement, return_cursor=False, **kwargs)

        