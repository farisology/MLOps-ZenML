import os
from zenml.config import DockerSettings
from zenml.config.schedule import Schedule
from pipelines.nfld_pipeline import training_nfld_model
from zenml.integrations.airflow.flavors.airflow_orchestrator_flavor import AirflowOrchestratorSettings
from steps.nfld_steps import (import_data, preprocess_data,
                              training_SVC, training_dct
                              )

airflow_settings = AirflowOrchestratorSettings(
    operator="docker",  # or "kubernetes_pod"
    # dag_output_dir=f"{os.getcwd()}/zipped_pipelines", #use your directory path to the zipped_pipes directory
    dag_id="non_fatty_liver_training",
    dag_tags=["zenml", "MLOPS", "Training"],
    # custom_dag_generator="zenml_custom_dag_template"
)
docker_settings = DockerSettings(requirements=["pandas", "scikit-learn", "boto3", "botocore==1.29.146"])

def main():
    # init and run the nfdl classifier training pipeline
    schedule = Schedule(cron_expression="5-15 * * * *")
    run_nfdl_training = training_nfld_model(
        import_data=import_data(),
        preprocess_data=preprocess_data(),
        training_SVC=training_SVC(),
        training_dct=training_dct()
    )

    run_nfdl_training.run(settings={"orchestrator.airflow": airflow_settings,
                                    "docker": docker_settings}, schedule=schedule)


if __name__ == "__main__":
    main()
