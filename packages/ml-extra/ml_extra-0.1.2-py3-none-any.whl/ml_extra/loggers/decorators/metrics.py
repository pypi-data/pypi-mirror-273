import mlflow
from ml_extra.loggers.decorators.utils import check_metric
from ml_extra.loggers.decorators.utils import check_metrics
from ml_extra.loggers.decorators.utils import check_param
from ml_extra.loggers.decorators.utils import check_params
from ml_extra.loggers.decorators.utils import check_run

from functools import wraps


def metric(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        if not check_run():
            return func(*args, **kwargs)

        result = func(*args, **kwargs)

        if check_metrics(result):
            mlflow.log_metrics(result)

        elif check_metric(result):
            mlflow.log_metric(key=result[0], value=result[1])
        else:
            raise Exception("Invalid metric format.")

        return result

    return wrapper


def param(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        if not check_run():
            return func(*args, **kwargs)

        result = func(*args, **kwargs)

        if check_params(result):
            mlflow.log_params(result)

        elif check_param(result):
            mlflow.log_param(key=result[0], value=result[1])
        else:
            raise Exception("Invalid param format.")

        return result

    return wrapper
