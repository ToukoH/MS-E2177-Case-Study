import pandas as pd

def data_processing(datapath: str) -> pd.DataFrame:
    data = pd.read_csv(datapath, delimiter=";", index_col=False)
    data = data.replace(",", ".", regex=True)
    data = data.apply(pd.to_numeric)
    return data