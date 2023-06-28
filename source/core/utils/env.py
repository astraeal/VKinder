import os


def get_missing_env_vars(variables: list[str]) -> list[str]:
    missing_vars = list()
    for var in variables:
        if os.getenv(var) is None:
            missing_vars.append(var)
    return missing_vars
