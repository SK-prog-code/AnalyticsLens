import pandas as pd


def summarize_result(result, plan):

    if result is None:
        return "No result was produced."


    # =========================================
    # SINGLE VALUE
    # =========================================

    if not isinstance(result, (pd.DataFrame, pd.Series)):

        return str(result)


    # =========================================
    # SERIES RESULT
    # =========================================

    if isinstance(result, pd.Series):

        summary = {
            "type": "series",
            "name": result.name,
            "number_of_values": len(result),
            "values": result.head(20).to_dict()
        }

        return str(summary)


    # =========================================
    # DATAFRAME RESULT
    # =========================================

    if isinstance(result, pd.DataFrame):

        summary = {
            "type": "dataframe",

            "rows": len(result),

            "columns": list(
                result.columns
            ),

            "first_rows":
                result.head(10).to_dict(
                    orient="records"
                )
        }


        # =====================================
        # NUMERIC SUMMARY
        # =====================================

        numeric_columns = (
            result.select_dtypes(
                include="number"
            ).columns.tolist()
        )


        if numeric_columns:

            summary["numeric_summary"] = (
                result[numeric_columns]
                .describe()
                .round(2)
                .to_dict()
            )


        return str(summary)


    return str(result)