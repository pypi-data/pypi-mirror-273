from ralium.element import JS

__registry__ = []

def _builtin(function):
    if function not in __registry__:
        __registry__.append(function)
    
    def wrapper(*args, **kwargs):
        return function(*args, **kwargs)
    
    return wrapper

@_builtin
def redirect(window, url):
    window.display(url)

@_builtin
def shutdown(window):
    window.shutdown()

@_builtin
def get_window_port(window, element = None):
    element.innerHTML = window.engine.port
    return window.engine.port

@_builtin
def get_window_path(window, element = None):
    element.innerHTML = JS.str(window.navigation.location)
    return window.navigation.location