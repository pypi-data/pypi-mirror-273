import chardet
import pandas as pd

def get_encode(file_path:str):
    with open(file_path, 'rb') as f:
        data = f.read()

    encoding_result = chardet.detect(data)
    encoding = encoding_result['encoding']
    return encoding

def cvs_2_dataset(file_path:str):
    return pd.read_csv(file_path, encoding=get_encode(file_path))