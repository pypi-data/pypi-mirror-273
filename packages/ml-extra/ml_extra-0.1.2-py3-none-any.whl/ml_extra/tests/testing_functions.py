from ml_extra.loggers.decorators.code import log_function_path
from ml_extra.loggers.decorators.code import log_module_function
from ml_extra.loggers.decorators.code import log_function

@log_function("custom_functions/do_something")
def do_something():
    """Does something."""
    return 42


@log_module_function
def do_something_else():
    """Does something else."""
    return 42
