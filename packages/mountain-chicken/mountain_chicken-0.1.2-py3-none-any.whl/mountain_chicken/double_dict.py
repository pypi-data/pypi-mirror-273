from typing import Any


class double_dict:
    def __init__(self, d: dict, **kwargs) -> None:
        self._d = d
        self._rev_d = {key : value for value,key in self._d.items()}
        if "default" in kwargs:
            self.default = kwargs["default"]
        else:
            self.default = False

    def __getitem__(self, name: any) -> Any:
        if name in self._d:
            return self._d[name] 
        
        elif name in self._rev_d:
            return self._rev_d[name]
        
        elif self.default:
            return self.default
        
        else: raise KeyError(name)
    
    def __setitem__(self, name: any, value: any) -> None:
        self._d[name] = value
        self._rev_d[value] = name

    def __str__(self) -> str:
        return str(self._d)
    
    def __delitem__(self, name: any) -> None:
        del self._rev_d[self._d[name]]
        del self._d[name]
    


