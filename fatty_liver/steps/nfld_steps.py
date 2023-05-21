import pandas as pd
from zenml.steps import step, Output


@step
def import_data(path: str) -> Output(dataset=pd.DataFrame):
    df = pd.read_csv(path)
    return df
