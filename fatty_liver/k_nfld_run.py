import os
import datetime
from zenml.config import DockerSettings
from zenml.config.schedule import Schedule
from pipelines.nfld_pipeline import training_nfld_model
from steps.nfld_steps import (import_data, preprocess_data,
                              training_SVC, training_dct
                              )

from zenml.integrations.kubernetes.flavors.kubernetes_orchestrator_flavor import KubernetesOrchestratorSettings
from kubernetes.client.models import V1Toleration

date_time = datetime.datetime.now()


kubernetes_settings = KubernetesOrchestratorSettings(
    pod_settings={
        "affinity": {
            "nodeAffinity": {
                "requiredDuringSchedulingIgnoredDuringExecution": {
                    "nodeSelectorTerms": [
                        {
                            "matchExpressions": [
                                {
                                    "key": "node.kubernetes.io/linux",
                                    "operator": "In",
                                    "values": ["my_powerful_node_group"],
                                }
                            ]
                        }
                    ]
                }
            }
        },
        "tolerations": [
            V1Toleration(
                key="node.kubernetes.io/linux",
                operator="Equal",
                value="",
                effect="NoSchedule"
            )
        ]
    }
)
docker_settings = DockerSettings(
    requirements=["pandas", "scikit-learn", "boto3", "botocore==1.29.146"])


def main():
    # init and run the nfdl classifier training pipeline in k8 orchestrator
    schedule = Schedule(cron_expression="5-15 * * * *")
    run_nfdl_training = training_nfld_model(
        import_data=import_data(),
        preprocess_data=preprocess_data(),
        training_SVC=training_SVC(),
        training_dct=training_dct()
    )

    # run_nfdl_training.run(
    #     settings={"orchestrator.kubernetes": kubernetes_settings})
    run_nfdl_training.run()


if __name__ == "__main__":
    main()
