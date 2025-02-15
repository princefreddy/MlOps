import kfp
from kfp import dsl
from kfp.dsl import ContainerOp, PipelineParam

# Définir les images Docker pour chaque étape
PREPROCESS_IMAGE = "princefreddy/preprocessing:"
TRAIN_IMAGE = "princefreddy/training"
EVALUATE_IMAGE = "princefreddy/evaluation"

# Définir les chemins des données et des modèles
DATA_PATH = "/app/data/cleaned_data.csv"
MODEL_PATH = "/app/models/mlp_classifier_model.pkl"
METRICS_PATH = "/app/metrics/model_metrics.txt"

# Définir le pipeline Kubeflow
@dsl.pipeline(
    name="MLOps Pipeline",
    description="Un pipeline MLOps complet pour le prétraitement, l'entraînement et l'évaluation."
)
def mlops_pipeline(data_path: str = DATA_PATH, model_path: str = MODEL_PATH, metrics_path: str = METRICS_PATH):
    # Étape 1 : Prétraitement des données
    preprocess = ContainerOp(
        name="preprocess-data",
        image=PREPROCESS_IMAGE,
        command=["python", "preprocess.py"],
        arguments=["--data_path", data_path],
    )

    # Étape 2 : Entraînement du modèle
    train = ContainerOp(
        name="train-model",
        image=TRAIN_IMAGE,
        command=["python", "train.py"],
        arguments=["--data_path", data_path, "--model_path", model_path],
    ).after(preprocess)  # L'entraînement dépend du prétraitement

    # Étape 3 : Évaluation du modèle
    evaluate = ContainerOp(
        name="evaluate-model",
        image=EVALUATE_IMAGE,
        command=["python", "evaluate.py"],
        arguments=["--model_path", model_path, "--data_path", data_path, "--metrics_path", metrics_path],
    ).after(train)  # L'évaluation dépend de l'entraînement

# Soumettre le pipeline à Kubeflow
if __name__ == "__main__":
    # Créer un client Kubeflow
    client = kfp.Client()

    # Soumettre le pipeline
    client.create_run_from_pipeline_func(
        mlops_pipeline,
        arguments={
            "data_path": DATA_PATH,
            "model_path": MODEL_PATH,
            "metrics_path": METRICS_PATH,
        },
    )