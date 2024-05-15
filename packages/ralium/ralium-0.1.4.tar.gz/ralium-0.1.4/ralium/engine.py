from ralium.webpage import WebHookNamespace
from ralium.element import HTMLElement
from ralium.errors import BridgeEventError
from ralium import _util

from bs4 import BeautifulSoup

import socketserver
import threading
import inspect
import os

def _process_api_calldata(window, calldata):
    webhook = window.webhooks.get(window.navigation.location)
    new_calldata = []

    for data in calldata:
        if isinstance(data, dict):
            element_id = data.get("className", None)
            local_name = data.get("localName", None)

            if element_id is None or local_name is None or element_id not in webhook.elements: 
                continue

            soup = BeautifulSoup(window.webview.html, "html.parser")
            element = soup.find(local_name, {"class": element_id})

            new_calldata.append(HTMLElement(window, element_id, element))
            continue

        new_calldata.append(data)
    
    return new_calldata

class WebBridge:
    def __init__(self, *functions):
        self.bridges = []
        self.initial = "function bridge(func) {pywebview.api.bridge(func)};"

        for function in functions:
            self.new(function)
        
        self.clear = self.bridges.clear
    
    def __str__(self):
        return self.initial + "".join(self.bridges)
    
    def _function_template(self, name, string):
        return f"function {name}(...calldata){{return pywebview.api.bridge(\"{string}\", calldata)}}"

    def _namespace_template(self, alias, *functions, **named_functions):
        functions = [
            f'{function.__name__}: {self._function_template("", str(function))}'
            for function in functions
        ]

        functions.extend([
            f'{alias}: {self._function_template("", str(function))}'
            for alias, function in named_functions.items()
        ])

        return f"let {alias} = {{{','.join(functions)}}}"

    def new(self, obj):
        if inspect.isfunction(obj) or inspect.ismethod(obj):
            return self.bridges.append(self._function_template(obj.__name__, str(obj)))
        
        if isinstance(obj, WebHookNamespace):
            return self.bridges.append(self._namespace_template(obj.name, **dict(obj.items())))
    
class WebApiFunctionDict(dict):
    def add_function(self, function):
        self[str(function)] = function
    
class WebEngine:
    def __init__(self, window):
        self.port, worker = self._init_server()
        
        self.server = threading.Thread(target=worker, daemon=True)
        self.__running = threading.Event()

        self.event = self.create_event()
        self.bridge = WebBridge()
        self.functions = WebApiFunctionDict()

        # Strictly for the 'WebApi' class created by 'WebEngine.create_api'
        self._window = window

        self.start = self.server.start
    
    def __str__(self):
        return f"http://localhost:{self.port}/"

    @property
    def running(self):
        return not self.__running.is_set()

    def _init_server(self):
        httpd = socketserver.TCPServer(("", 0,), _util.BasicHTTPServer)
        port = httpd.socket.getsockname()[1]

        def worker():
            while self.running:
                httpd.handle_request()
            os._exit(0)
        
        return port, worker
    
    def close(self):
        self.__running.set()
        self.server.join(timeout=5)
    
    def create_api(engine):
        class WebApi:
            def __init__(self):
                return

            def bridge(self, func, calldata=None):
                if not engine.functions.get(func, False): return

                calldata = _process_api_calldata(engine._window, calldata)

                if calldata:
                    return engine.functions[func](*calldata)
                
                return engine.functions[func]()
        
        return WebApi()
    
    def create_event(self):
        def BridgeEvent(function):
            if callable(function):
                if not str(function) in self.functions:
                    self.functions.add_function(function)
                return f"bridge('{str(function)}')"
            raise BridgeEventError("Event attribute is not a function.")
        return BridgeEvent
    