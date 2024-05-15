from enum import Enum
from typing import Any


class Order(str, Enum):
    """Use this with the order_by_columns and default_order parameter of the select function."""

    ASCENDING = "ASC"
    DESCENDING = "DESC"
    DEFAULT = "DEFAULT"


class TableCreateMode(str, Enum):
    """Options for create_table if the table already exists
    ERROR_IF_TABLE_EXISTS: Raise exception if the table exists
    REPLACE_CURR_TABLE: Replace existing table with the same name
    RETURN_CURR_TABLE: Return the existing table when create_table is called"""

    ERROR_IF_TABLE_EXISTS = "ERROR_IF_TABLE_EXISTS"
    REPLACE_CURR_TABLE = "REPLACE_CURR_TABLE"
    RETURN_CURR_TABLE = "RETURN_CURR_TABLE"


class ImageFormat(str, Enum):
    """Image format enum. Used with the Image column type."""

    JPEG = "JPEG"
    PNG = "PNG"
    TIFF = "TIFF"
    GIF = "GIF"
    BMP = "BMP"


class OperationEnum(str, Enum):
    NOT = "$!"
    AND = "$&"
    OR = "$|"
    GREATER_THAN = "$GT"
    LESS_THAN = "$LT"
    GREATER_THAN_OR_EQUAL = "$GTE"
    LESS_THAN_OR_EQUAL = "$LTE"
    EQUAL = "$EQ"
    NOT_EQUAL = "$NEQ"
    LIKE = "$LIKE"
    NOT_LIKE = "$NLIKE"


ColumnName = str
TableName = str
RowDict = dict[ColumnName, Any]
OrderByColumns = ColumnName | tuple[ColumnName, Order] | list[ColumnName | tuple[ColumnName, Order]]
