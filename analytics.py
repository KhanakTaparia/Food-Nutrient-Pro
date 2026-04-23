import pandas as pd

def weekly_summary(df):
    if df.empty:
        return None

    df["date"] = pd.to_datetime(df["date"])
    df["week"] = df["date"].dt.isocalendar().week

    return df.groupby("week").sum(numeric_only=True)


def streak(df):
    if df.empty:
        return 0

    return df["date"].nunique()