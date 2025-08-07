import pandas as pd
from config import REQUIRED_COLUMNS

def normalize_data(raw_data):
    """
    Normalize and clean Instagram data from Apify scraper
    """
    if not raw_data:
        raise ValueError("No data provided to normalize")
    
    try:
        # Convert to DataFrame
        df = pd.json_normalize(raw_data)
        
        # Check if required columns exist
        missing_columns = [col for col in REQUIRED_COLUMNS if col not in df.columns]
        
        if missing_columns:
            print(f"⚠️  Warning: Missing columns: {missing_columns}")
            # Add missing columns with default values
            for col in missing_columns:
                if col in ["likesCount", "commentsCount"]:
                    df[col] = 0
                elif col == "caption":
                    df[col] = ""
                elif col == "takenAtTimestamp":
                    df[col] = pd.Timestamp.now().timestamp()
                else:
                    df[col] = ""
        
        # Select only the columns we need
        df = df[REQUIRED_COLUMNS]
        
        # Convert timestamp to datetime
        df["takenAtTimestamp"] = pd.to_datetime(df["takenAtTimestamp"], unit='s', errors='coerce')
        
        # Fill missing timestamps with current time (fixed chained assignment warning)
        df.loc[df["takenAtTimestamp"].isna(), "takenAtTimestamp"] = pd.Timestamp.now()
        
        # Convert numeric columns
        df["likesCount"] = pd.to_numeric(df["likesCount"], errors='coerce').fillna(0).astype(int)
        df["commentsCount"] = pd.to_numeric(df["commentsCount"], errors='coerce').fillna(0).astype(int)
        
        # Clean captions
        df["caption"] = df["caption"].fillna("")
        
        print(f"✅ Data normalized successfully. Shape: {df.shape}")
        return df
        
    except Exception as e:
        print(f"❌ Error normalizing data: {e}")
        raise
