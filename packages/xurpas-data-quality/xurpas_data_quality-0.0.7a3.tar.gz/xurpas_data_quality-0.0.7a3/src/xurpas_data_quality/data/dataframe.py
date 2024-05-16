import os
import functools

import pandas as pd


def load_csv(file_path, **kwargs):
    return pd.read_csv(file_path)

def load_excel(file_path, **kwargs):
    return pd.read_excel(file_path, **kwargs)

def load_parquet(file_path, **kwargs):
    return pd.read_parquet(file_path, **kwargs)

def load_orc(file_path, **kwargs):
    return pd.read_orc(file_path, **kwargs)
    

def validate_dataframe(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        df = func(*args, **kwargs)
        if df.empty:
            raise ValueError("DataFrame is empty!")
        else:
            return df
    return wrapper

@validate_dataframe
def load_dataframe(file_path: str) -> pd.DataFrame:
    load_methods = {
    '.csv': load_csv,
    '.xlsx': load_excel,
    '.parquet': load_parquet,
    '.orc': load_orc
    }
    # Get the file extension
    _, file_extension = os.path.splitext(file_path)
    
    # Get the loading method from the dictionary
    load_method = load_methods.get(file_extension)
    
    # If the loading method exists, call it, else raise an error
    if load_method:
        return load_method(file_path)
    else:
        raise ValueError(f'Unsupported file format: {file_extension}')


    
