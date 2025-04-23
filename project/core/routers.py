import importlib.util
import os
from importlib.machinery import ModuleSpec
from pathlib import Path

from fastapi import APIRouter, FastAPI

from project.config.base import settings

logger = settings.LOGGER.getChild(__name__)


def register_routers(app: FastAPI) -> None:
    """Basic function for bypassing modules and registering routers"""
    logger.debug("Router registration")
    modules_directory = str(Path(__file__).parent.parent / "modules")
    for root, _dirs, files in os.walk(modules_directory):
        for file in files:
            if file.endswith(".py"):
                module_path = Path(root) / file
                module_name = Path(file).stem

                spec = importlib.util.spec_from_file_location(module_name, module_path)
                if spec is not None:
                    module = load_module(spec)
                    if module is not None:
                        register_module_routers(app, module)
                    else:
                        logger.error(f"Failed to load module {module_name} from {module_path}")
                else:
                    logger.error(f"Failed to find a specification for module {module_name} from {module_path}")


def load_module(spec: ModuleSpec) -> object | None:
    """Loading and executing the module"""
    if spec.loader is not None:
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    return None


def register_module_routers(app: FastAPI, module: object) -> None:
    """Registration of routers found in the module"""
    for item_name in dir(module):
        item = getattr(module, item_name)
        if isinstance(item, APIRouter):
            app.include_router(item)
