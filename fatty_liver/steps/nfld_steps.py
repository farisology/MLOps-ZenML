import pandas as pd
from zenml.steps import step, Output
from sklearn.impute import KNNImputer


@step
def import_data(path: str) -> Output(dataset=pd.DataFrame):
    df = pd.read_csv(path)
    return df


@step
def preprocess_data(dataset: pd.DataFrame) -> Output(features=pd.DataFrame, labels=pd.DataFrame):
    # remove the redundant columns
    data = dataset.drop(['id', 'Unnamed: 0', 'case.id'], axis=1)
    labels = data.pop('status')

    # impute the missing values using the KNNImputer
    imputer = KNNImputer(n_neighbors=2, weights="uniform")
    imputer = imputer.fit(data)
    features = imputer.transform(data)

    return features, labels
