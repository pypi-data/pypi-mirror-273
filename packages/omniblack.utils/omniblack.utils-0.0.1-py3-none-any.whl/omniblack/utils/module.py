import sys

from importlib.metadata import version
from types import ModuleType

from public import public

from .export import export


@public
def improve_module(__name__, ignore=None):
    sys.modules[__name__].__class__ = OmniblackModule
    export(sys.modules[__name__].__dict__, ignore)


@public
class OmniblackModule(ModuleType):
    def __getattr__(self, name):
        if name == '__version__':
            ver = version(self.__package__)
            self.__dict__['__version__'] = ver
            return ver
        else:
            raise AttributeError(name)
