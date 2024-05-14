from ralium._util import TypeAlias, Any
from ralium.window import Window
from bs4 import BeautifulSoup

RaliumIDStr: TypeAlias = str
HTMLElementStr: TypeAlias = str

ALL_HTML_ELEMENTS: list[HTMLElementStr]
ALL_HTML_ELEMENT_INSTANCE_METHODS: list[str]
RALIUM_ID_IDENTIFIER_PREFIX: str

def create_ralium_id(tag: dict[str, Any]) -> str: ...
def create_element(
    html: BeautifulSoup, 
    tag: HTMLElementStr, 
    setitems: dict[str] | None = None, 
    **setattrs: dict[str, Any]
) -> None: ...

class JS:
    @staticmethod
    def str(__value: str) -> str: ...

class HTMLElement:
    def __init__(self, window: Window, id: RaliumIDStr, element: HTMLElement = None) -> None: ...
    def __getattr__(self, identifier: str) -> Any: ...
    def __setattr__(self, identifier: str, value: Any) -> None: ...
    def _get_js_element(self) -> str: ...
    def _as_js_str(self) -> str: ...