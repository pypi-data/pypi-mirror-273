from ralium.navigation import WindowNavigation
from ralium.element import create_element, create_ralium_id
from ralium.webpage import WebHookDict, HTML_TEMPLATE
from ralium.errors import WebHookHomepageError
from ralium.config import WindowConfig
from ralium.engine import WebEngine
import ralium.builtins

from bs4 import BeautifulSoup

import webview

class Window:
    """
    Represents a Ralium GUI Window.

    :param webhooks: A list of WebHooks that handle each URL.
    :param config: Optional configuration for the window.

    :raises WebHookHompageError: If more than one WebHook has the homepage option set to `True`.
    """

    def __init__(self, webhooks, config = None):
        self.config = config or WindowConfig()
        self.engine = WebEngine(self)
        self.running = False
        self.webhooks = WebHookDict(webhooks)
        self.navigation = WindowNavigation()

        self.webview = webview.create_window(
            html=HTML_TEMPLATE,
            hidden=True,
            js_api=self.engine.create_api(),
            **self.config.as_webview_kwargs(),
            **self.config.other_options
        )

        for webhook in webhooks:
            if webhook.homepage:
                if self.navigation.homepage is not None:
                    raise WebHookHomepageError(f"A WebHook homepage already exists for the url '{self.navigation.homepage}'")
                self.navigation.setdefault(webhook.url)
            
            if self.config.use_builtins:
                webhook.functions.extend(ralium.builtins.__registry__)

            webhook.set_window(self)
            webhook._wrap_functions()
            webhook._wrap_namespaces()
        
        self.engine.start()
    
    def load_handler(self, window):
        def on_load():
            window.show()
            window.events.loaded -= on_load

        window.events.loaded += on_load
        
    def display(self, url):
        """
        Displays a URL by calling the WebHook attached to the URL.

        :param url: The URL to display.
        """

        self.navigation.location = url
        webhook = self.webhooks.get(self.navigation.location)

        self.engine.bridge.clear()
        self.engine.functions.clear()

        for function in webhook.functions:
            self.engine.bridge.new(function)
            self.engine.functions.add_function(function)
        
        for namespace in webhook.namespaces:
            self.engine.bridge.new(namespace)

            for function in namespace.values():
                self.engine.functions.add_function(function)
        
        html = BeautifulSoup(webhook.html, features="lxml")
        webhook.elements = [create_ralium_id(element) for element in html.body.find_all()]

        create_element(html, "base", {"href": str(self.engine)})
        create_element(html, "script", string=str(self.engine.bridge))
        create_element(html, "style", string=webhook.css)

        if self.running:
            return self.webview.evaluate_js(f"document.open();document.write(`{str(html)}`);document.close();") and None
        
        self.webview.html = str(html)
    
    def start(self):
        """Starts the Ralium Window and officially displays the GUI."""
        if self.running: return
        
        self.running = True
        webview.start(self.load_handler, self.webview, private_mode=False)
    
    def show(self):
        """Show a Ralium Window."""
        self.webview.show()
    
    def hide(self):
        """Hide a Ralium Window."""
        self.webview.hide()
    
    def shutdown(self):
        """Shutdown a Ralium Window."""
        self.webview.destroy()
        self.engine.close()