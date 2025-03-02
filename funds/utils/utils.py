import time
import logging
from functools import wraps

logger = logging.getLogger("funds")  

def log_execution_time(func):
    """Decorator to log the execution time of API views."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        response = func(*args, **kwargs)
        elapsed_time = time.time() - start_time

        if len(args) > 1:
            request = args[1]
        else:
            request = args[0]

        logger.info(f"⏳ {func.__name__}: {request.method} {request.path} took {elapsed_time:.4f} seconds")

        return response

    return wrapper
