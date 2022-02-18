from __future__ import annotations


class ObjectPromise:
    def __init__(self):
        self._solved = False
        self._solution = None
        self._actions: list[AttributePromise] = []

    def __getattribute__(self, item: str):
        return ObjectPromise.__get(self, item)

    def __setattr__(self, key, value):
        if key.startswith("_") or key == "solve":
            return super(ObjectPromise, self).__setattr__(key, value)
        if self._solved:
            return setattr(self._solution, key, value)
        return self._get_attr_promise(key, 1, value)

    def __delattr__(self, item):
        if item.startswith("_") or item == "solve":
            return super(ObjectPromise, self).__delattr__(item)
        if self._solved:
            return delattr(self._solution, item)
        return self._get_attr_promise(item, 2)

    def __call__(self, *args, **kwargs):
        return ObjectPromise.__get(self, "__call__", True)(*args, **kwargs)

    def __get(self, item: str, force=False):
        if force:
            if self._solved:
                return getattr(self._solution, item, None)
            return self._get_attr_promise(item, 0)
        if item.startswith("_") or item == "solve":
            return super(ObjectPromise, self).__getattribute__(item)
        if self._solved:
            return getattr(self._solution, item, None)
        return self._get_attr_promise(item, 0)

    def _get_attr_promise(self, name: str, mode: int, extra=None):
        ret = AttributePromise(self, name, mode, extra)
        self._actions.append(ret)
        return ret

    def solve(self, obj):
        self._solved = True
        self._solution = obj

        for action in self._actions:
            action.solve(self._solution)
        return obj


class AttributePromise(ObjectPromise):
    def __init__(self, parent: ObjectPromise | AttributePromise, name: str, mode: int = 0, extra=None):
        super(AttributePromise, self).__init__()
        self._parent = parent
        self._name = name
        self._mode = mode
        self._extra = extra

    def __get__(self, instance, owner):
        if instance is None or not self.solved:
            return self
        return self.solution

    def solve(self, obj):
        if self._solved:
            return self._solution
        self._solved = True
        if self._mode == 0:
            self._solution = getattr(obj, self._name, None)
        elif self._mode == 1:
            self._solution = self._extra
            setattr(obj, self._name, self._extra)
        elif self._mode == 2:
            self._solution = None
            delattr(obj, self._name)
            return
        for action in self._actions:
            action.solve(self.solution)
        return self._solution


__all__ = [
    "ObjectPromise"
]
