import pandas as pd

def analyze_posting_schedule(df):
    df["day_of_week"] = df["takenAtTimestamp"].dt.day_name()
    df["hour"] = df["takenAtTimestamp"].dt.hour
    return df.groupby(["day_of_week", "hour"]).size().unstack(fill_value=0)
