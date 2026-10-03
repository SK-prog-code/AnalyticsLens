import pandas as pd


def get_dataset_info(df):

    info = {}

    info["rows"] = len(df)

    info["columns"] = len(df.columns)

    info["column_names"] = list(df.columns)

    info["data_types"] = (
        df.dtypes.astype(str).to_dict()
    )

    info["missing_values"] = (
        df.isnull().sum().to_dict()
    )

    info["duplicate_rows"] = int(
        df.duplicated().sum()
    )

    return info


def create_dataset_context(df):

    info = get_dataset_info(df)

    # -----------------------------------------
    # Basic information
    # -----------------------------------------

    context = f"""
DATASET INFORMATION

Number of rows:
{info["rows"]}

Number of columns:
{info["columns"]}

Column names:
{info["column_names"]}

Data types:
{info["data_types"]}

Missing values:
{info["missing_values"]}

Duplicate rows:
{info["duplicate_rows"]}
"""


    # -----------------------------------------
    # Sample data
    # -----------------------------------------

    context += """

FIRST 10 ROWS:

"""

    context += df.head(10).to_string(
        index=False
    )


    # -----------------------------------------
    # Numeric columns
    # -----------------------------------------

    numeric_columns = (
        df.select_dtypes(
            include="number"
        ).columns.tolist()
    )


    if numeric_columns:

        context += """

NUMERIC COLUMN SUMMARY:

"""

        numeric_summary = (
            df[numeric_columns]
            .describe()
            .round(2)
        )

        context += numeric_summary.to_string()


    # -----------------------------------------
    # Categorical columns
    # -----------------------------------------

    categorical_columns = (
        df.select_dtypes(
            include=["object", "category"]
        ).columns.tolist()
    )


    if categorical_columns:

        context += """

CATEGORICAL COLUMNS:

"""

        for column in categorical_columns[:10]:

            unique_values = (
                df[column]
                .dropna()
                .unique()
                .tolist()
            )

            # Limit the number of values
            unique_values = unique_values[:20]

            context += (
                f"\n{column}: "
                f"{unique_values}"
            )


    return context