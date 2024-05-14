from ml_extra.experiments.utils import get_or_create_experiment
from ml_extra.loggers.decorators.metrics import metric
from ml_extra.loggers.decorators.code import log_function
from ml_extra.loggers.decorators.code import log_function_path
from ml_extra.loggers.decorators.code import log_module_source
from ml_extra.tests.testing_functions import do_something
from ml_extra.tests.testing_functions import do_something_else
from ml_extra.tests.inner_test.dummy_module import do_something as ds
from ml_extra.tests.inner_test.dummy_module import dummy_function
from ml_extra.tests.testing_classes import DummyClass
from ml_extra.tests.testing_classes import DummyClass2
from ml_extra.tests.inner_test.dummy_module import AnotherClass
from ml_extra.tests.inner_test import dummy_module
import mlflow
from ml_extra.loggers.decorators import code
import inspect
from typing import Optional
import time
import os
import sys
from mlflow.pyfunc import PythonModel


@metric
@log_function("custom_code/calculate_metrics.py")
def calculate_metrics():
    return {"custom_metric": 1.0}


@log_function_path
def testing_function(a: int, b: int):
    result = a + b
    return result


# class DummyModel(PythonModel):

#     def __init__(self, run_id=None):
#         self.run_id = run_id

#     def predict(self, context, model_input):
#         return model_input

#     def load_context(self, context):
#         print(self.run_id)
#         print("CONTEXT: ", context)
#         print(context.model_config)

# run_id = context.model_config["run_id"]
# self.__add_code_to_sys_path(run_id)
# from mlflow_extra.tests.inner_test.dummy_module import say_something
# say_something()


# def __add_code_to_sys_path(self, run_id:str):
#     # download artifacts
#     os.makedirs("custom_code", exist_ok=True)
#     print("downloading artifacts from run_id: ", run_id)
#     dst = mlflow.artifacts.download_artifacts(run_id=run_id, artifact_path="custom_code", dst_path="custom_code")

#     # add custom code to sys.path
#     print("Adding code to sys.path: ", dst)
#     sys.path.append(os.path.abspath(dst))


def log_module_code_with_mlflow(module, run_id: Optional[str] = None):
    code = inspect.getsource(module)
    module_name = inspect.getmodule(module).__name__

    if mlflow.active_run():
        mlflow.log_text(code, "custom_code/" + module_name.replace(".", "/") + ".py")
    elif run_id:
        with mlflow.start_run(run_id=run_id):
            mlflow.log_text(
                code, "custom_code/" + module_name.replace(".", "/") + ".py"
            )
    else:
        raise Exception("No active run found and no run_id provided.")


def main2():
    client = mlflow.MlflowClient()
    model_uri = "models:/dummy_model/latest"
    loaded_model = mlflow.pyfunc.load_model(model_uri)
    print(loaded_model.predict("Input"))
    # print(loaded_model.predict("Hello"))
    # print(loaded_model)
    # registered_model = client.get_registered_model("dummy_model")
    # print(registered_model)
    # run_id = registered_model.latest_versions[0].run_id
    # # download artifacts
    # os.makedirs("custom_code", exist_ok=True)
    # dst = mlflow.artifacts.download_artifacts(run_id=run_id, artifact_path="custom_code", dst_path="custom_code")
    # print(dst)
    # # add custom code to sys.path
    # sys.path.append(os.path.abspath(dst))
    # from mlflow_extra.tests.inner_test.dummy_module import do_something as ds


def main():
    # print(inspect.getabsfile(dummy_module))
    # print(inspect.getsourcefile(dummy_module))
    # print(inspect.getmodule(dummy_module).__name__)
    experiment = get_or_create_experiment(name="example_experiment")
    # print(inspect.getsource(dummy_module))

    # print(help(calculate_metrics))
    # print(calculate_metrics.__name__)
    # print(calculate_metrics.__module__)
    # str1 = inspect.getsource(get_or_create_experiment)
    # str2 = inspect.getsource(log_code)
    # total = "\n \n".join([str1,str2])

    # print(total)
    # print(type(inspect.getsource(get_or_create_experiment)))

    with mlflow.start_run(experiment_id=experiment.experiment_id) as run:
        custom_metric = calculate_metrics()
        result = testing_function(1, 2)
        print(result)
        my_class = DummyClass()
        my_class.say_something("Hello")

        my_class2 = DummyClass2()
        my_class2.say_something("Hello")

    #     another_class = AnotherClass()
    #     another_class.say_something("Hello")
    #     calculate_metrics()
    #     testing_function(1, 2)
        do_something()
        do_something_else()
        log_module_source(code)

    #     ds()
    #     dummy_function()
