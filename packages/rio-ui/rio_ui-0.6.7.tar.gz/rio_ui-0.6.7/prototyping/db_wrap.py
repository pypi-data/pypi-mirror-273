from __future__ import annotations

import sys
import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import *  # type: ignore

import duckdb
from typing_extensions import dataclass_transform

T = TypeVar("T")
M = TypeVar("M", bound="DbModel")


def _escape_duckdb_column_name(value: str) -> str:
    assert isinstance(value, str), value

    # Allow the remaining code to assume the value isn't empty
    if not value:
        return '""'

    # Python's `repr` escapes the string in a similar fashion to what's needed
    # by DuckDB. Just touch it up a bit.
    escaped = repr(value)

    # Quick check to ensure the string didn't end up with triple quotes or
    # something silly. This is safe, only because the value cannot be "" at this
    # point.
    assert escaped[0] in ('"', "'"), escaped
    assert escaped[1] != escaped[0], escaped

    # Deal with quotes
    if escaped[0] == "'":
        escaped = escaped[1:-1].replace("\\'", "'")
    else:
        escaped = escaped[1:-1].replace('\\"', '""')

    # Done
    return f'"{escaped}"'


def _escape_duckdb_string(value: str) -> str:
    assert isinstance(value, str), value

    # Allow the remaining code to assume the value isn't empty
    if not value:
        return "''"

    # Python's `repr` escapes the string in a similar fashion to what's needed
    # by DuckDB. Just touch it up a bit.
    escaped = repr(value)

    # Quick check to ensure the string didn't end up with triple quotes or
    # something silly. This is safe, only because the value cannot be "" at this
    # point.
    assert escaped[0] in ('"', "'"), escaped
    assert escaped[1] != escaped[0], escaped

    # Deal with quotes
    if escaped[0] == "'":
        escaped = escaped[1:-1].replace("\\'", "''")
    else:
        escaped = escaped[1:-1].replace('\\"', '"')

    # Done
    return f"E'{escaped}'"


def _value_as_duckdb(value: Any) -> str:
    """
    Given a Python value, return the SQL representation of it.
    """
    # None
    if value is None:
        return "NULL"

    # Directly passed-through valuess: bool, int, float
    if isinstance(value, (bool, int, float)):
        return repr(value)

    # Strings
    if isinstance(value, str):
        return _escape_duckdb_string(value)

    # UUIDs
    if isinstance(value, uuid.UUID):
        return f"'{value}'"

    # Unsupported types
    raise NotImplementedError(f"Unsupported type: {type(value)}")


def _type_as_duckdb(type: Type) -> str:
    """
    Given a Python type, return the SQL representation of it.
    """
    # Directly passed-through types
    if type in (bool, int, float):
        return type.__name__

    # Strings
    if type is str:
        return "TEXT"

    # UUIDs
    if type is uuid.UUID:
        return "UUID"

    # Unsupported types
    raise NotImplementedError(f"Unsupported type: {type}")


class Filter(ABC):
    def __and__(self, other: Filter) -> Filter:
        subfilters = []

        if isinstance(self, AndFilter):
            subfilters.extend(self.filters)
        else:
            subfilters.append(self)

        if isinstance(other, AndFilter):
            subfilters.extend(other.filters)
        else:
            subfilters.append(other)

        return AndFilter(subfilters)

    def __or__(self, other: Filter) -> Filter:
        subfilters = []

        if isinstance(self, OrFilter):
            subfilters.extend(self.filters)
        else:
            subfilters.append(self)

        if isinstance(other, OrFilter):
            subfilters.extend(other.filters)
        else:
            subfilters.append(other)

        return OrFilter(subfilters)

    def __invert__(self) -> Filter:
        return NotFilter(self)

    @abstractmethod
    def _as_sql_filter(self) -> str:
        raise NotImplementedError


@dataclass
class Unfilter(Filter):
    """
    A filter matching any object.
    """

    def _as_sql_filter(self) -> str:
        return "(1=1)"


@dataclass(frozen=True)
class FieldFilter(Filter):
    field: DbField
    operator: Literal["==", "!=", ">", "<", ">=", "<="]
    value: Any

    def _as_sql_filter(self) -> str:
        return f"({self.field.sql_escape()} {self.operator} {self.value})"


@dataclass(frozen=True)
class AndFilter(Filter):
    filters: list[Filter]

    def _as_sql_filter(self) -> str:
        return (
            "(" + " AND ".join(f._as_sql_filter() for f in self.filters) + ")"
        )


