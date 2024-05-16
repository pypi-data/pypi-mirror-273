import inspect

class SubscriptionService:
    def __init__(self):
        self.before = {}
        self.after = {}
    
    def subscribe(self, function, after = False):
        getattr(self, ("before", "after")[after])[function.__name__] = function
    
    def unsubscribe(self, function, after = False):
        del getattr(self, ("before", "after")[after])[function.__name__]

class FunctionCallInfo:
    def __init__(self, cls, function, result = None, *args, **kwargs):
        self.parent = cls
        self.function = function
        self.result = result
        self.args = args
        self.kwargs = kwargs

class ClassListener:
    def __init__(self, cls):
        self.cls = cls
        self.members = inspect.getmembers(cls)

        for name, object in self.members:
            if not inspect.isfunction(object) or (name.startswith("__") and name.endswith("__")):
                continue

            self.listen(name, object)
    
    def __call__(self, *args, **kwargs):
        return self.cls(*args, **kwargs)
    
    def listen(this, name, function):
        class BroadcastFunction:
            def __init__(self):
                self.function = function
                self.subscriptions = SubscriptionService()

                self.subscribe = self.subscriptions.subscribe
                self.unsubscribe = self.subscriptions.unsubscribe
            
            def __call__(self, *args, **kwargs):
                for f in self.subscriptions.before.values():
                    f(FunctionCallInfo(cls=this.cls, function=self.function, *args, **kwargs))
                
                result = self.function(this.cls, *args, **kwargs)

                for f in self.subscriptions.after.values():
                    f(FunctionCallInfo(cls=this.cls, function=self.function, result=result, *args, **kwargs))
                
                return result
            
        BroadcastFunction.__name__     = function.__name__
        BroadcastFunction.__qualname__ = function.__qualname__
        
        setattr(this.cls, name, BroadcastFunction())