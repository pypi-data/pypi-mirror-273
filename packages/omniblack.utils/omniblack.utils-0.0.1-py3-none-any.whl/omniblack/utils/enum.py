from enum import Enum as _Enum

from public import public


@public
class Enum(_Enum):
    def __init_subclass__(cls, *args, **kwargs):
        super().__init_subclass__(*args, **kwargs)
        cls._subclasses.append(cls)

        for yaml in cls._yaml:
            yaml.register_class(cls)

    @staticmethod
    def _generate_next_value_(name, start, count, last_values):
        return name

    @classmethod
    def to_yaml(cls, representer, node):
        return representer.represent_str(node.value)

    @classmethod
    def from_yaml(cls, constructor, node):
        return cls(node.value)

    @classmethod
    def set_yaml(cls, yaml_instance):
        cls._yaml.append(yaml_instance)

        for sub_cls in cls._subclasses:
            yaml_instance.register_class(sub_cls)


Enum._yaml = []
Enum._subclasses = []
