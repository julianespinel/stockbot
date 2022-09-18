import os


def get_or_throw(variable_name: str) -> str:
    value = os.environ.get(variable_name)
    if not value:
        raise ValueError(f'{variable_name} environment variable is not defined')
    return value
