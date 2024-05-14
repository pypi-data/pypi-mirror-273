from types import NoneType

class WindowConfig:
    """
    A Window Configuration Object.

    :param title: The Window Title.
    :param icon: The Window Icon.
    :param size: The Window Size.
    :param min_size: The minimum size the Window can be.
    :param resizable: If the window can be resized.
    :param builtins: Add builtin functions to the JavaScript function space.
    :param kwargs: Extra arguments for the `pywebview.create_window` function.

    :raises TypeError: If a specific config option has an invalid value type.
    """

    def __init__(self,
        title = None,
        icon = None,
        size = (900, 600), 
        min_size = (300, 300), 
        child_window = False, 
        resizable = True,
        builtins = True,
        **kwargs
    ):
        self.icon = icon
        self.size = size
        self.title = title
        self.min_size = min_size
        self.use_builtins = builtins
        self.is_resizable = resizable
        self.is_child_window = child_window
        self.other_options = kwargs

        if not isinstance(title, (str, NoneType)):
            raise TypeError(f"Expected the title to be a string, instead got '{type(title)}'")
        
        if not isinstance(size, tuple):
            raise TypeError(f"Expected the window size to be a tuple, instead got '{type(size)}'")
        
        if len(size) != 2:
            raise TypeError(f"Invalid size, expected just width and height.")
        
        if not isinstance(min_size, tuple):
            raise TypeError(f"Expected the minimum window size to be a tuple, instead got '{type(min_size)}'")
        
        if len(min_size) != 2:
            raise TypeError(f"Invalid minimum size, expected just width and height.")

        self.width, self.height = size
        self.min_width, self.min_height = min_size

        if not isinstance(self.width, int):
            raise TypeError(f"Expected the window width to be an int, instead got '{type(self.width)}'")
        
        if not isinstance(self.height, int):
            raise TypeError(f"Expected the window height to be an int, instead got '{type(self.height)}'")
        
        if not isinstance(self.min_width, int):
            raise TypeError(f"Expected the minimum window width to be an int, instead got '{type(self.min_width)}'")
        
        if not isinstance(self.min_height, int):
            raise TypeError(f"Expected the minimum window height to be an int, instead got '{type(self.min_height)}'")
        
        if not isinstance(self.is_child_window, bool):
            raise TypeError(f"Expected a boolean for argument 'child_window', instead got '{type(self.child_window)}'")
        
        if not isinstance(self.is_resizable, bool):
            raise TypeError(f"Expected a boolean for argument 'resizable', instead got '{type(self.child_window)}'")
    
    def as_webview_kwargs(self):
        """
        A helper function for converting the configuration options to a dict for `pywebview.create_window` function.
        """

        return {
            "title": self.title,
            "width": self.width,
            "height": self.height,
            "min_size": self.min_size,
            "resizable": self.is_resizable
        }