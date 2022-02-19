from __future__ import annotations


_required_magic_methods = set(dir(object))
_add_keywords = {
    '__new__', '__init__', '__del__', '__pos__', '__neg__', '__abs__', '__invert__', '__round__', '__floor__',
    '__ceil__', '__trunc__', '__iadd__', '__isub__', '__imul__', '__ifloordiv__', '__idiv__', '__itruediv__',
    '__imod__', '__ipow__', '__ilshift__', '__irshift__', '__iand__', '__ior__', '__ixor__', '__int__',
    '__float__', '__complex__', '__oct__', '__hex__', '__index__', '__trunc__', '__str__', '__repr__',
    '__unicode__', '__format__', '__hash__', '__nonzero__', '__dir__', '__sizeof__', '__getattr__',
    '__setattr__', '__delattr__', '__add__', '__sub__', '__mul__', '__floordiv__', '__truediv__',
    '__mod__', '__pow__', '__lt__', '__le__', '__eq__', '__ne__', '__ge__'
}

_add_keywords = _add_keywords.difference(_required_magic_methods)


def _is_important_key(key: str):
    return key in _required_magic_methods or (key.startswith("_") and not key.startswith("__")) or key == "solve"


def _is_sub_important(key: str):
    return key in {"__init__", "__getattribute__", "__setattr__", "__delattr__", "__get__"} or key == "solve"\
           or (
                   (len(key) == 0 or key[0] == "_")
                   and not (len(key) <= 1 or key[1] == "_")
           )


def _generate_magic_method(name: str):
    gl = {}
    exec(f"""def {name}(self, *args, **kwargs):
    try:
        val = self._get("{name}", False)
    except AttributeError:
        return
    return val(*args, **kwargs)""", gl)
    return gl[name]


class ObjectPromise:
    for _ in _add_keywords:
        locals()[_] = _generate_magic_method(_)

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
