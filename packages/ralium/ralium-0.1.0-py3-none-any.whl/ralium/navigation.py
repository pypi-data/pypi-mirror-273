class WindowNavigation:
    """
    The Window Navigation Manager.

    :param current_url: The url to initially display.
    """

    def __init__(self, current_url = "/"):
        self.__homepage = None
        self.__previous = None
        self.__location = current_url

    def setdefault(self, url):
        """Sets the homepage."""
        self.__homepage = url
    
    @property
    def homepage(self):
        return self.__homepage

    @property
    def previous(self):
        return self.__previous

    @property
    def location(self):
        return self.__location

    @location.setter
    def location(self, new_url):
        self.__previous = None
        self.__location = new_url