@dataclass(frozen=True)
class OrFilter(Filter):
    filters: list[Filter]

    def _as_sql_filter(self) -> str:
        return "(" + " OR ".join(f._as_sql_filter() for f in self.filters) + ")"


@dataclass(frozen=True)
class NotFilter(Filter):
    filter: Filter

    def _as_sql_filter(self) -> str:
        return f"(NOT {self.filter._as_sql_filter()})"


@dataclass(frozen=True)
class FieldSort:
    _field: DbField
    _sort_ascending: bool

    def ascending(self) -> FieldSort:
        return FieldSort(self._field, True)

    def descending(self) -> FieldSort:
        return FieldSort(self._field, False)

    def reversed(self) -> FieldSort:
        return FieldSort(self._field, not self.ascending)


class DbField:
    def __init__(self, name: str, type: type, default: Any = None):
        self.name = name
        self.type = type
        self.default = default

    def __get__(
        self,
        instance: DbModel | None,
        owner: type | None = None,
    ) -> object:
        # If accessed through the class, rather than instance, return the
        # field itself
        if instance is None:
            return self

        # Otherwise get the value assigned to the property in the model
        # instance
        try:
            return vars(instance)[self.name]
        except KeyError:
            raise AttributeError(self.name) from None

    def __set__(self, instance: DbModel, value: object) -> None:
        vars(instance)[self.name] = value

    def __eq__(self, value: Any) -> FieldFilter:
        return FieldFilter(self, "==", value)

    def __ne__(self, value: Any) -> FieldFilter:
        return FieldFilter(self, "!=", value)

    def __gt__(self, value: Any) -> FieldFilter:
        return FieldFilter(self, ">", value)

    def __lt__(self, value: Any) -> FieldFilter:
        return FieldFilter(self, "<", value)

    def __ge__(self, value: Any) -> FieldFilter:
        return FieldFilter(self, ">=", value)

    def __le__(self, value: Any) -> FieldFilter:
        return FieldFilter(self, "<=", value)

    def sql_escape(self) -> str:
        return _escape_duckdb_column_name(self.name)

    def ascending(self) -> FieldSort:
        return FieldSort(self, True)

    def descending(self) -> FieldSort:
        return FieldSort(self, False)

    def reversed(self) -> FieldSort:
        return FieldSort(self, not self.ascending)


@dataclass_transform()
@dataclass
class DbModel:
    _db_fields_: ClassVar[dict[str, DbField]] = {
        "id": DbField("id", uuid.UUID),
    }

    id: uuid.UUID = field(default_factory=uuid.uuid4)

    def __init_subclass__(cls) -> None:
        # Apply the dataclass transformation
        dataclass(cls)

        # Fetch all inherited fields
        all_parent_fields: dict[str, DbField] = {}

        for base in reversed(cls.__bases__):
            if issubclass(base, DbModel):
                all_parent_fields.update(base._db_fields_)

        cls._db_fields_ = all_parent_fields

        # Add the fields from the class itself
        annotations: dict = vars(cls).get("__annotations__", {})
        module = sys.modules[cls.__module__]

        for field_name, field in class_local_fields(cls).items():
            # Add the field to the class
            field = DbField(field_name, annotations[field_name], module)
            setattr(cls, field_name, field)

            # Add it to the set of all fields for rapid lookup
            cls._db_fields_[field_name] = field

    def __init__(self, id: uuid.UUID | None) -> None:
        if id is None:
            self.id = uuid.uuid4()
        else:
            self.id = id


def _table_name_from_type(type: Type[M]) -> str:
    return f"instances__{type.__name__}"


