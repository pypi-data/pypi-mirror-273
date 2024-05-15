from typing import Any

from logger_local.MetaLogger import MetaLogger

from .constants import LOGGER_CONNECTOR_CODE_OBJECT


class Cursor(metaclass=MetaLogger, object=LOGGER_CONNECTOR_CODE_OBJECT):
    def __init__(self, cursor) -> None:
        self.cursor = cursor

    # TODO: If environment <> prod1 and dvlp1 break down using 3rd party package and analyze the formatted_sql
    #  and call private method _validate_select_table_name(table_name)
    def execute(self, sql_statement: str, sql_parameters: tuple or list = None) -> None:
        # TODO: validate_select_table_name(table_name)
        if sql_parameters:
            quoted_parameters = tuple("'" + str(param) + "'" for param in sql_parameters)
            formatted_sql = sql_statement % quoted_parameters
            sql_parameters_str = ", ".join(quoted_parameters)
        else:
            formatted_sql = sql_statement
            sql_parameters_str = "None"
        self.logger.info('database-mysql-local cursor.py execute()', object={
            "formatted_sql": formatted_sql,
            "sql_parameters": sql_parameters_str,
            "sql_statement": sql_statement
        })
        self.cursor.execute(sql_statement, sql_parameters)

    def executemany(self, sql_statement: str, sql_parameters: tuple or list = None) -> None:
        try:
            if sql_parameters:  # sql_parameters is list of tuples, each tuple is a row
                sql_parameters_str = [tuple(f'"{param}"' if not isinstance(param, str) else param for param in sql_parameter) for sql_parameter in sql_parameters]
                # Num of placeholders is the same as the num of columns in the table,
                # but there are multiple rows in sql_parameters, so we should add more placeholders before formatting
                sql, values = sql_statement.split("VALUES")
                values = values.strip()
                if not values.startswith("("):
                    values = "(" + values
                if not values.endswith(")"):
                    values = values + ")"
                placeholders = "[" + ", ".join([values] * len(sql_parameters)) + "]"
                concat_params_tuple = tuple([param for tup in sql_parameters_str for param in tup])
                formatted_sql = f"{sql} VALUES {placeholders}" % concat_params_tuple
            else:
                formatted_sql = sql_statement
                sql_parameters_str = "None"
            self.logger.info('database-mysql-local cursor.py executemany()', object={
                "formatted_sql": formatted_sql,
                "sql_parameters": sql_parameters_str,
                "sql_statement": sql_statement
            })
        except Exception as e:
            self.logger.warning('Unable to format parameters', object={
                "sql_statement": sql_statement,
                "sql_parameters": sql_parameters,
                "error": str(e)
            })

        self.cursor.executemany(sql_statement, sql_parameters)

    def fetchall(self) -> Any:
        return self.cursor.fetchall()

    def fetchone(self) -> Any:
        return self.cursor.fetchone()

    def description(self) -> Any:
        return self.cursor.description

    def lastrowid(self) -> int:
        return self.cursor.lastrowid

    def close(self) -> None:
        self.cursor.close()
