import importlib
import inspect
import pkgutil
from typing import Optional

from solidipes.utils import logging

print = logging.invalidPrint
logger = logging.getLogger()


def get_subclasses_from_package(
    package,
    BaseClass: type,
    base_class_module_name: str,
) -> list[type]:
    """Get all subclasses of a base class in a package"""

    module_names = [
        module.name
        for module in pkgutil.iter_modules(package.__path__)
        if module.name != base_class_module_name and module.ispkg is False  # Skip the base abstract class
    ]

    modules = [importlib.import_module(f"{package.__name__}.{module_name}") for module_name in module_names]
    subclasses = [get_subclass_from_module(module, BaseClass) for module in modules]
    subclasses = [S for S in subclasses if S is not None]

    return subclasses


def get_subclass_from_module(module, BaseClass: type) -> Optional[type]:
    for name, obj in inspect.getmembers(module):
        if inspect.isclass(obj) and issubclass(obj, BaseClass) and obj != BaseClass:
            return obj

    logger.debug(f"Could not find subclass of {BaseClass.__name__} in module {module}")
    return None
