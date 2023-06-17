import os
import datetime
from zenml.config import DockerSettings
from zenml.config.schedule import Schedule
from pipelines.nfld_pipeline import training_nfld_model
from zenml.integrations.airflow.flavors.airflow_orchestrator_flavor import AirflowOrchestratorSettings
from steps.nfld_steps import (import_data, preprocess_data,
                              training_SVC, training_dct
                              )

date_time = datetime.datetime.now()

airflow_settings = AirflowOrchestratorSettings(
    operator="docker",  # or "kubernetes_pod"
    # use your directory path to the zipped_pipes directory
    dag_output_dir=f"{os.getcwd()}/zipped_pipelines",
    dag_id=f"non_fatty_liver_trainingx",
    dag_tags=["zenml", "MLOPS", "Training"],
    # custom_dag_generator="zenml_custom_dag_template"
)
docker_settings = DockerSettings(
    requirements=["pandas", "scikit-learn", "boto3", "botocore==1.29.146"])


def main():
    # init and run the nfdl classifier training pipeline
    schedule = Schedule(cron_expression="5-15 * * * *")
    run_nfdl_training = training_nfld_model(
        import_datax=import_data(),
        preprocess_datax=preprocess_data(),
        training_SVCx=training_SVC(),
        training_dctx=training_dct()
    )

    run_nfdl_training.run(settings={"orchestrator.airflow": airflow_settings,
                                    "docker": docker_settings}, schedule=schedule,
                          run_name=f"custom_pipeline_run_name_{date_time}")  # this to create unique run name and avoid EntityExistsError


if __name__ == "__main__":
    main()
