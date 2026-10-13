import pandas as pd


def summarize_bmi_by_group(data: pd.DataFrame) -> pd.DataFrame:
    """Summarize observed and missing BMI by income group and gender."""
    required_columns = {"BMI", "IncomeGroup", "Gender"}
    missing_columns = required_columns.difference(data.columns)
    if missing_columns:
        raise ValueError(f"Missing required columns: {sorted(missing_columns)}")

    summary = (
        data.dropna(subset=["IncomeGroup", "Gender"])
        .groupby(["IncomeGroup", "Gender"])["BMI"]
        .agg(
            n="count",
            n_missing_bmi=lambda values: values.isna().sum(),
            mean_bmi="mean",
            sd_bmi="std",
            median_bmi="median",
            iqr_bmi=lambda values: values.quantile(0.75) - values.quantile(0.25),
        )
        .reset_index()
    )

    summary_columns = ["mean_bmi", "sd_bmi", "median_bmi", "iqr_bmi"]
    summary[summary_columns] = summary[summary_columns].round(2)
    return summary