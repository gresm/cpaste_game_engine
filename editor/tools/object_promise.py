from __future__ import annotations


_required_magic_methods = set(dir(object))


def _is_important_key(key: str):
    return key in _required_magic_methods or (key.startswith("_") and not key.startswith("__")) or key == "solve"


def _is_sub_important(key: str):
    return key in {"__init__", "__getattribute__", "__setattr__", "__delattr__", "__get__"} or key == "solve"\
           or (key.startswith("_") and not key.startswith("__"))


class ObjectPromise:
    def __init__(self):
        self._solved = False
        self._solution = None
        self._actions: list[AttributePromise] = []

    def __getattribute__(self, item: str):
        return ObjectPromise._get(self, item, True)

    def __setattr__(self, key, value):
        return ObjectPromise._set(self, key, value, True)

    def __delattr__(self, item):
        return ObjectPromise._del(self, item, True)

    def __call__(self, *args, **kwargs):
        return self._get("__call__", False)(*args, **kwargs)

    def __float__(self, *args, **kwargs):
        return self._get("__float__", False)(*args, **kwargs)

    def __int__(self, *args, **kwargs):
        return self._get("__int__", False)(*args, **kwargs)

    def _get(self, item: str, imp):
        run = _is_sub_important
        if imp:
            run = _is_important_key
        if run(item):
            return super(ObjectPromise, self).__getattribute__(item)
        if self._solved:
            return getattr(self._solution, item)
        return self._get_attr_promise(item, 0)

    def _set(self, item: str, value, imp):
        run = _is_sub_important
        if imp:
            run = _is_important_key
        if run(item):
            return super(ObjectPromise, self).__setattr__(item, value)
        if self._solved:
            return setattr(self._solution, item, value)
        return self._get_attr_promise(item, 1, value)

    def _del(self, item: str, imp):
        run = _is_sub_important
        if imp:
            run = _is_important_key
        if run(item):
            return super(ObjectPromise, self).__delattr__(item)
        if self._solved:
            return delattr(self._solution, item)
        return self._get_attr_promise(item, 2)

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

    def __getattribute__(self, item: str):
        return ObjectPromise._get(self, item, False)

    def __setattr__(self, key, value):
        return ObjectPromise._set(self, key, value, False)

    def __delattr__(self, item):
        return ObjectPromise._del(self, item, False)

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
