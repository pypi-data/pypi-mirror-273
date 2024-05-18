from typing import Any, Dict


def transformation(name: str):
    def __transformation(function):
        def wrapper(data: Dict[str, Any]):
            function(data)

        wrapper.__gd_transformation__ = True
        wrapper.__gd_transformation_name__ = name

        return wrapper

    return __transformation
