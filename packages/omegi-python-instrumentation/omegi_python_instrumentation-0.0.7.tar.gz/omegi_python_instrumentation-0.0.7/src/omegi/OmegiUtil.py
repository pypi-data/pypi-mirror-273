import importlib
import inspect
import logging
import os

from .OmegiDecorator import omegi_decorator


def wrap_functions(tracer):
    logging.info("[OMEGIUTIL] wrap_functions: STARTED")
    for module_name in _get_project_modules(_find_project_root()):
        module = importlib.import_module(module_name)
        wrapped_functions = set()
        for name, obj in inspect.getmembers(module):
            if inspect.isfunction(obj) :
                if obj not in wrapped_functions:
                    logging.info(f"[OMEGIUTIL] wrap_functions: INPROGRESS -> wrapped module {module} {name}")
                    decorator = omegi_decorator(tracer)
                    wrapped = decorator(obj)
                    setattr(module, name, wrapped)
                    wrapped_functions.add(obj)


def _find_project_root():
    logging.info("[OMEGIUTIL] _find_project_root: STARTED")
    current_path = os.path.abspath(__file__)
    while True:
        if os.path.exists(os.path.join(current_path, 'requirements.txt')) or os.path.exists(os.path.join(current_path, 'setup.py')):
            return current_path
        parent_path = os.path.dirname(current_path)
        if parent_path == current_path:
            raise Exception("Project root not found.")
        current_path = parent_path
    logging.info(f"[OMEGIUTIL] _find_project_root: ENDED -> {current_path}")
    return current_path


def _get_project_modules(project_root):
    logging.info("[OMEGIUTIL] _get_project_modules: STARTED")
    project_modules = []
    for root, dirs, files in os.walk(project_root):
        for file in files:
            if file.endswith('.py'):
                module_path = os.path.relpath(os.path.join(root, file), project_root)
                module_name = module_path.replace('/', '.').replace('\\', '.')[:-3]
                if not module_path.startswith(".venv") and not module_path.startswith("omegi") and module_name != "omegi.OmegiUtil":
                    project_modules.append(module_name)
    logging.info(f"[OMEGIUTIL] _get_project_modules: ENDED -> {project_modules}")
    return project_modules