import inspect

class _FunctionCallInfo:
    def __init__(self, cls, func, result = None, *args, **kwargs):
        self.cls = cls
        self.func = func
        self.result = result
        self.args = list(args)
        self.kwargs = kwargs
    
    def __repr__(self):
        if self.result:
            return f"FunctionCallInfo(cls={repr(self.cls)}, func={repr(self.func)}, result='{self.result}', args={self.args}, kwargs={self.kwargs})"
        return f"FunctionCallInfo(cls={repr(self.cls)}, func={repr(self.func)}, args={self.args}, kwargs={self.kwargs})"

class ClassListener:
    def __init__(self, cls):
        self.cls = cls
    
    def __call__(self, *args, **kwargs):
        self.cls = self.cls(*args, **kwargs)
        for name, object in inspect.getmembers(self.cls):
            if ((not inspect.isfunction(object) and not inspect.ismethod(object)) or 
                (name.startswith("__") and name.endswith("__"))):
                continue

            setattr(self.cls, name, self.create_listener(object))
        return self.cls
    
    def create_listener(self, function):
        cls = self.cls

        class BroadcastFunction:
            def __init__(self):
                self.__before = {}
                self.__after = {}
            
            def __call__(self, *args, **kwargs):
                info = _FunctionCallInfo(cls, function, None, *args, **kwargs)

                for f in self.__before.values():
                    f(info)

                info.result = function(*info.args, **info.kwargs)

                for f in self.__after.values():
                    f(info)
                
                return info.result
            
            def subscribe(self, function, is_after = False):
                if is_after:
                    self.__after[str(function)] = function
                    return
                self.__before[str(function)] = function
            
            def unsubscribe(self, function, is_after = False):
                if is_after:
                    del self.__after[str(function)]
                    return
                del self.__before[str(function)]
        
        BroadcastFunction.__name__     = function.__name__
        BroadcastFunction.__qualname__ = function.__qualname__

        return BroadcastFunction()