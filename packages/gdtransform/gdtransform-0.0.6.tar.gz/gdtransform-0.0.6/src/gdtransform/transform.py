from typing import Any, Dict

from .constants import GRID_TRANSFORMATION_FLAG, GRID_TRANSFORMATION_NAME


def transformation(name: str):
    if not name:
        raise Exception('invalid transformation name')

    def __transformation(function):
        def wrapper(data: Dict[str, Any]):
            function(data)

        setattr(wrapper, GRID_TRANSFORMATION_FLAG, True)
        setattr(wrapper, GRID_TRANSFORMATION_NAME, name)

        return wrapper

    return __transformation
