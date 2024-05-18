import os
import pandas as pd
import requests

def load_data(name):
    data_dir = os.path.join(os.path.expanduser("~"), ".edudat_cache")
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    
    file_path = os.path.join(data_dir, name)
    if not os.path.exists(file_path):
        url = f"https://raw.githubusercontent.com/tensorchiefs/data/main/data/{name}"
        response = requests.get(url)
        response.raise_for_status()
        with open(file_path, 'wb') as f:
            f.write(response.content)
    
    return pd.read_csv(file_path)
