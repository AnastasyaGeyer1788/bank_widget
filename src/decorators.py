import functools
from datetime import datetime


def log(filename=None):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Добавляем запись аргументов в лог
            log_entry = f"{func.__name__} called at {datetime.now()}\n" f"Args: {args}, Kwargs: {kwargs}\n"

            try:
                result = func(*args, **kwargs)
                success_msg = f"{func.__name__} ok\n"
                if filename:
                    with open(filename, "a") as f:
                        f.write(log_entry + success_msg)
                else:
                    print(log_entry + success_msg, end="")
                return result
            except Exception as e:
                error_msg = f"{func.__name__} error: {type(e).__name__}\n"
                if filename:
                    with open(filename, "a") as f:
                        f.write(log_entry + error_msg)
                else:
                    print(log_entry + error_msg, end="")
                raise

        return wrapper

    return decorator
