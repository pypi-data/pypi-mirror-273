import warnings

import pandas as pd

# TODO - Replace return types with Gable Types
# from gable.openapi import (
#     FieldModel,
#     GableSchemaBool,
#     GableSchemaFloat,
#     GableSchemaInt,
#     GableSchemaList,
#     GableSchemaNull,
#     GableSchemaString,
#     GableSchemaStruct,
#     GableSchemaType,
#     GableSchemaUnion,
# )


class NativeS3Converter:
    def __init__(self):
        pass

    def to_recap(self, df: pd.DataFrame, has_schema: bool, event_name: str) -> dict:
        """
        Convert a pandas DataFrame to a Recap StructType.
        Args:
            df (pd.DataFrame): The pandas DataFrame to convert.
            event_name (str): The name of the field.
            has_schema (bool): Whether the DataFrame has a predefined schema. If False, the schema will be inferred based on its contents
        Returns:
            StructType: The Recap StructType representing the DataFrame.
        """
        schema = self._get_schema(df, has_schema)
        nullable = df.isnull().any()
        fields = []
        for field_name, field_dtype in schema.items():
            try:
                # Handle column representing nested JSON field
                # ex: customerDetails.technicalContact.email
                if "." in field_name:
                    self._handle_nested_fields(
                        field_name,
                        field_dtype,
                        nullable,
                        fields,
                        df[field_name],  # type: ignore
                        has_schema,
                    )
                else:
                    gable_type = self._parse_type(
                        str(field_dtype),
                        field_name,
                        nullable[field_name],  # type: ignore
                        df[field_name],  # type: ignore
                        has_schema,
                    )
                    fields.append(gable_type)
            except ValueError as e:
                print(f"Error parsing field {field_name} of type {field_dtype}: {e}")

        return {"fields": fields, "name": event_name, "type": "struct"}

    def _parse_type(
        self,
        dtype: str,
        field_name: str,
        nullable: bool,
        column: pd.Series,
        has_schema: bool,
    ) -> dict:
        """
        Parse a Dataframe dtype and return the corresponding Gable Type.
        Args:
            field_type (str): The field type to parse.
            field_name (str): The name of the field.
            nullable (bool): Whether the field is nullable.
            column (pd.Series): The column to parse.
            has_schema (bool): Whether the DataFrame has a predefined schema. If False, the schema will be inferred based on its contents
        Returns:
            The Gable Type corresponding to the field type.
        """

        if dtype == "string":
            type = {"type": "string", "name": field_name}
        elif dtype == "Int64":
            type = {"type": "int", "name": field_name, "bits": 64}
        elif dtype == "Int32":
            type = {"type": "int", "name": field_name, "bits": 32}
        elif dtype == "Float64":
            type = {"type": "float", "name": field_name, "bits": 64}
        elif dtype == "boolean":
            type = {"type": "bool", "name": field_name}
        elif dtype == "object":
            # TODO - figure out what is inside the list
            type = {"type": "list", "name": field_name, "values": {"type": "Unknown"}}
        elif dtype.startswith("datetime64[ns") and dtype.endswith(
            "]"
        ):  # datetime string representation may have timezone inside
            type = self._parse_datetime_type(column, field_name)
        else:
            raise ValueError(f"Unsupported dtype: {dtype}")

        # if it already has a schema don't dig through the column
        if not has_schema and nullable:
            if column.isnull().all():  # If we only see null values, return a null type
                return {
                    "type": "null",
                    "name": field_name,
                }
            type = {
                "type": "union",
                "types": [type, {"type": "null"}],
                "name": field_name,
            }
            # in conversations with Adrian and Suzanne, we determined that it's safe (in the short term)
            # to assume that when a dtype is an object and also nullable, that it's a null type.
            # the above todo for determining list types will need to be tackled in future work and may include a refactoring to replace pandas for JSON parsing/inference
            if dtype == "object":
                type = {
                    "type": "null",
                    "name": field_name,
                }

        return type

    def _parse_datetime_type(self, column: pd.Series, field_name: str) -> dict:
        """
        Parse a datetime type and return the corresponding Gable Type.
        Args:
            df (pd.DataFrame): The pandas DataFrame to convert.
            field_name (str): The name of the field.
        Returns:
            The Gable Type corresponding to the field type.
        """
        # If the datetime column has a timezone, assume it's a timestamp
        if column.dt.tz is not None:
            return {
                "type": "int",
                "logical": "build.recap.Timestamp",
                "name": field_name,
                "bits": 64,
            }

        # If all values are midnight, assume it's a date
        is_date = (
            all(column.dt.hour == 0)
            and all(column.dt.minute == 0)
            and all(column.dt.second == 0)
            and all(column.dt.microsecond == 0)
            and all(column.dt.nanosecond == 0)
        )
        if is_date:
            return {
                "type": "int",
                "logical": "build.recap.Date",
                "name": field_name,
                "bits": 64,
            }

        # If we could not determine, assume it's a timestamp
        return {
            "type": "int",
            "logical": "build.recap.Timestamp",  # TODO - improve. Consider a Duration, Time, etc.
            "name": field_name,
            "bits": 64,
        }

    def _handle_nested_fields(
        self,
        field_name: str,
        field_type: str,
        nullable,
        current_level_fields: list[dict],
        column: pd.Series,
        has_schema: bool,
    ):
        """
        Handle nested fields in a DataFrame.
        Args:
            field_name (str): The name of the field.
            field_type (str): The field type to parse.
            nullable (pd.Series): Whether the field is nullable.
            current_level_fields (list): The current "level" of fields.
            column (pd.Series): The column to parse.
            has_schema (bool): Whether the DataFrame has a predefined schema. If False, the schema will be inferred based on its contents
        """

        field_name_parts = field_name.split(".")
        # Iterate through each "level" of the nested fields
        for index, subfield_name in enumerate(field_name_parts):
            # Look to see if the subfield has already been added to the current level
            found_recap_type = next(
                (
                    field
                    for field in current_level_fields
                    if field["name"] == subfield_name
                ),
                None,
            )
            if found_recap_type is not None:
                subfield_recap_type = found_recap_type
            else:
                if index == len(field_name_parts) - 1:
                    # Last item in the list is not a StructType
                    subfield_recap_type = self._parse_type(
                        str(field_type),
                        subfield_name,
                        nullable[field_name],
                        column,
                        has_schema,
                    )
                else:
                    subfield_recap_type = {
                        "fields": [],
                        "name": subfield_name,
                        "type": "struct",
                    }
                current_level_fields.append(subfield_recap_type)

            if subfield_recap_type["type"] == "struct":
                # Update current_level_fields to the next "level"
                current_level_fields = subfield_recap_type["fields"]

    def _get_schema(self, df: pd.DataFrame, has_schema: bool) -> dict[str, str]:
        # If dataframe is from no header csv and column names are ints, we convert them to strings
        df.columns = df.columns.astype(str)

        # if it has a schema already, assume it is correct and don't try coercing types down
        if not has_schema:
            with warnings.catch_warnings():
                # Stop pandas from warning about converting types and spamming the console logs
                warnings.simplefilter(action="ignore", category=UserWarning)
                # Loop through each column and attempt to convert it to the most specific type
                for col in df.columns:
                    try:
                        df[col] = pd.to_numeric(df[col], errors="raise")
                    except:
                        try:
                            df[col] = pd.to_datetime(
                                df[col], infer_datetime_format=True, errors="raise"
                            )
                        except:
                            pass
                            # TODO: Add other specific types here
        return df.convert_dtypes().dtypes.to_dict()
