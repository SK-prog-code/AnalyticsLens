import matplotlib.pyplot as plt
import pandas as pd


def create_chart(result, plan):

    visualization = plan.get("visualization")

    if visualization == "none":
        return None

    # -------------------------
    # BAR CHART
    # -------------------------
    if visualization == "bar":

        if not isinstance(result, pd.Series):
            return None

        fig, ax = plt.subplots()

        result.plot(
            kind="bar",
            ax=ax
        )

        ax.set_title(
            f"{plan.get('value_column')} by "
            f"{plan.get('group_column')}"
        )

        ax.set_xlabel(
            plan.get("group_column")
        )

        ax.set_ylabel(
            plan.get("value_column")
        )

        plt.xticks(rotation=45)
        plt.tight_layout()

        return fig

    # -------------------------
    # LINE CHART
    # -------------------------
    if visualization == "line":

        if not isinstance(result, pd.Series):
            return None

        fig, ax = plt.subplots()

        result.plot(
            kind="line",
            marker="o",
            ax=ax
        )

        ax.set_title(
    f"{plan.get('value_column')} Trend"
)

        ax.set_xlabel(
            plan.get("group_column")
        )

        ax.set_ylabel(
            plan.get("value_column")
        )

        plt.xticks(rotation=45)
        plt.tight_layout()

        return fig

    # -------------------------
    # HISTOGRAM
    # -------------------------
    if visualization == "histogram":

        column = plan.get("column")

        if column is None:
            return None

        if column not in result.columns:
            return None

        fig, ax = plt.subplots()

        result[column].plot(
            kind="hist",
            bins=20,
            ax=ax
        )

        ax.set_title(
            f"Distribution of {column}"
        )

        ax.set_xlabel(column)
        ax.set_ylabel("Frequency")

        plt.tight_layout()

        return fig

    # -------------------------
    # SCATTER PLOT
    # -------------------------
    if visualization == "scatter":

        columns = plan.get("columns", [])

        if len(columns) < 2:
            return None

        x_column = columns[0]
        y_column = columns[1]

        if x_column not in result.columns:
            return None

        if y_column not in result.columns:
            return None

        fig, ax = plt.subplots()

        ax.scatter(
            result[x_column],
            result[y_column]
        )

        ax.set_title(
            f"{x_column} vs {y_column}"
        )

        ax.set_xlabel(x_column)
        ax.set_ylabel(y_column)

        plt.tight_layout()

        return fig

    return None