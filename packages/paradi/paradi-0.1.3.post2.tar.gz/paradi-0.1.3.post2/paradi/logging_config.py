import logging

# Create logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Add handlers to logger
logger.addHandler(logging.NullHandler())


def log_errors(f):
    """
    intercepts the error output to redirect it in a log file via a wrapped function

    :param f: The function to be decorated
    :return: A function that wraps the function f.
    """
    def inner(*args, **kwargs):
        try:
            res = f(*args, **kwargs)
        except Exception as e:
            logger.error(f"The following exception occurred while executing {f.__module__}.{f.__qualname__}")
            logger.error(f'{e.__class__.__name__} : {e}')
        else:
            return res
    return inner
