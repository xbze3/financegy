import os
import pandas as pd

def to_dataframe(data: dict | list[dict]):
    """Output as Dataframe"""

    if isinstance(data, list) and not all(isinstance(item, dict) for item in data):
        raise TypeError("All items in the list must be dictionaries")
    elif not isinstance(data, (dict, list)):
        raise TypeError("data must be a dict or a list of dicts")
    
    if isinstance(data, dict):
        data = [data]      

    return pd.DataFrame(data)

def save_to_csv(data, filename: str = "output.csv", path: str = None):
    """Save a list of dicts to CSV"""

    if path is None:
        path = os.getcwd()
    else:
        path = os.path.abspath(path)

    full_path = os.path.join(path, filename)

    df = to_dataframe(data)

    df.to_csv(full_path, index=False)

    print(f"Saved CSV to: {full_path}")

    return True

def save_to_excel(data: dict | list[dict], filename: str = "output.xlsx", path: str = None):
    """Save data to an Excel spreadsheet."""
    
    if path is None:
        path = os.getcwd()
    else:
        path = os.path.abspath(path)

    full_path = os.path.join(path, filename)
    df = to_dataframe(data)
    df.to_excel(full_path, index=False)
    
    print(f"Saved Excel Document to: {full_path}")
    return True



