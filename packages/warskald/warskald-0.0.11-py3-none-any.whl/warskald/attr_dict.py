class AttrDict(dict):
    def __init__(self, *args, **kwargs):
        #self.dict = dict(*args, **kwargs)
        super().__init__(*args, **kwargs)
        for key, value in self.items():
            if isinstance(value, dict):
                self[key] = AttrDict(value)

    def __getitem__(self, key):
        #return self.dict.get(key, default)
        value = None
        try:
            value = super().__getitem__(key)
        except KeyError:
            try:
                value = super().__getattribute__(key)
            except AttributeError:
                pass
        return value

    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        super().__setattr__(key, value)

    def __getattr__(self, attr):
        value = None
        try:
            super().__getattribute__(attr)
        except AttributeError:
            try:
                value = super().__getitem__(attr)
            except KeyError:
                pass
        return value
    
    def __setattr__(self, attr, value):
        super().__setattr__(attr, value)
        super().__setitem__(attr, value)
        
    def get(self, key, default=None):
        return super().get(key, default)