from typing import Any

class WindowConfig:
    def __init__(self,
        title: str | None = None,
        icon: str | None = None,
        size: tuple[int, int] = (900, 600), 
        min_size: tuple[int, int] = (300, 300), 
        child_window: bool = False, 
        resizable: bool = True,
        encoding: str = "UTF-8",
        builtins: bool = True,
        **kwargs
    ) -> None: ...

    def as_webview_kwargs(self) -> dict[str, Any]: ...