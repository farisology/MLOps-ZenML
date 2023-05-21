import numpy as np
import pandas as pd
from sklearn.svm import SVC
from zenml.steps import step, Output
from sklearn.impute import KNNImputer
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split


@step
def import_data() -> Output(dataset=pd.DataFrame):
    df = pd.read_csv("nafld1.csv")
    return df


@step
def preprocess_data(dataset: pd.DataFrame) -> Output(features=np.ndarray, labels=pd.core.series.Series):
    # remove the redundant columns
    data = dataset.drop(['id', 'Unnamed: 0', 'case.id'], axis=1)
    labels = data.pop('status')

    # impute the missing values using the KNNImputer
    imputer = KNNImputer(n_neighbors=2, weights="uniform")
    imputer = imputer.fit(data)
    features = imputer.transform(data)

    return features, labels


@step
def training_SVC(features: np.ndarray, labels: pd.core.series.Series) -> SVC:
    x_train, x_test, y_train, y_test = train_test_split(
        features, labels, test_size=0.2)
    svc_model = SVC()
    svc_model.fit(x_train, y_train)

    y_pred = svc_model.predict(x_test)
    print(classification_report(y_test, y_pred))
    return svc_model


@step
def training_dct(features: np.ndarray, labels: pd.core.series.Series) -> DecisionTreeClassifier:
    x_train, x_test, y_train, y_test = train_test_split(
        features, labels, test_size=0.2)
    dct_model = DecisionTreeClassifier()
    dct_model.fit(x_train, y_train)

    y_pred = dct_model.predict(x_test)
    print(classification_report(y_test, y_pred))
    return dct_model
