from ralium.webpage import WebHook, WebHookNamespace
from ralium.config import WindowConfig
from ralium.window import Window
from ralium.errors import *
from ralium._util import _get_path, _norm_url

from types import FunctionType, MethodType

import inspect
import os

RALIUM_API_REGISTRY_IDENTIFIER = "__ralium_registry__"
    
def _check_web_folder(webfolder):
    if not os.path.exists(webfolder):
        raise WebFolderNotFoundError("Web folder path does not exist.")
    
    if not os.path.isdir(webfolder):
        raise WebFolderDirectoryError("Web folder must be a directory.")

def _check_web_routes(webroutes):
    if not os.path.exists(webroutes):
        raise WebRoutesNotFoundError("Web folder must contain a routes directory.")
    
    if not os.path.isdir(webroutes):
        raise WebRoutesDirectoryError("Web folder routes must be a directory.")

def _collect_global_css_files(webfolder):
    cssfiles = []
    cssfolder = os.path.join(webfolder, "styles")

    if os.path.exists(cssfolder) and os.path.isdir(cssfolder):
        for root, _, files in os.walk(webfolder):
            cssfiles.extend([os.path.join(root, file) for file in files if os.path.splitext(file)[-1] == ".css"])
    
    return cssfiles

def _get_registry_contents(pyfile):
    with open(pyfile, "r") as f:
        content = f.read()
    
    _globals = {}
    exec(content, _globals)

    return _globals.get(RALIUM_API_REGISTRY_IDENTIFIER, [])

def _collect_webhooks(webfolder, webroutes):
    webhooks = []
    global_css = _collect_global_css_files(webfolder)
    root_split_string = os.path.join(os.path.basename(webfolder), "routes")

    for root, _, files in os.walk(webroutes):
        url = _norm_url(f"{root.split(root_split_string)[-1]}")

        if not files: 
            continue

        css = [*global_css]
        html = None
        functions = []
        namespaces = []

        for file in files:
            file_path = os.path.join(root, file)

            if file == "+page.html":
                html = file_path
                continue
                
            _, ext = os.path.splitext(file)
            if ext == ".css":
                css.append(file_path)
                continue

            if file == "+server.py":
                registry = _get_registry_contents(file_path)

                for item in registry:
                    if isinstance(item, WebHookNamespace):
                        namespaces.append(item)
                        continue
                    
                    if isinstance(item, (FunctionType, MethodType,)):
                        functions.append(item)

        webhooks.append(WebHook(url=url, html=html, css=css, homepage=(url == "/"), functions=functions, namespaces=namespaces))
    
    return webhooks

class Module:
    """
    A container, typically used for module methods, that wraps functions and named functions that don't need a window argument.

    :param functions: A list of functions or methods to wrap.
    :param named_functions: A dictionary of functions with names different from their current ones to wrap.
    """

    # Flag attribute used by the 'WebHookNamespace' class.
    _module_api_class = True
    
    def __init__(self, *functions, **named_functions):
        self.functions = [wrap(function) for function in functions]
        self.named_functions = {name: wrap(function) for name, function in named_functions.items()}

def create_window(webfolder, config = None):
    """
    Creates a window from a specific directory structure.

    :param webfolder: The project directory.
    :param config: The window configuration.

    :returns: A `Window` object.

    :raises WebFolderNotFoundError: If the webfolder path doesn't exist.
    :raises WebFolderDirectoryError: If the webfolder path is not a directory.
    :raises WebRoutesNotFoundError: If the `webfolder` directory doesn't contain a `routes` directory.
    :raises WebRoutesDirectoryError: If `{webfolder}/routes` is not a directory.
    """

    webfolder = _get_path(webfolder)
    webroutes = os.path.join(webfolder, "routes")

    _check_web_folder(webfolder)
    _check_web_routes(webfolder)

    webhooks = _collect_webhooks(webfolder, webroutes)

    return Window(webhooks, config or WindowConfig())

def register():
    """
    Creates a registry list to expose functions and namespaces for use within JavaScript.

    :returns: A decorator for exposing Python functions to JavaScript.
    """

    globals = inspect.currentframe().f_back.f_globals
    globals[RALIUM_API_REGISTRY_IDENTIFIER] = []

    def wrapper(function):
        if not inspect.isfunction(function):
            raise WebFunctionApiError("WebFunction wrapper must be used on a function.")

        if function not in globals[RALIUM_API_REGISTRY_IDENTIFIER]:
            globals[RALIUM_API_REGISTRY_IDENTIFIER].append(function)

    return wrapper

def namespace(name, *functions, **named_functions):
    """
    Adds a namespace to the registry.

    :param name: An alias for referencing the namespace.
    :param functions: A list of functions or methods to register under the namespace.
    :param named_functions: A dictionary of functions with names different from their current ones to add to the namespace.
    """

    registry = inspect.currentframe().f_back.f_globals.get(RALIUM_API_REGISTRY_IDENTIFIER)

    if registry is None:
        raise RegistryNotFoundError(
            "No active registry found in the global space.",
            "Ensure that 'ralium.api.register' has been called to initialize the registry.",
            "('ralium.api.register' must be called at the top-level of the stack)"
        )
    
    registry.append(WebHookNamespace(name, *functions, **named_functions))

def wrap(function):
    """
    Wraps a function to accept a 'window' argument, typically for module methods.

    :param function: A function or method.

    :returns: A decorator for the wrapped function.
    """

    def wrapper(_, *args, **kwargs):
        return function(*args, **kwargs)
    
    wrapper.__name__     = function.__name__
    wrapper.__qualname__ = function.__qualname__
    
    return wrapper