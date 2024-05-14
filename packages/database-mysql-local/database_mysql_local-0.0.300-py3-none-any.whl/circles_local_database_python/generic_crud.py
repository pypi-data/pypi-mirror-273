import os
import re
from datetime import datetime
from functools import lru_cache
from typing import Any
from typing import Optional

import mysql.connector
from database_infrastructure_local.number_generator import NumberGenerator
from logger_local.MetaLogger import MetaLogger
from user_context_remote.user_context import UserContext

from .connector import Connector
from .constants import DEFAULT_SQL_SELECT_LIMIT, LOGGER_CRUD_CODE_OBJECT
from .table_definition import table_definition
from .utils import (process_insert_data_dict, process_update_data_dict,
                    validate_none_select_table_name,
                    validate_select_table_name)


# TODO: this file is too big, can we break it down into smaller files?
class GenericCRUD(metaclass=MetaLogger, object=LOGGER_CRUD_CODE_OBJECT):
    """A class that provides generic CRUD functionality.
    There are 4 main functions to create, read, update, and delete data from the database.
    The rest of the functions are helper functions or wrappers around the main functions."""

    # TODO add default_select_clause_value and default_where in all functions not only in select_multi_tuple_by_where
    #   (no need to add to the the selects, as they all call select_multi_tuple_by_where)
    def __init__(self, *, default_schema_name: str,
                 default_table_name: str = None, default_view_table_name: str = None,
                 default_column_name: str = None, default_id_column_name: str = None,
                 default_select_clause_value: str = "*", default_where: str = None, is_test_data: bool = False) -> None:
        """Initializes the GenericCRUD class. If a connection is not provided, a new connection will be created."""
        self.default_schema_name = default_schema_name
        self.connection = Connector.connect(schema_name=default_schema_name)
        self.cursor = self.connection.cursor()
        self.default_column_name = self._deprecated_id_column(default_id_column_name, default_column_name)
        self.default_table_name = default_table_name
        self.default_view_table_name = default_view_table_name or self.generate_view_name(default_table_name)
        self.default_select_clause_value = default_select_clause_value
        self.default_where = default_where
        self.is_test_data = is_test_data or self.__detect_if_is_test_data()
        self.user_context = UserContext()

    def _data_json_to_dict(self, data_json: dict = None) -> dict:
        if data_json is not None:
            # We let the developers migrate quietly for a week
            if datetime.now() > datetime(2024, 5, 20):
                self.logger.warning(
                    "GenericCRUD: data_json is deprecated and scheduled to be removed by 12/06/2024, use data_dict instead. "
                    "In general, use _dict when the the typing is dict and _json when the typing is json / str.")

            return data_json

    def _deprecated_id_column(self, id_column_name: str, column_name: str) -> str:
        if id_column_name:
            # We let the developers migrate quietly for a week
            if datetime.now() > datetime(2024, 5, 20):
                self.logger.warning(
                    "GenericCRUD: id_column_name and id_column_value are deprecated and scheduled to be removed by 12/06/2024, use column_name and column_value instead.")
            return id_column_name
        return column_name

    def insert(self, *, schema_name: str = None, table_name: str = None, data_dict: dict = None, data_json: dict = None,
               ignore_duplicate: bool = False, commit_changes: bool = True) -> int:
        """Inserts a new row into the table and returns the id of the new row or -1 if an error occurred."""
        data_dict = data_json or self._data_json_to_dict(data_dict)
        if ignore_duplicate:
            # TODO Also display the data_dict
            self.logger.warning(f"GenericCRUD.insert({schema_name}.{table_name}) using ignore_duplicate, is it needed?",
                                object={"data_dict": data_dict})

        table_name = table_name or self.default_table_name
        schema_name = schema_name or self.default_schema_name
        self._validate_args(args=locals())

        # if table_name in table_definition:
        #     if table_definition[table_name]["is_number_column"]:
        #         view_name = self._get_view_name(table_name)
        #         number = NumberGenerator.get_random_number(schema_name=schema_name, view_name=view_name)
        #         data_dict["number"] = number
        # else:
        #     self.logger.warning(f"database-mysql-local-python generic_crud.py Table {table_name} not found in "
        #                         f"database-mysql-local.table_definition_table data structure, we might need to run sql2code")

        # TODO: In the future we may want to check this with table_definition
        #   and not with self.is_column_in_table for better performance
        data_dict = self.__add_create_updated_user_profile_ids(
            data_dict=data_dict, add_created_user_id=True, schema_name=schema_name, table_name=table_name)

        columns, values, data_dict = process_insert_data_dict(data_dict=data_dict)
        # We removed the IGNORE from the SQL Statement as we want to return the id of the existing row
        insert_query = "INSERT " + \
                       f"INTO `{schema_name}`.`{table_name}` ({columns}) " \
                       f"VALUES ({values});"
        # Log query without parameters
        values_str = ', '.join(f"'{value}'" for value in data_dict.values())
        insert_query_without_parameters = f"INSERT INTO `{schema_name}`.`{table_name}` ({columns}) VALUES ({values_str});"
        self.logger.info("GenericCRUD.insert",
                         object={"insert_query_without_parameters": insert_query_without_parameters})
        try:
            self.cursor.execute(insert_query, tuple(data_dict.values()))
            if commit_changes:
                self.connection.commit()
            inserted_id = self.cursor.lastrowid()
        except mysql.connector.errors.IntegrityError as exception:
            if ignore_duplicate:
                self.logger.warning("GenericCRUD.insert: existing record found, selecting it's id."
                                    f"(table_name={table_name}, data_dict={data_dict})")
                inserted_id = self._get_existing_duplicate_id(schema_name, table_name, exception)
            else:
                raise exception
        finally:
            self.logger.debug(object=locals())
        return inserted_id

    def upsert(self, *, schema_name: str = None, table_name: str = None, view_table_name: str = None,
               data_dict: dict = None, data_json: dict = None,
               data_dict_compare: dict = None, data_json_compare: dict = None,
               order_by: str = None, compare_with_or: bool = False) -> Optional[int]:
        """Inserts a new row into the table, or updates an existing row if a row with the
          same values as data_dict_compare exists,
          and returns the id of the new row or None if an error occurred."""
        data_dict = data_json or self._data_json_to_dict(data_dict)
        data_dict_compare = data_json_compare or self._data_json_to_dict(data_dict_compare)
        old_schema_name = self.default_schema_name
        schema_name = schema_name or self.default_schema_name
        table_name = table_name or self.default_table_name
        view_table_name = view_table_name or self.default_view_table_name
        column_name = self.generate_column_name(table_name)
        self._validate_args(args=locals())
        if not data_dict:
            self.logger.warning(log_message="GenericCRUD.upsert: data_dict is empty")
            return
        if not data_dict_compare:
            return self.insert(schema_name=schema_name, table_name=table_name, data_dict=data_dict)

        columns, values, processed_data_dict_compare = process_insert_data_dict(data_dict=data_dict_compare)
        where_clauses = []
        params = []
        for key, value in processed_data_dict_compare.items():
            if isinstance(value, list):
                where_clauses.append(f"({' OR '.join([f'{key}=%s' for _ in value])})")
                params.extend(value)
            else:
                where_clauses.append(f"{key}=%s")
                params.append(value)

        where_clause = " OR " if compare_with_or else " AND "
        where_clause = where_clause.join(where_clauses)

        old_cursor = self.cursor
        cursor = None
        try:
            cursor = self.connection.cursor()
            self.cursor = cursor
            table_id = self.select_one_value_by_where(
                schema_name=schema_name, view_table_name=view_table_name, select_clause_value=column_name,
                where=where_clause, params=tuple(params), order_by=order_by)
            if table_id:
                self.update_by_column_and_value(
                    schema_name=schema_name, table_name=table_name, column_name=column_name, column_value=table_id,
                    data_dict=data_dict, commit_changes=False)
            else:
                table_id = self.insert(schema_name=schema_name, table_name=table_name, data_dict=data_dict,
                                       commit_changes=False, ignore_duplicate=True)
            self.connection.commit()
        except Exception as exception:
            self.connection.rollback()
            raise exception
        finally:
            self.cursor = old_cursor
            self.default_schema_name = old_schema_name
            if cursor:
                cursor.close()
            self.logger.debug(object=locals())
        return table_id

    def _get_existing_duplicate_id(self, schema_name: str, table_name: str, error: Exception) -> int or None:
        """Error examples:
        - Duplicate entry 'test@gmail.com' for key 'email_address_table.email_address.unique'
        - Duplicate entry '1' for key 'test_mysql_table.PRIMARY'
        - Duplicate entry '7263200721327371865' for key 'test_mysql_table.number_UNIQUE"""
        pattern = r'Duplicate entry \'(.+?)\' for key \'(.+?)\''
        match = re.search(pattern, str(error))
        if not match:  # a different error
            raise error
        duplicate_value = match.group(1)
        duplicate_column_name = match.group(2).split('.')[1]
        if duplicate_column_name == "PRIMARY":
            return int(duplicate_value)
        if duplicate_column_name.endswith("_UNIQUE"):
            duplicate_column_name = duplicate_column_name.split('_')[0]

        query = """
        SELECT COLUMN_NAME
        FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
        WHERE TABLE_NAME = %s AND CONSTRAINT_NAME = "PRIMARY";
        """
        self.cursor.execute(query, (table_name,))
        column_name = (self.cursor.fetchone() or [None])[0]
        if not column_name:
            raise error  # Column name for constraint not found
        select_query = f"SELECT {column_name} FROM `{schema_name}`.`{table_name}` WHERE {duplicate_column_name} = %s LIMIT 1;"
        self.cursor.execute(select_query, (duplicate_value,))
        existing_duplicate_id = (self.cursor.fetchone() or [None])[0]
        self.logger.debug(object=locals())
        return existing_duplicate_id

    def update_by_id(
            self, *, schema_name: str = None, table_name: str = None, column_name: str = None, column_value: Any = None,
            id_column_name: str = None, id_column_value: Any = None, data_dict: dict = None, data_json: dict = None,
            limit: int = DEFAULT_SQL_SELECT_LIMIT, order_by: str = None, commit_changes: bool = True) -> None:
        if datetime.now() > datetime(2024, 5, 20):
            self.logger.warning("GenericCRUD.update_by_id is deprecated, use update_by_column_and_value instead.")
        return self.update_by_column_and_value(schema_name=schema_name, table_name=table_name,
                                          column_name=column_name, column_value=column_value,
                                          id_column_name=id_column_name, id_column_value=id_column_value,
                                          data_dict=data_dict, data_json=data_json,
                                          limit=limit, order_by=order_by, commit_changes=commit_changes)

    def update_by_column_and_value(
            self, *, schema_name: str = None, table_name: str = None, column_name: str = None, column_value: Any = None,
            id_column_name: str = None, id_column_value: Any = None, data_dict: dict = None, data_json: dict = None,
            limit: int = DEFAULT_SQL_SELECT_LIMIT, order_by: str = None, commit_changes: bool = True) -> None:
        """Updates data in the table by ID."""
        column_name = self._deprecated_id_column(id_column_name, column_name)
        column_value = column_value or id_column_value
        data_dict = data_json or self._data_json_to_dict(data_dict)
        table_name = table_name or self.default_table_name
        column_name = column_name or self.default_column_name

        if column_name:
            where, params = self.__get_where_params(column_name, column_value)
            self.update_by_where(schema_name=schema_name, table_name=table_name, where=where,
                                 data_dict=data_dict, params=params,
                                 limit=limit, order_by=order_by, commit_changes=commit_changes)
        else:
            raise Exception("Update by id requires an column_name")

    def update_by_where(self, *, schema_name: str = None, table_name: str = None, where: str = None,
                        params: tuple = None, data_dict: dict = None, data_json: dict = None,
                        limit: int = DEFAULT_SQL_SELECT_LIMIT, order_by: str = None,
                        commit_changes: bool = True) -> None:
        """Updates data in the table by WHERE.
        Example:
        "UPDATE table_name SET A=A_val, B=B_val WHERE C=C_val AND D=D_val"
        translates into:
        update_by_where(table_name="table_name",
                        data_dict={"A": A_val, "B": B_val},
                        where="C=%s AND D=%s",
                        params=(C_val, D_val)"""
        data_dict = data_json or self._data_json_to_dict(data_dict)
        table_name = table_name or self.default_table_name
        schema_name = schema_name or self.default_schema_name
        self._validate_args(args=locals())

        data_dict = self.__add_create_updated_user_profile_ids(data_dict=data_dict, add_created_user_id=False,
                                                               schema_name=schema_name, table_name=table_name)

        set_values, data_dict = process_update_data_dict(data_dict)
        if not where:
            raise Exception("update_by_where requires a 'where'")

        update_query = f"UPDATE `{schema_name}`.`{table_name}` " \
                       f"SET {set_values} updated_timestamp=CURRENT_TIMESTAMP() " \
                       f"WHERE {where} " + \
                       (f"ORDER BY {order_by} " if order_by else "") + \
                       f"LIMIT {limit};"
        params = params or tuple()
        self.cursor.execute(update_query, tuple(data_dict.values()) + params)
        if commit_changes:
            self.connection.commit()

    def delete_by_id(self, *, schema_name: str = None, table_name: str = None,
                     column_name: str = None, column_value: Any = None,
                     id_column_name: str = None, id_column_value: Any = None) -> None:
        if datetime.now() > datetime(2024, 5, 20):
            self.logger.warning("GenericCRUD.delete_by_id is deprecated, use delete_by_column_and_value instead.")
        return self.delete_by_column_and_value(schema_name=schema_name, table_name=table_name,
                                          column_name=column_name, column_value=column_value,
                                          id_column_name=id_column_name, id_column_value=id_column_value)

    def delete_by_column_and_value(self, *, schema_name: str = None, table_name: str = None,
                              column_name: str = None, column_value: Any = None,
                              id_column_name: str = None, id_column_value: Any = None) -> None:
        """Deletes data from the table by id"""
        # checks are done inside delete_by_where
        column_name = self._deprecated_id_column(id_column_name, column_name)
        column_value = column_value or id_column_value
        column_name = column_name or self.default_column_name
        if column_name:  # column_value can be empty
            where, params = self.__get_where_params(column_name, column_value)
            self.delete_by_where(schema_name=schema_name, table_name=table_name, where=where, params=params)
        else:
            raise Exception("Delete by id requires an column_name and column_value.")

    def delete_by_where(self, *, schema_name: str = None, table_name: str = None, where: str = None,
                        params: tuple = None) -> None:
        """Deletes data from the table by WHERE."""

        table_name = table_name or self.default_table_name
        schema_name = schema_name or self.default_schema_name
        self._validate_args(args=locals())
        if not where:
            raise Exception("delete_by_where requires a 'where'")

        update_query = f"UPDATE `{schema_name}`.`{table_name}` " \
                       f"SET end_timestamp=CURRENT_TIMESTAMP() " \
                       f"WHERE {where};"
        self.cursor.execute(update_query, params)
        self.connection.commit()

    # Main select function
    def select_multi_tuple_by_where(
            self, *, schema_name: str = None, view_table_name: str = None, select_clause_value: str = None,
            where: str = None, params: tuple = None, distinct: bool = False, limit: int = DEFAULT_SQL_SELECT_LIMIT,
            order_by: str = "") -> list:
        """Selects multiple rows from the table based on a WHERE clause and returns them as a list of tuples."""

        schema_name = schema_name or self.default_schema_name
        view_table_name = view_table_name or self.default_view_table_name
        select_clause_value = select_clause_value or self.default_select_clause_value
        where = where or self.default_where
        where = self.__where_security(where=where, view_name=view_table_name)
        self._validate_args(args=locals())

        # TODO: add ` to column names if they are not reserved words (like COUNT, ST_X(point), etc.)
        # select_clause_value = ",".join([f"`{x.strip()}`" for x in select_clause_value.split(",") if x != "*"])
        # TODO: If is_test_data exists in the table and is_test_data=False, add `AND is_test_data=0` to avoid users getting test data
        #   (but the tests should be allowed to access real data)
        select_query = f"SELECT {'DISTINCT' if distinct else ''} {select_clause_value} " \
                       f"FROM `{schema_name}`.`{view_table_name}` " + \
                       (f"WHERE {where} " if where else "") + \
                       (f"ORDER BY {order_by} " if order_by else "") + \
                       f"LIMIT {limit};"
        self.cursor.execute(select_query, params)
        result = self.cursor.fetchall()
        self.logger.debug(object=locals())
        return result

    def select_multi_dict_by_where(
            self, *, schema_name: str = None, view_table_name: str = None, select_clause_value: str = None,
            where: str = None, params: tuple = None, distinct: bool = False,
            limit: int = DEFAULT_SQL_SELECT_LIMIT, order_by: str = None) -> list:
        """Selects multiple rows from the table based on a WHERE clause and returns them as a list of dictionaries."""
        result = self.select_multi_tuple_by_where(
            schema_name=schema_name, view_table_name=view_table_name, select_clause_value=select_clause_value,
            where=where, params=params, distinct=distinct, limit=limit, order_by=order_by)
        return self.convert_multi_to_dict(result, select_clause_value)

    # TODO: test distinct
    def select_one_tuple_by_id(self, *, schema_name: str = None, view_table_name: str = None,
                               select_clause_value: str = None,
                               column_name: str = None, column_value: Any = None,
                               id_column_name: str = None, id_column_value: Any = None,
                               distinct: bool = False, order_by: str = "") -> tuple:
        if datetime.now() > datetime(2024, 5, 20):
            self.logger.warning(
                "GenericCRUD.select_one_tuple_by_id is deprecated, use select_one_tuple_by_column_and_value instead.")
        return self.select_one_tuple_by_column_and_value(
            schema_name=schema_name, view_table_name=view_table_name, select_clause_value=select_clause_value,
            column_name=column_name, column_value=column_value, id_column_name=id_column_name,
            id_column_value=id_column_value, distinct=distinct, order_by=order_by)

    def select_one_tuple_by_column_and_value(
            self, *, schema_name: str = None, view_table_name: str = None, select_clause_value: str = None,
            column_name: str = None, column_value: Any = None, id_column_name: str = None, id_column_value: Any = None,
            distinct: bool = False, order_by: str = "") -> tuple:
        """Selects one row from the table by ID and returns it as a tuple."""
        column_name = column_name or id_column_name
        column_value = column_value or id_column_value
        result = self.select_multi_tuple_by_column_and_value(
            schema_name=schema_name, view_table_name=view_table_name, select_clause_value=select_clause_value,
            column_name=column_name, column_value=column_value, distinct=distinct, limit=1, order_by=order_by)
        if result:
            return result[0]
        else:
            return tuple()  # or None?

    def select_one_dict_by_id(
            self, *, schema_name: str = None, view_table_name: str = None, select_clause_value: str = None,
            column_name: str = None, column_value: Any = None, id_column_name: str = None, id_column_value: Any = None,
            distinct: bool = False, order_by: str = "") -> dict:
        if datetime.now() > datetime(2024, 5, 20):
            self.logger.warning(
                "GenericCRUD.select_one_dict_by_id is deprecated, use select_one_dict_by_column_and_value instead.")
        return self.select_one_dict_by_column_and_value(
            schema_name=schema_name, view_table_name=view_table_name, select_clause_value=select_clause_value,
            column_name=column_name, column_value=column_value, id_column_name=id_column_name,
            id_column_value=id_column_value, distinct=distinct, order_by=order_by)

    def select_one_dict_by_column_and_value(
            self, *, schema_name: str = None, view_table_name: str = None, select_clause_value: str = None,
            column_name: str = None, column_value: Any = None, id_column_name: str = None, id_column_value: Any = None,
            distinct: bool = False, order_by: str = "") -> dict:
        """Selects one row from the table by ID and returns it as a dictionary (column_name: value)"""
        column_name = column_name or id_column_name
        column_value = column_value or id_column_value
        result = self.select_one_tuple_by_column_and_value(
            schema_name=schema_name, view_table_name=view_table_name, select_clause_value=select_clause_value,
            column_name=column_name, column_value=column_value, distinct=distinct, order_by=order_by)
        return self.convert_to_dict(result, select_clause_value)

    def __validate_single_clause_value(self, select_clause_value: str = None) -> None:
        select_clause_value = select_clause_value or self.default_select_clause_value
        if "," in select_clause_value or select_clause_value == "*":
            raise ValueError("select value requires a single column name")

    def select_one_value_by_id(
            self, *, select_clause_value: str, schema_name: str = None, view_table_name: str = None,
            column_name: str = None, column_value: Any = None, id_column_name: str = None, id_column_value: Any = None,
            distinct: bool = False, order_by: str = "", skip_null_values: bool = True) -> Any:
        if datetime.now() > datetime(2024, 5, 20):
            self.logger.warning(
                "GenericCRUD.select_one_value_by_id is deprecated, use select_one_value_by_column_and_value instead.")
        return self.select_one_value_by_column_and_value(
            select_clause_value=select_clause_value, schema_name=schema_name, view_table_name=view_table_name,
            column_name=column_name, column_value=column_value, id_column_name=id_column_name,
            id_column_value=id_column_value, distinct=distinct, order_by=order_by, skip_null_values=skip_null_values)

    def select_one_value_by_column_and_value(
            self, *, select_clause_value: str, schema_name: str = None, view_table_name: str = None,
            column_name: str = None, column_value: Any = None, id_column_name: str = None, id_column_value: Any = None,
            distinct: bool = False, order_by: str = "", skip_null_values: bool = True) -> Any:
        """Selects one value from the table by ID and returns it."""
        column_name = column_name or id_column_name
        column_value = column_value or id_column_value
        column_name = column_name or id_column_name
        column_value = column_value or id_column_value
        self.__validate_single_clause_value(select_clause_value)
        where, params = self.__get_where_params(column_name, column_value)
        where = self.__where_skip_null_values(where, select_clause_value, skip_null_values)
        result = self.select_one_tuple_by_where(
            schema_name=schema_name, view_table_name=view_table_name, select_clause_value=select_clause_value,
            where=where, params=params, distinct=distinct, order_by=order_by)
        if result:  # TODO: the caller can't tell if not found, or found null
            return result[0]

    def select_one_tuple_by_where(
            self, *, schema_name: str = None, view_table_name: str = None, select_clause_value: str = None,
            where: str = None, params: tuple = None, distinct: bool = False, order_by: str = "") -> tuple:
        """Selects one row from the table based on a WHERE clause and returns it as a tuple."""
        result = self.select_multi_tuple_by_where(
            schema_name=schema_name, view_table_name=view_table_name, select_clause_value=select_clause_value,
            where=where, params=params, distinct=distinct, limit=1, order_by=order_by)
        if result:
            return result[0]
        else:
            return tuple()

    def select_one_dict_by_where(
            self, *, schema_name: str = None, view_table_name: str = None, select_clause_value: str = None,
            where: str = None, params: tuple = None, distinct: bool = False, order_by: str = "") -> dict:
        """Selects one row from the table based on a WHERE clause and returns it as a dictionary."""
        result = self.select_one_tuple_by_where(
            schema_name=schema_name, view_table_name=view_table_name, select_clause_value=select_clause_value,
            where=where, params=params, distinct=distinct, order_by=order_by)
        return self.convert_to_dict(result, select_clause_value)

    def select_one_value_by_where(
            self, *, select_clause_value: str, schema_name: str = None, view_table_name: str = None,
            where: str = None, params: tuple = None, distinct: bool = False, order_by: str = "",
            skip_null_values: bool = True) -> Any:
        """Selects one value from the table based on a WHERE clause and returns it."""
        self.__validate_single_clause_value(select_clause_value)
        where = self.__where_skip_null_values(where, select_clause_value, skip_null_values)
        result = self.select_one_tuple_by_where(
            schema_name=schema_name, view_table_name=view_table_name, select_clause_value=select_clause_value,
            where=where, params=params, distinct=distinct, order_by=order_by)
        if result:
            return result[0]

    def select_multi_value_by_id(
            self, *, schema_name: str = None, view_table_name: str = None, select_clause_value: str = None,
            column_name: str = None, column_value: Any = None, id_column_name: str = None, id_column_value: Any = None,
            distinct: bool = False, limit: int = DEFAULT_SQL_SELECT_LIMIT, order_by: str = "",
            skip_null_values: bool = True) -> list:
        if datetime.now() > datetime(2024, 5, 20):
            self.logger.warning(
                "GenericCRUD.select_multi_value_by_id is deprecated, use select_multi_value_by_column_and_value instead.")
        return self.select_multi_value_by_column_and_value(
            schema_name=schema_name, view_table_name=view_table_name, select_clause_value=select_clause_value,
            column_name=column_name, column_value=column_value, id_column_name=id_column_name,
            id_column_value=id_column_value, distinct=distinct, limit=limit, order_by=order_by,
            skip_null_values=skip_null_values)


    def select_multi_value_by_column_and_value(
            self, *, schema_name: str = None, view_table_name: str = None, select_clause_value: str = None,
            column_name: str = None, column_value: Any = None, id_column_name: str = None, id_column_value: Any = None,
            distinct: bool = False, limit: int = DEFAULT_SQL_SELECT_LIMIT, order_by: str = "",
            skip_null_values: bool = True) -> list:
        """Selects multiple values from the table by ID and returns them as a list."""
        column_name = column_name or id_column_name
        column_value = column_value or id_column_value
        self.__validate_single_clause_value(select_clause_value)
        where, params = self.__get_where_params(column_name, column_value)
        where = self.__where_skip_null_values(where, select_clause_value, skip_null_values)
        result = self.select_multi_tuple_by_where(
            schema_name=schema_name, view_table_name=view_table_name, select_clause_value=select_clause_value,
            where=where, params=params, distinct=distinct, limit=limit, order_by=order_by)
        return [row[0] for row in result]

    def select_multi_value_by_where(
            self, *, schema_name: str = None, view_table_name: str = None, select_clause_value: str = None,
            where: str = None, params: tuple = None, distinct: bool = False, limit: int = DEFAULT_SQL_SELECT_LIMIT,
            order_by: str = "", skip_null_values: bool = True) -> list:
        self.__validate_single_clause_value(select_clause_value)
        where = self.__where_skip_null_values(where, select_clause_value, skip_null_values)
        result = self.select_multi_tuple_by_where(
            schema_name=schema_name, view_table_name=view_table_name, select_clause_value=select_clause_value,
            where=where, params=params, distinct=distinct, limit=limit, order_by=order_by)
        return [row[0] for row in result]

    def select_multi_tuple_by_id(
            self, *, schema_name: str = None, view_table_name: str = None, select_clause_value: str = None,
            column_name: str = None, column_value: Any = None, id_column_name: str = None, id_column_value: Any = None,
            distinct: bool = False, limit: int = DEFAULT_SQL_SELECT_LIMIT, order_by: str = None) -> list:
        if datetime.now() > datetime(2024, 5, 20):
            self.logger.warning(
                "GenericCRUD.select_multi_tuple_by_id is deprecated, use select_multi_tuple_by_column_and_value instead.")
        return self.select_multi_tuple_by_column_and_value(
            schema_name=schema_name, view_table_name=view_table_name, select_clause_value=select_clause_value,
            column_name=column_name, column_value=column_value, id_column_name=id_column_name,
            id_column_value=id_column_value, distinct=distinct, limit=limit, order_by=order_by)

    def select_multi_tuple_by_column_and_value(
            self, *, schema_name: str = None, view_table_name: str = None, select_clause_value: str = None,
            column_name: str = None, column_value: Any = None, id_column_name: str = None, id_column_value: Any = None,
            distinct: bool = False, limit: int = DEFAULT_SQL_SELECT_LIMIT, order_by: str = None) -> list:
        """Selects multiple rows from the table by ID and returns them as a
        list of tuples.
        send `column_name=''` if you want to select all rows and ignore default column"""
        column_name = self._deprecated_id_column(id_column_name, column_name)
        column_value = column_value or id_column_value
        column_name = column_name or self.default_column_name

        if not column_name:
            where = None
            params = None
        else:
            if column_value is None:
                where = f"`{column_name}` IS NULL"
                params = None
            else:
                where = f"`{column_name}`=%s"
                params = (column_value,)
        return self.select_multi_tuple_by_where(
            schema_name=schema_name, view_table_name=view_table_name, select_clause_value=select_clause_value,
            where=where, params=params, distinct=distinct, limit=limit, order_by=order_by)

    def select_multi_dict_by_id(
            self, *, schema_name: str = None, view_table_name: str = None, select_clause_value: str = None,
            column_name: str = None, column_value: Any = None, id_column_name: str = None, id_column_value: Any = None,
            distinct: bool = False, limit: int = DEFAULT_SQL_SELECT_LIMIT, order_by: str = None) -> list:
        if datetime.now() > datetime(2024, 5, 20):
            self.logger.warning(
                "GenericCRUD.select_multi_dict_by_id is deprecated, use select_multi_dict_by_column_and_value instead.")
        return self.select_multi_dict_by_column_and_value(
            schema_name=schema_name, view_table_name=view_table_name, select_clause_value=select_clause_value,
            column_name=column_name, column_value=column_value, id_column_name=id_column_name,
            id_column_value=id_column_value, distinct=distinct, limit=limit, order_by=order_by)

    def select_multi_dict_by_column_and_value(
            self, *, schema_name: str = None, view_table_name: str = None, select_clause_value: str = None,
            column_name: str = None, column_value: Any = None, id_column_name: str = None, id_column_value: Any = None,
            distinct: bool = False, limit: int = DEFAULT_SQL_SELECT_LIMIT, order_by: str = None) -> list:
        """Selects multiple rows from the table by ID and returns them as a list of dictionaries."""
        column_name = column_name or id_column_name
        column_value = column_value or id_column_value
        result = self.select_multi_tuple_by_column_and_value(
            schema_name=schema_name, view_table_name=view_table_name, select_clause_value=select_clause_value,
            column_name=column_name, column_value=column_value, distinct=distinct, limit=limit, order_by=order_by)
        return self.convert_multi_to_dict(result, select_clause_value)

    def is_column_in_table(self, column_name: str, schema_name: str = None, table_name: str = None) -> bool:
        schema_name = schema_name or self.default_schema_name
        table_name = table_name or self.default_table_name
        if not column_name:
            raise Exception("is_column_in_table requires a column_name")
        columns = self.get_columns_dict(schema_name=schema_name, table_name=table_name)
        is_column_in_table_result = (column_name in columns)
        self.logger.debug(object=locals())
        return is_column_in_table_result

    # TODO: use table_definition_table to improve performance
    # TODO: replace with redis in the future with table_definition_table
    @lru_cache
    def get_columns_dict(self, schema_name: str = None, table_name: str = None) -> dict:
        schema_name = schema_name or self.default_schema_name
        table_name = table_name or self.default_table_name
        select_query = "SELECT column_name " \
                       "FROM information_schema.columns " \
                       "WHERE TABLE_SCHEMA = %s " \
                       "AND TABLE_NAME = %s;"
        params = (schema_name, table_name)
        self.cursor.execute(select_query, params)
        result = self.cursor.fetchall()
        columns_dict = {row[0]: None for row in result}
        self.logger.debug(object=locals())
        return columns_dict

    # helper functions:
    def convert_to_dict(self, row: tuple, select_clause_value: str = None) -> dict:
        """Returns a dictionary of the column names and their values."""
        select_clause_value = select_clause_value or self.default_select_clause_value
        if select_clause_value == "*":
            column_names = [col[0] for col in self.cursor.description()]
        else:
            column_names = [x.strip() for x in select_clause_value.split(",")]
        dict_result = dict(zip(column_names, row or tuple()))
        self.logger.debug(object=locals())
        return dict_result

    def convert_multi_to_dict(self, rows: list[tuple], select_clause_value: str = None) -> list[dict]:
        """Converts multiple rows to dictionaries."""
        multiple_dict_result = [self.convert_to_dict(row, select_clause_value) for row in rows]
        self.logger.debug(object=locals())
        return multiple_dict_result

    def _validate_args(self, args: dict) -> None:
        # args = locals() of the calling function
        required_args = ("table_name", "view_table_name", "schema_name", "select_clause_value")  # TODO: , "data_dict")
        for arg_name, arg_value in args.items():
            message = ""
            if arg_name in ("self", "__class__"):
                continue
            elif arg_name in required_args and not arg_value:
                message = f"Invalid value for {arg_name}: {arg_value}"
            elif arg_name == "table_name":
                validate_none_select_table_name(arg_value)
            elif arg_name == "view_table_name":
                validate_select_table_name(arg_value, is_test_data=self.is_test_data)

            # data_dict values are allowed to contain ';', as we use them with %s (TODO: unless it's ToSQLInterface)
            if ((arg_name.startswith("data_") and arg_value and any(
                    ";" in str(x) for x in arg_value.keys())) or  # check columns
                    (not arg_name.startswith("data_") and arg_name != "params" and ";" in str(arg_value))):
                message = f"Invalid value for {arg_name}: {arg_value} (contains ';')"

            if message:
                raise Exception(message)

    @staticmethod
    def __detect_if_is_test_data() -> bool:
        """Check if running from a Unit Test file."""
        import inspect
        possible_current_files = [os.path.basename(frame.filename) for frame in inspect.stack()]

        for file_name in possible_current_files:
            if file_name.startswith('test_') or file_name.endswith('_test.py') or "pytest" in file_name:
                return True
        return False

    @staticmethod
    def __get_entity_type_by_table_name(table_name: str) -> int or None:
        """Returns the entity_type_id of the table."""
        if table_name in table_definition:
            entity_type_id = table_definition[table_name].get("entity_type_id1")
            return entity_type_id

    def __add_identifier(self, data_dict: dict, table_name: str) -> None:
        # If there's an "identifier" column in the table, we want to insert a random identifier
        #  to the identifier_table and use it in the data_dict.
        identifier_entity_type_id = self.__get_entity_type_by_table_name(table_name)
        if not identifier_entity_type_id:
            return
            # TODO Please add maximum infomation to any exception i.e. table_name, data_dict ...
            # raise Exception("Could not find the entity_type_id1 for table " + table_name + " in database.table_definition_table")

        identifier = NumberGenerator.get_random_identifier(schema_name="identifier",
                                                           view_name="identifier_view",
                                                           identifier_column_name="identifier")
        data_dict["identifier"] = identifier
        # TODO: use self.insert
        insert_query = "INSERT " + \
                       "INTO `identifier`.`identifier_table` (identifier, entity_type_id) " \
                       "VALUES (%s, %s);"
        self.cursor.execute(insert_query, (identifier, identifier_entity_type_id))
        self.connection.commit()

    # TODO: add warning logs
    def __add_create_updated_user_profile_ids(self, data_dict: dict, add_created_user_id: bool = False,
                                              schema_name: str = None, table_name: str = None) -> dict:
        """Adds created_user_id and updated_user_id to data_dict."""
        # if get_environment_name() not in (EnvironmentName.DVLP1.value, EnvironmentName.PROD1.value):
        # TODO data_dict = data_dict.copy() ?
        schema_name = schema_name or self.default_schema_name
        table_name = table_name or self.default_table_name
        columns_dict = self.get_columns_dict(schema_name=schema_name, table_name=table_name)
        if add_created_user_id:
            if "created_user_id" in columns_dict:
                data_dict["created_user_id"] = self.user_context.get_effective_user_id()
            else:
                self.__log_warning("created_user_id", schema_name, table_name)
            if "created_real_user_id" in columns_dict:
                data_dict["created_real_user_id"] = self.user_context.get_real_user_id()
            else:
                self.__log_warning("created_real_user_id", schema_name, table_name)
            if "created_effective_user_id" in columns_dict:
                data_dict["created_effective_user_id"] = self.user_context.get_effective_user_id()
            else:
                self.__log_warning("created_effective_user_id", schema_name, table_name)
            if "created_effective_profile_id" in columns_dict:
                data_dict["created_effective_profile_id"] = self.user_context.get_effective_profile_id()
            else:
                self.__log_warning("created_effective_profile_id", schema_name, table_name)
            if "number" in columns_dict:
                # TODO: the commented line caused errors, we need to check it
                # view_name = self.default_view_table_name or self._get_view_name(table_name)
                view_name = table_name
                number = NumberGenerator.get_random_number(schema_name=schema_name, view_name=view_name)
                data_dict["number"] = number
            else:
                self.__log_warning("number", schema_name, table_name)

            if "identifier" in columns_dict:
                self.__add_identifier(data_dict=data_dict, table_name=table_name)
            else:
                self.__log_warning("identifier", schema_name, table_name)
        if "updated_user_id" in columns_dict:
            data_dict["updated_user_id"] = self.user_context.get_effective_user_id()
        else:
            self.__log_warning("updated_user_id", schema_name, table_name)
        if "updated_real_user_id" in columns_dict:
            data_dict["updated_real_user_id"] = self.user_context.get_real_user_id()
        else:
            self.__log_warning("updated_real_user_id", schema_name, table_name)
        if "updated_effective_user_id" in columns_dict:
            data_dict["updated_effective_user_id"] = self.user_context.get_effective_user_id()
        else:
            self.__log_warning("updated_effective_user_id", schema_name, table_name)
        if "updated_effective_profile_id" in columns_dict:
            data_dict["updated_effective_profile_id"] = self.user_context.get_effective_profile_id()
        else:
            self.__log_warning("updated_effective_profile_id", schema_name, table_name)
        # TODO: later we may want to add a check for the table_definition to see if there is a column for is_test_data
        if "is_test_data" in columns_dict:
            data_dict["is_test_data"] = self.is_test_data
        else:
            self.__log_warning("is_test_data", schema_name, table_name)
        # else:
        #     schema_name = schema_name or self.schema_name
        #     table_name = table_name or self.default_table_name
        #     if add_created_user_id:
        #         data_dict["created_user_id"] = self.user_context.get_effective_user_id()
        #         data_dict["created_real_user_id"] = self.user_context.get_real_user_id()
        #         data_dict["created_effective_user_id"] = self.user_context.get_effective_user_id()
        #         data_dict["created_effective_profile_id"] = self.user_context.get_effective_profile_id()
        #         # TODO: the commented line caused errors, we need to check it
        #         # view_name = self._get_view_name(table_name)
        #         view_name = table_name
        #         number = NumberGenerator.get_random_number(schema_name=schema_name, view_name=view_name)
        #         data_dict["number"] = number
        #
        #         # self.__add_identifier(data_dict=data_dict)
        #     data_dict["updated_user_id"] = self.user_context.get_effective_user_id()
        #     data_dict["updated_real_user_id"] = self.user_context.get_real_user_id()
        #     data_dict["updated_effective_user_id"] = self.user_context.get_effective_user_id()
        #     data_dict["updated_effective_profile_id"] = self.user_context.get_effective_profile_id()
        #     data_dict["is_test_data"] = self.is_test_data
        self.logger.debug(object=locals())
        return data_dict

    def __log_warning(self, column_name: str, schema_name: str, table_name: str):
        """Generates a warning log message and logs it."""
        log_message = f"{column_name} not found in {schema_name}.{table_name}"
        self.logger.warning(log_message)

    def __where_security(self, where: str, view_name: str) -> str:
        """Adds security to the where clause."""
        '''
        if self.is_column_in_table(column_name="visibility_id", schema_name=self.schema_name, table_name=view_name):
            effective_profile_id = self.user_context.get_effective_profile_id()
            where_security = f"(visibility_id > 1 OR created_effective_profile_id = {effective_profile_id})"
            if not (where == "" or where is None):
                where_security += f" AND ({where})"
            return where_security
        '''
        if view_name in table_definition:
            if table_definition[view_name].get("is_visibility"):
                effective_profile_id = self.user_context.get_effective_profile_id()
                where_security = f"(visibility_id > 1 OR created_effective_profile_id = {effective_profile_id})"
                if where:
                    where_security += f" AND ({where})"
                return where_security
        return where

    def set_schema(self, schema_name: Optional[str]):
        """Sets the given schema to be the default schema.
        In most cases you do not have to call this directly - you can pass schema_name to most functions"""
        if schema_name and self.default_schema_name != schema_name:
            self.connection.set_schema(schema_name)
            self.default_schema_name = schema_name

    def close(self) -> None:
        """Closes the connection to the database (we usually do not have to call this)"""
        self.connection.close()

    def _log_error_message(self, message: str, sql_statement: str, schema_name: str) -> str:
        return (f"{message} - SQL statement: {sql_statement}. "
                f"(user={self.connection.user}, host={self.connection.host}, schema={schema_name})")

    @staticmethod
    def generate_view_name(table_name: Optional[str]) -> Optional[str]:
        if table_name:
            return re.sub(r'(_table)$', '_view', table_name)

    @staticmethod
    def generate_column_name(table_name: Optional[str]) -> Optional[str]:
        if table_name:
            return re.sub(r'(_table)$', '_id', table_name)

    def get_test_entity_id(self, *, entity_name: str, insert_function: callable, insert_kwargs: dict = None,
                           entity_creator: callable = None, create_kwargs: dict = None,
                           schema_name: str = None, view_name: str = None) -> int:
        """
        1. Check if there's an entity with is `is_test_data=True`.
        2. If there is, return its id.
        3. If not, create a new entity with `is_test_data=True` and return its id.
        (assuming entity_creator expects `is_test_data` as parameters,
            and returns the expected argument for insert_function)

        Example: get_test_entity_id(entity_name='person', entity_creator=Person, insert_function=PersonsLocal.insert)
        """
        view_name = view_name or self.default_view_table_name
        select_clause_value = entity_name + "_id"
        fetched_result = self.select_one_dict_by_id(
            schema_name=schema_name or self.default_schema_name, view_table_name=view_name,
            column_name='is_test_data', column_value='1', select_clause_value=select_clause_value)
        if fetched_result:
            test_entity_id = fetched_result[select_clause_value]
        else:
            insert_kwargs = insert_kwargs or {}
            create_kwargs = create_kwargs or {}
            # is_test_data from the constructor should be used in the sons to avoid duplications
            if entity_creator:
                entity_result = entity_creator(**create_kwargs)
                test_entity_id = insert_function(entity_result, **insert_kwargs)
            else:
                test_entity_id = insert_function(**insert_kwargs)
        self.logger.debug(object=locals())
        return test_entity_id

    def __get_where_params(self, column_name: str, column_value: Any) -> tuple:
        column_name = column_name or self.default_column_name
        if column_value:
            where = f"`{column_name}`=%s"
            params = (column_value,)
        else:
            where = f"`{column_name}` IS NULL"
            params = None
        return where, params

    def __where_skip_null_values(self, where: str or None, select_clause_value: str, skip_null_values: bool = False) -> str:
        select_clause_value = select_clause_value or self.default_select_clause_value
        if skip_null_values:
            self.__validate_single_clause_value(select_clause_value)
            where_skip = f"`{select_clause_value}` IS NOT NULL"
            if where:
                where += f" AND {where_skip}"
            else:
                where = where_skip
        return where
