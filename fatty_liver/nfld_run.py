from zenml.config.schedule import Schedule
from pipelines.nfld_pipeline import training_nfld_model
from steps.nfld_steps import (import_data, preprocess_data,
                              training_SVC, training_dct
                              )


def main():
    # init and run the nfdl classifier training pipeline
    run_nfdl_training = training_nfld_model(
        import_data=import_data(),
        preprocess_data=preprocess_data(),
        training_SVC=training_SVC(),
        training_dct=training_dct()
    )

    run_nfdl_training.run()


if __name__ == "__main__":
    main()
