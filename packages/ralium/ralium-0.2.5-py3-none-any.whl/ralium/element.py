import uuid

ALL_HTML_ELEMENTS = [
    "a", "abbr", "acronym", "address", "area", "article", "aside", "audio", "b", "base",
    "bdi", "bdo", "big", "blockquote", "body", "br", "button", "canvas", "caption", "center",
    "cite", "code", "col", "colgroup", "data", "datalist", "dd", "del", "details", "dfn", "dialog",
    "dir", "div", "dl", "dt", "em", "embed", "fencedframe", "fieldset", "figcaption", "figure",
    "font", "footer", "form", "frame", "frameset", "h1", "head", "header", "hgroup", "hr", "html",
    "i", "iframe", "img", "input", "ins", "kbd", "label", "legend", "li", "link", "main", "map",
    "mark", "marquee", "menu", "menuitem", "meta", "meter", "nav", "nobr", "noembed", "noframes",
    "noscript", "object", "ol", "optgroup", "option", "output", "p", "param", "picture", "plaintext",
    "portal", "pre", "progress", "q", "rb", "rp", "rt", "rtc", "ruby", "s", "samp", "script", "search",
    "section", "select", "slot", "small", "source", "span", "strike", "strong", "style", "sub", "summary",
    "sup", "table", "tbody", "td", "template", "textarea", "tfoot", "th", "thead", "time", "title", "tr",
    "track", "tt", "u", "ul", "var", "video", "wbr", "xmp"
]

ALL_HTML_ELEMENT_INSTANCE_METHODS = [
    "after", "animate", "append", "attachShadow", "before", "checkVisibility", "closest",
    "computedStyleMap", "getAnimations", "getAttribute", "getAttributeNames", "getAttributeNode",
    "getAttributeNodeNS", "getAttributeNS", "getBoundingClientRect", "getClientRects",
    "getElementsByClassName", "getElementsByTagName", "getElementsByTagNameNS", "getHTML",
    "hasAttribute", "hasAttributeNS", "hasAttributes", "hasPointerCapture", "insertAdjacentElement",
    "insertAdjacentHTML", "insertAdjacentText", "matches", "prepend", "querySelector",
    "querySelectorAll", "releasePointerCapture", "remove", "removeAttribute", "removeAttributeNode",
    "removeAttributeNS", "replaceChildren", "replaceWith", "requestFullscreen", "requestPointerLock",
    "scroll", "scrollBy", "scrollIntoView", "scrollIntoViewIfNeeded", "scrollTo", "setAttribute",
    "setAttributeNode", "setAttributeNodeNS", "setAttributeNS", "setCapture", "setHTML",
    "setPointerCapture", "toggleAttribute"
]

RALIUM_ID_IDENTIFIER_PREFIX = "ralium-"

def create_ralium_id(tag):
    ralium_id = f"{RALIUM_ID_IDENTIFIER_PREFIX}{uuid.uuid1()}"

    tag['class'] = f"{ralium_id} {' '.join(tag.get('class', []))}".strip()

    return ralium_id

def create_element(html, tag, setitems = None, **setattrs):
    element = html.new_tag(tag)
    setitems = setitems or {}

    if not isinstance(setitems, dict):
        raise TypeError(f"Expected argument 'setitems' to be of type str, instead got '{type(setitems)}'")

    for name, value in setattrs.items():
        setattr(element, name, value)
    
    for name, value in setitems.items():
        element[name] = value
    
    html.body.append(element)

class JS:
    @staticmethod
    def str(__value):
        return f'"{__value}"'
    
    true = str("true")
    false = str("false")

    @staticmethod
    def bool(__value):
        if __value == "true":
            return True

        if __value == "false":
            return False

    class ClassList(list):
        def __init__(self, element):
            self.element = element
            super().__init__(str(element._eval(f"{element._as_js_str()}.classList")).split(' '))
        
        def add(self, classname):
            if classname in self:
                return

            super().append(classname)
            self.element._eval(f'{self.element._as_js_str()}.classList.add("{classname}")')
        
        def remove(self, classname):
            if classname not in self:
                return
            
            super().remove(classname)
            self.element._eval(f'{self.element._as_js_str()}.classList.remove("{classname}")')
    
HTMLElementAttributes = [
    "_ralium_id", 
    "_ralium_window", 
    "_ralium_element",
    "classList"
]

class HTMLElement:
    def __init__(self, window, id, element = None):
        self._ralium_id = id
        self._ralium_window = window
        self._ralium_element = element
        self.classList = JS.ClassList(self)

        if RALIUM_ID_IDENTIFIER_PREFIX in self._ralium_id or not id:
            return

        classes = str(self._eval(f""" '' + document.getElementById("{id}").classList;""")).split(' ')

        if RALIUM_ID_IDENTIFIER_PREFIX in classes[0]:
            self._ralium_id = classes[0]
            return

        for classname in classes:
            if RALIUM_ID_IDENTIFIER_PREFIX in classname:
                self._ralium_id = classname
        
    def __getattr__(self, identifier):
        if identifier in ALL_HTML_ELEMENT_INSTANCE_METHODS:
            def wrapper(*args, **kwargs):
                _prepare = lambda v: (str(v), f'"{v}"')[isinstance(v, str)]
                args_str = [_prepare(arg) for arg in args]
                args_str.extend([f'{_prepare(key)}={_prepare(value)}' for key, value in kwargs.items()])
                args_str = ",".join(args_str)

                return self._eval(f"{self._as_js_str()}.{identifier}({args_str})")
            
            wrapper.__name__     = identifier
            wrapper.__qualname__ = f"HTMLElement.{identifier}"

            return wrapper

        return self._parse(self._eval(f"{self._as_js_str()}.{identifier}"))
    
    def __setattr__(self, identifier, value):
        if identifier in HTMLElementAttributes:
            return object.__setattr__(self, identifier, value)

        self._eval(f"{self._get_js_element()}.{identifier} = {value};")
    
    def _get_js_element(self):
        return f"document.getElementsByClassName('{self._ralium_id}')[0]"
    
    def _as_js_str(self):
        return f"'' + {self._get_js_element()}"
    
    def _eval(self, cmd):
        return self._ralium_window.webview.evaluate_js(cmd)
    
    def _parse(self, value):
        if value in ["true", "false"]:
            return JS.bool(value)
        return value