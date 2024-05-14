from typing import Tuple
from typing import Dict
import mlflow
from typing import Optional
import tempfile
from pathlib import Path
import inspect


def check_metrics(metrics: Dict[str, float]) -> bool:
    """
    Check if the metrics are a dictionary with string keys and int/float values.

    :param metrics: The metrics to check.
    :return: True if the metrics are a dictionary with string keys and int/float values, False otherwise.
    """
    if isinstance(metrics, dict) and all(isinstance(k, str) for k in metrics.keys()):
        return True
    return False


def check_metric(metric: Tuple) -> bool:
    """
    Check if the metric is a tuple with a string key and an int/float value.

    :param metric: The metric to check.
    :return: True if the metric is a tuple with a string key and an int/float value, False otherwise.
    """
    if (
        isinstance(metric, tuple)
        and len(metric) == 2
        and isinstance(metric[0], str)
        and isinstance(metric[1], (int, float))
    ):
        return True
    return False


def check_params(params: Dict[str, str]) -> bool:
    """
    Check if the params are a dictionary with string keys and string values.

    :param params: The params to check.
    :return: True if the params are a dictionary with string keys and string values, False otherwise.
    """
    if isinstance(params, dict) and all(isinstance(k, str) for k in params.keys()):
        return True
    return False


def check_param(param: Tuple) -> bool:
    """
    Check if the param is a tuple with a string key and a string value.

    :param param: The param to check.
    :return: True if the param is a tuple with a string key and a string value, False otherwise.
    """
    if (
        isinstance(param, tuple)
        and len(param) == 2
        and isinstance(param[0], str)
        and isinstance(param[1], str)
    ):
        return True
    return False


def check_run(run_id: Optional[str] = None, fail: Optional[bool] = False) -> True:
    """
    Check if an active run exists.

    :param run_id: The run_id to check.
    :param fail: If True, raise an exception if no active run is found.
    :return: True if an active run exists, False otherwise.

    """
    run = mlflow.active_run()
    if not run:
        if run_id:
            mlflow.start_run(run_id=run_id)
            return True
        elif fail:
            raise mlflow.exceptions.MlflowException("No active run found.")
        else:
            print("No active run found.")
            return False
    return True


def get_valid_artifact_path_for_modules(artifact_path: str) -> str:
    """
    Get a valid artifact path for a module.

    :param artifact_path: The artifact path.
    :return: A valid artifact path for a module.
    """
    if not isinstance(artifact_path, str):
        raise TypeError("The artifact path must be a string.")

    if not artifact_path.endswith(".py"):
        return artifact_path.replace(".", "/") + ".py"
    return artifact_path


def check_logged_code(run, func) -> bool:
    """
    Check if the code of the function has already been logged.

    :param run: The active run.
    :param func: The function to check.
    :return: True if the code of the function has already been logged, False otherwise.
    """
    module_path = Path(func.__module__.replace(".", "/") + ".py")
    artifacts = mlflow.artifacts.list_artifacts(
        run_id=run.info.run_id, artifact_path=module_path.parent
    )
    if artifacts:
        files = [file.path for file in artifacts]
        if module_path.as_posix() in files:
            return True
    else:
        return False


def append_code(run, func) -> str:
    """
    Append the code of the function to the code of the module.

    :param run: The active run.
    :param func: The function to append.
    :return: The full code of the module.
    """
    module_name = func.__module__
    with tempfile.TemporaryDirectory() as tmpdirname:
        mlflow.artifacts.download_artifacts(
            run_id=run.info.run_id,
            artifact_path=module_name.replace(".", "/") + ".py",
            dst_path=tmpdirname,
        )
        with open(tmpdirname + "/" + module_name.replace(".", "/") + ".py", "r") as f:
            code = f.read()
            func_code = inspect.getsource(func)
            full_code = "\n\n".join([code, func_code])
    return full_code
