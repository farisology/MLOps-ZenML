from zenml.pipelines import pipeline


@pipeline
def training_nfld_model(import_data, preprocess_data, training_SVC, training_dct):
    """Training non-fatty liver classifier"""
    alldata = import_data()
    x, y = preprocess_data(alldata)
    svc = training_SVC(x, y)
    dct = training_dct(x, y)
