import pandas as pd
from glob import glob

def getDataset(day: str, path: str="data/datasets/") -> object:
    """
        Return a DataFrame object containing the data of the day chosen
        'day' parameter should be a str in that format:
        %Y_%m_%d
    """
    df = pd.read_csv(path+"stations_status_" + day + ".zip")
    df['time'] = pd.to_datetime(df['time'])
    df = df.drop(["Unnamed: 0"] , axis=1)
    return df

def listDatasets(path="data/datasets/") -> list:
    return glob(path+"stations_status_*.zip")
