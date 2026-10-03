import pandas as pd


def execute_analysis(df, plan):

    operation = plan.get("operation")


    # =========================================
    # COUNT
    # =========================================

    if operation == "count":

        return {
            "result": len(df)
        }


    # =========================================
    # PROFILE
    # =========================================

    elif operation == "profile":

        return {
            "result": {
                "rows": len(df),
                "columns": len(df.columns),
                "column_names": list(df.columns),
                "missing_values": (
                    df.isnull().sum().to_dict()
                ),
                "duplicate_rows": int(
                    df.duplicated().sum()
                )
            }
        }


    # =========================================
    # QUALITY
    # =========================================

    elif operation == "quality":

        missing_values = (
            df.isnull().sum()
        )

        missing_values = (
            missing_values[
                missing_values > 0
            ]
        )

        duplicate_rows = int(
            df.duplicated().sum()
        )

        total_missing = int(
            df.isnull().sum().sum()
        )

        return {
            "result": {
                "total_missing_values": total_missing,

                "missing_by_column":
                    missing_values.to_dict(),

                "duplicate_rows":
                    duplicate_rows
            }
        }


    # =========================================
    # AGGREGATE
    # =========================================

    elif operation == "aggregate":

        column = plan.get("value_column")

        aggregation = plan.get(
            "aggregation"
        )

        if column not in df.columns:

            return {
                "error":
                f"Column '{column}' does not exist."
            }

        if aggregation == "mean":

            result = df[column].mean()

        elif aggregation == "sum":

            result = df[column].sum()

        elif aggregation == "max":

            result = df[column].max()

        elif aggregation == "min":

            result = df[column].min()

        elif aggregation == "count":

            result = df[column].count()

        elif aggregation == "median":

            result = df[column].median()

        else:

            return {
                "error":
                f"Unsupported aggregation: {aggregation}"
            }

        return {
            "result": result
        }


    # =========================================
    # GROUPBY
    # =========================================

    elif operation == "groupby":

        group_column = plan.get(
            "group_column"
        )

        value_column = plan.get(
            "value_column"
        )

        aggregation = plan.get(
            "aggregation"
        )

        if group_column not in df.columns:

            return {
                "error":
                f"Column '{group_column}' does not exist."
            }

        if value_column not in df.columns:

            return {
                "error":
                f"Column '{value_column}' does not exist."
            }

        if aggregation == "sum":

            result = (
                df.groupby(group_column)
                [value_column]
                .sum()
            )

        elif aggregation == "mean":

            result = (
                df.groupby(group_column)
                [value_column]
                .mean()
            )

        elif aggregation == "count":

            result = (
                df.groupby(group_column)
                [value_column]
                .count()
            )

        elif aggregation == "median":

            result = (
                df.groupby(group_column)
                [value_column]
                .median()
            )

        else:

            return {
                "error":
                f"Unsupported aggregation: {aggregation}"
            }

        sort_order = plan.get("sort")

        if sort_order == "descending":

            result = result.sort_values(
                ascending=False
            )

        elif sort_order == "ascending":

            result = result.sort_values(
                ascending=True
            )

        limit = plan.get("limit")

        if limit:

            result = result.head(
                int(limit)
            )

        return {
            "result": result
        }


    # =========================================
    # FILTER
    # =========================================

    elif operation == "filter":

        column = plan.get("column")

        operator = plan.get("operator")

        value = plan.get("value")

        if column not in df.columns:

            return {
                "error":
                f"Column '{column}' does not exist."
            }

        try:

            if operator == ">":

                filtered = df[
                    df[column] > value
                ]

            elif operator == "<":

                filtered = df[
                    df[column] < value
                ]

            elif operator == ">=":

                filtered = df[
                    df[column] >= value
                ]

            elif operator == "<=":

                filtered = df[
                    df[column] <= value
                ]

            elif operator == "==":

                filtered = df[
                    df[column] == value
                ]

            elif operator == "!=":

                filtered = df[
                    df[column] != value
                ]

            else:

                return {
                    "error":
                    f"Unsupported operator: {operator}"
                }

        except Exception as error:

            return {
                "error":
                f"Could not filter data: {error}"
            }

        return {
            "result": filtered
        }


    # =========================================
    # SORT
    # =========================================

    elif operation == "sort":

        column = plan.get("column")

        order = plan.get(
            "sort",
            "descending"
        )

        if column not in df.columns:

            return {
                "error":
                f"Column '{column}' does not exist."
            }

        ascending = (
            order == "ascending"
        )

        result = df.sort_values(
            by=column,
            ascending=ascending
        )

        limit = plan.get("limit")

        if limit:

            result = result.head(
                int(limit)
            )

        return {
            "result": result
        }


    # =========================================
    # TOP N
    # =========================================

    elif operation == "top_n":

        column = plan.get("column")

        n = int(
            plan.get("limit", 5)
        )

        if column not in df.columns:

            return {
                "error":
                f"Column '{column}' does not exist."
            }

        result = df.nlargest(
            n,
            column
        )

        return {
            "result": result
        }


    # =========================================
    # BOTTOM N
    # =========================================

    elif operation == "bottom_n":

        column = plan.get("column")

        n = int(
            plan.get("limit", 5)
        )

        if column not in df.columns:

            return {
                "error":
                f"Column '{column}' does not exist."
            }

        result = df.nsmallest(
            n,
            column
        )

        return {
            "result": result
        }


    # =========================================
    # CORRELATION
    # =========================================

    elif operation == "correlation":

        columns = plan.get(
            "columns",
            []
        )

        if len(columns) < 2:

            return {
                "error":
                "At least two columns are required."
            }

        for column in columns:

            if column not in df.columns:

                return {
                    "error":
                    f"Column '{column}' does not exist."
                }

        result = df[
            columns
        ].corr()

        return {
            "result": result
        }


    # =========================================
    # OUTLIER
    # =========================================

    elif operation == "outlier":

        column = plan.get("column")

        if column not in df.columns:

            return {
                "error":
                f"Column '{column}' does not exist."
            }

        if not pd.api.types.is_numeric_dtype(
            df[column]
        ):

            return {
                "error":
                f"Column '{column}' is not numeric."
            }

        Q1 = df[column].quantile(
            0.25
        )

        Q3 = df[column].quantile(
            0.75
        )

        IQR = Q3 - Q1

        lower_bound = (
            Q1 - 1.5 * IQR
        )

        upper_bound = (
            Q3 + 1.5 * IQR
        )

        result = df[
            (df[column] < lower_bound)
            |
            (df[column] > upper_bound)
        ]

        return {
            "result": result,

            "lower_bound":
                lower_bound,

            "upper_bound":
                upper_bound
        }


    # =========================================
    # TREND
    # =========================================

    elif operation == "trend":

        group_column = plan.get(
            "group_column"
        )

        value_column = plan.get(
            "value_column"
        )

        aggregation = plan.get(
            "aggregation"
        )

        if group_column not in df.columns:

            return {
                "error":
                f"Column '{group_column}' does not exist."
            }

        if value_column not in df.columns:

            return {
                "error":
                f"Column '{value_column}' does not exist."
            }

        data = df.copy()

        data[group_column] = pd.to_datetime(
            data[group_column],
            errors="coerce"
        )

        data = data.dropna(
            subset=[group_column]
        )

        if aggregation == "sum":

            result = (
                data.groupby(group_column)
                [value_column]
                .sum()
            )

        elif aggregation == "mean":

            result = (
                data.groupby(group_column)
                [value_column]
                .mean()
            )

        elif aggregation == "count":

            result = (
                data.groupby(group_column)
                [value_column]
                .count()
            )

        else:

            return {
                "error":
                f"Unsupported trend aggregation: {aggregation}"
            }

        result = result.sort_index()

        return {
            "result": result
        }


    # =========================================
    # DISTRIBUTION
    # =========================================

    elif operation == "distribution":

        column = plan.get(
            "column"
        )

        if column not in df.columns:

            return {
                "error":
                f"Column '{column}' does not exist."
            }

        if not pd.api.types.is_numeric_dtype(
            df[column]
        ):

            return {
                "error":
                f"Column '{column}' is not numeric."
            }

        result = df[
            [column]
        ].dropna()

        return {
            "result": result
        }


    # =========================================
    # COMPARE
    # =========================================

    elif operation == "compare":

        columns = plan.get(
            "columns",
            []
        )

        if len(columns) < 2:

            return {
                "error":
                "Two columns are required for comparison."
            }

        for column in columns:

            if column not in df.columns:

                return {
                    "error":
                    f"Column '{column}' does not exist."
                }

            if not pd.api.types.is_numeric_dtype(
                df[column]
            ):

                return {
                    "error":
                    f"Column '{column}' must be numeric."
                }

        result = df[
            columns
        ].dropna()

        return {
            "result": result
        }


    # =========================================
    # UNSUPPORTED
    # =========================================

    else:

        return {
            "error":
            f"Unsupported operation: {operation}"
        }