class SyncAccessor:
    def __init__(
        self,
        db: duckdb.DuckDBPyConnection,
    ):
        self.db = db

    def _run_query_with_table(
        self,
        type: Type[M],
        query: str,
    ) -> duckdb.DuckDBPyConnection:
        """
        Runs the given query, ensuring that the target table exists.
        """
        # Try to run the query
        try:
            return self.db.execute(query)
        except duckdb.CatalogException:
            pass

        # Create the table
        field_name_strings: list[str] = []

        for field in type._db_fields_.values():
            field_name = _escape_duckdb_column_name(field.name)
            field_type = _type_as_duckdb(field.type)
            field_name_strings.append(f"{field_name} {field_type}")

        creation_query = f"CREATE TABLE {_table_name_from_type(type)} ({', '.join(field_name_strings)})"
        self.db.execute(creation_query)

        # Re-run the original query
        return self.db.execute(query)

    def _build_sql_query(
        self,
        type: Type[M],
        filter: Filter | None = None,
        *,
        projection: str = "*",
        sort: DbField | FieldSort | Iterable[DbField | FieldSort] | None = None,
        skip: int = 0,
        limit: int | None = None,
    ) -> str:
        # Prepare the filter
        if filter is None:
            filter = Unfilter()

        filter_str = filter._as_sql_filter()

        # Prepare the sort
        if sort is None:
            sort_str = ""
        elif isinstance(sort, DbField):
            sort_str = f"ORDER BY {sort.sql_escape()}"
        elif isinstance(sort, FieldSort):
            sort_str = f"ORDER BY {sort._field.sql_escape()} {'ASC' if sort._sort_ascending else 'DESC'}"
        else:
            subsorts = []

            for s in sort:
                if isinstance(s, DbField):
                    subsorts.append(s.sql_escape())
                else:
                    subsorts.append(
                        f"{s._field.sql_escape()} {'ASC' if s._sort_ascending else 'DESC'}"
                    )

            sort_str = f"ORDER BY {', '.join(subsorts)}"

        # Skip / limit
        if limit is None:
            limit_str = ""
        else:
            limit_str = f"LIMIT {limit}"

        # Prepare the query
        return f"SELECT {projection} FROM {_table_name_from_type(type)} WHERE {filter_str} {sort_str} {limit_str} OFFSET {skip}"

    def insert(self, *instances: DbModel) -> None:
        """
        Inserts the given instance into the database.
        """
        # Anything to do?
        if not instances:
            return

        # Get the field names
        fields: list[DbField] = list(instances[0]._db_fields_.values())
        field_names: list[str] = [
            _escape_duckdb_column_name(f.name) for f in fields
        ]

        # Prepare the values
        value_tuples: list[str] = []

        for instance in instances:
            values = []

            for field in fields:
                value = field.__get__(instance)
                values.append(_value_as_duckdb(value))

            value_tuples.append(f"({', '.join(values)})")

        # Execute the query
        query = f"INSERT INTO {_table_name_from_type(type(instance))} ({', '.join(field_names)}) VALUES {', '.join(value_tuples)}"
        self._run_query_with_table(type(instance), query)

    def count(self, type: Type[M], filter: Filter | None = None) -> int:
        """
        Counts the number of instances matching the given filter.
        """
        # Prepare the query
        query = self._build_sql_query(type, filter, projection="COUNT(*)")

        # Run it
        #
        # There is no need to ensure the table exists, as a missing table simply
        # indicates that there are no matches.
        try:
            cursor = self.db.execute(query)
        except duckdb.CatalogException:
            return 0
        else:
            result = cursor.fetchone()
            assert isinstance(result, tuple), result

            result = result[0]
            assert isinstance(result, int), result

            return result

    def find(
        self,
        type: Type[M],
        filter: Filter | None = None,
        *,
        sort: DbField | FieldSort | Iterable[DbField | FieldSort] | None = None,
        skip: int = 0,
        limit: int | None = None,
    ) -> Iterable[M]:
        """
        Retrieves all instances matching the given filter.
        """
        # Prepare the query
        query = self._build_sql_query(
            type, filter, sort=sort, skip=skip, limit=limit
        )

        # Execute the query
        cursor = self.db.execute(query)

        # Fetch the results
        for row in cursor.fetchall():
            yield type(*row)  # TODO

    def find_one(
        self,
        type: Type[T],
        filter: Filter | None = None,
        *,
        sort: DbField | FieldSort | Iterable[DbField | FieldSort] | None = None,
        skip: int = 0,
    ) -> T:
        """
        Retrieves the first instance matching the given filter. If no sort is
        provided, any matching instance is returned.

        ## Raises

        `KeyError`: If no instance matches the filter.
        """
        result = self.find(type, filter, sort=sort, skip=skip, limit=1)

        if result:
            return result[0]

        raise KeyError("No instance matches the filter.")


# Just some test code
if __name__ == "__main__":
    duckdb_connection = duckdb.connect(":memory:")
    sync_accessor = SyncAccessor(duckdb_connection)

    # Define some test models
    class TestModel(DbModel):
        name: str = "foo"
        age: int = 42

    # For now, manually ensure the table exists
    duckdb_connection.execute(
        "CREATE TABLE instances__DbModel (id UUID PRIMARY KEY)"
    )

    # Run some commands
    print(sync_accessor.count(DbModel))

    sync_accessor.insert(
        TestModel(name="Name 1", age=1),
        TestModel(name="Name 2", age=2),
        TestModel(name="Name 3", age=3),
        DbModel(id=uuid.uuid4()),
    )

    print(sync_accessor.count(DbModel))

    for match in sync_accessor.find(DbModel):
        print(match)
