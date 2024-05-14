from ml_extra.utils.utils import get_root_path

import mlflow
from mlflow.entities import Experiment
from typing import Dict


def get_or_create_experiment(name: str, tags: Dict[str, str] = {}) -> Experiment:
    """
    Get or create an experiment with the given name and tags.

    :param name: The name of the experiment.
    :param tags: The tags of the experiment.
    :return: The experiment.
    """

    root_dir = get_root_path()
    mlflow.set_tracking_uri((root_dir / "mlruns").as_uri())
    experiment = mlflow.get_experiment_by_name(name)
    if experiment is None:
        experiment_id = mlflow.create_experiment(name, tags=tags)
        experiment = mlflow.get_experiment(experiment_id)

    mlflow.set_experiment(experiment_name=name)

    return experiment
