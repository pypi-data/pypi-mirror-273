from ml_extra.loggers.decorators.utils import check_run
from ml_extra.loggers.decorators.utils import get_valid_artifact_path_for_modules
from ml_extra.loggers.decorators.utils import check_logged_code
from ml_extra.loggers.decorators.utils import append_code
import inspect
import mlflow

import tempfile
from pathlib import Path
from functools import wraps
from inspect import isfunction


def log_function(artifact_path: str):
    """
    Log the code of the function passed as argument.
    """
    if artifact_path and not isfunction(artifact_path):
        artifact_path = get_valid_artifact_path_for_modules(artifact_path)
    else:
        raise ValueError("artifact_path is required")

    def inner(func):
        """
        Log the code of the function passed as argument.
        """

        @wraps(func)
        def wrapper(*args, **kwargs):
            if not check_run():
                return func(*args, **kwargs)

            code = inspect.getsource(func)
            mlflow.log_text(code, artifact_path)
            return func(*args, **kwargs)

        return wrapper

    return inner


def log_function_path(func):
    """Log the code of the function passed as argument."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        run = mlflow.active_run()
        if run is None:
            raise mlflow.exceptions.MlflowException("No active run found.")

        if check_logged_code(run, func):
            code = append_code(run, func)
        else:
            code = inspect.getsource(func)

        module_name = func.__module__
        mlflow.log_text(code, module_name.replace(".", "/") + ".py")
        return func(*args, **kwargs)

    return wrapper


def log_class(cls):

    orig_init = cls.__init__

    def __init__(self, *args, **kws):
        run = mlflow.active_run()
        if run is None:
            raise mlflow.exceptions.MlflowException("No active run found.")

        if check_logged_code(run, cls):
            code = append_code(run, cls)
        else:
            code = inspect.getsource(cls)

        module_name = cls.__module__
        mlflow.log_text(code, module_name.replace(".", "/") + ".py")
        orig_init(self, *args, **kws)

    cls.__init__ = __init__

    return cls

def log_module_function(func):
    """
    Log the code of the module passed as argument.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        if not check_run():
            return func(*args, **kwargs)

        module = inspect.getmodule(func)
        code = inspect.getsource(module)
        module_name = module.__name__
        mlflow.log_text(code, module_name.replace(".", "/") + ".py")
        return func(*args, **kwargs)

    return wrapper

def log_module_source(module)->None:
    """
    Log the code of the module passed as argument.
    """

    if not check_run():
        return
    code = inspect.getsource(module)
    module_name = inspect.getmodule(module).__name__
    mlflow.log_text(code, module_name.replace(".", "/") + ".py")
