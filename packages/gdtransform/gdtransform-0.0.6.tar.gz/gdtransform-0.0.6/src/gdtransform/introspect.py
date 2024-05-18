from inspect import getmembers, isfunction

from .constants import GRID_TRANSFORMATION_FLAG, GRID_TRANSFORMATION_NAME


def is_valid_transformation(function, name):
    return hasattr(function, GRID_TRANSFORMATION_FLAG) and \
        hasattr(function, GRID_TRANSFORMATION_NAME) and \
        getattr(function, GRID_TRANSFORMATION_FLAG) and \
        getattr(function, GRID_TRANSFORMATION_NAME) == name


def get_module_transformation(module, name: str):
    members = getmembers(module, isfunction)
    if not members:
        return None
    for (_, member_func) in members:
        if is_valid_transformation(member_func, name):
            return member_func

    return None
