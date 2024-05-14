import pandas as pd

def load_dataframe(file_path: str) -> pd.DataFrame:
    return validate_dataframe(pd.read_csv(file_path))

def validate_dataframe(df:pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        raise ValueError("DataFrame is empty!")
    else:
        return df