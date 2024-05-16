import warnings


def deprecation_warning(message):
    def decorator(func):
        def wrapper(*args, **kwargs):
            # Issue a deprecation warning with the provided message
            warnings.warn(message, category=DeprecationWarning, stacklevel=2)
            # Call the original function
            return func(*args, **kwargs)

        return wrapper

    return decorator


def behavior_change_warning(message):
    def decorator(func):
        def wrapper(*args, **kwargs):
            # Issue a FutureWarning about the change in behavior
            warnings.warn(message, category=FutureWarning, stacklevel=2)
            # Call the original function
            return func(*args, **kwargs)

        return wrapper

    return decorator
