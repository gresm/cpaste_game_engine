from __future__ import annotations


from typing import Type
import re


class _Template:
    def __init__(self):
        self.txt: list[str | tuple[str]] = []
        self.fields: set[str] = set()

    def __str__(self):
        ret = ""
        for el in self.txt:
            if isinstance(el, tuple):
                ret += f"{{{ret[0]}}}"
            else:
                ret += el
        return ret

    def __repr__(self):
        return f"<{self.__class__.__name__}(\"{str(self)}\")>"

    def append_txt(self, txt: str):
        self.txt.append(txt)

    def append_field(self, txt: str):
        self.txt.append((txt,))
        self.fields.add(txt)

    def convert(self, fields: dict[str, str]):
        ret = ""
        for el in self.txt:
            if isinstance(el, tuple):
                if el[0] in fields:
                    ret += fields[el[0]]
            else:
                ret += el
        return ret


def _parse_template(template: str):
    var_symbol = "%"
    var_valid = r"\w"
    cur_name = ""
    is_var = False
    ret = _Template()

    for char in template:
        if char == var_symbol:
            if is_var:
                ret.append_field(cur_name)
            else:
                ret.append_txt(cur_name)
            is_var = not is_var
            cur_name = ""
        else:
            if is_var:
                if re.match(var_valid, char):
                    cur_name += char
                else:
                    is_var = False
            else:
                cur_name += char

    if cur_name != "":
        ret.append_txt(cur_name)
    return ret


class TypeInfo:
    def __init__(
            self, cls: Type[ArgType], name: str, runtime_types: set[str], elements: dict[str, tuple[str, list[str]]]
    ):
        self.cls = cls
        self.name = name
        self.runtime_types = runtime_types
        self._elements = elements
        self.elements: dict[str, ElementTypeInfo] = {}

        for name in elements:
            el_type = elements[name][0]
            el_confs: list[ElementTypeConfigInfo] = []

            for conf in elements[name][1]:
                el_confs.append(ElementTypeConfigInfo(conf, conf not in runtime_types))

            el_type_conf = ElementTypeConfigInfo(el_type, el_type not in runtime_types)
            self.elements[name] = ElementTypeInfo(name, el_type_conf, el_confs)


class ElementTypeInfo:
    def __init__(
            self, name: str, requested_type: ElementTypeConfigInfo, requested_configs: list[ElementTypeConfigInfo]
    ):
        self.name = name
        self.requested_type = requested_type
        self.requested_configs = requested_configs


class ElementTypeConfigInfo:
    def __init__(self, name: str, decided: bool):
        self.name = name
        self.decided = decided


class ArgType:
    _registered_types: dict[str, TypeInfo] = {}

    def __init__(self, *args, **kwargs):
        pass

    def __init_subclass__(cls, **kwargs):
        self = ArgType
        name: str = kwargs["name"] if "name" in kwargs else cls.__name__
        fields: set[str] = set(kwargs["fields"]) if "fields" in kwargs else set()
        new_args = set(dir(cls)).difference(dir(self))
        elements: dict[str, tuple[str, list[str]]] = {}

        for el in new_args:
            v = getattr(cls, el, None)
            if isinstance(v, str):
                if v[-1] == "]":
                    splt = v[:-1].split("[")
                    args = splt[1].split(",")
                    elements[el] = splt[0], args

        self._register_type(name, TypeInfo(cls, name, fields, elements))

    @classmethod
    def _register_type(cls, name: str, el: TypeInfo):
        cls._registered_types[name] = el


class BaseSnippet:
    def __init__(self, snippet_text: str):
        self.snippet_text = snippet_text

    def generate(self) -> str:
        pass
