import pandas as pd

def estimate_avg_engagement(df: pd.DataFrame) -> pd.DataFrame:
    df["day"] = df["takenAtTimestamp"].dt.day_name()
    df["hour"] = df["takenAtTimestamp"].dt.hour

    grouped = df.groupby(["day", "hour"]).agg({
        "likesCount": "mean",
        "commentsCount": "mean",
        "caption": "count"
    }).rename(columns={"caption": "num_posts"}).round(2)

    return grouped.sort_values(by="likesCount", ascending=False)
