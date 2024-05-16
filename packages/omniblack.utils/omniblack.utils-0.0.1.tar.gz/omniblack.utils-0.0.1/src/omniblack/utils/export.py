import sys
from importlib import import_module
from importlib.metadata import entry_points
from importlib.resources import files

from public import public

public(public=public)

console_scripts_entry_points = entry_points(group='console_scripts')

console_scripts = {
    ep.value.rsplit(':')[0]
    for ep in console_scripts_entry_points
}


@public
def export(module_dict=None, ignore=None):
    if ignore is None:
        ignore = {'__init__', '__main__'}
    else:
        ignore = {'__init__', '__main__', *ignore}
    try:
        if module_dict is None:
            module_dict = sys._getframe(1).f_globals

        pkg_name = module_dict['__package__']

        pkgs = tuple(pkg_name.split('.'))
        pkg = files(pkg_name)

        mod_all = []
        for entry in pkg.iterdir():

            entry_name = entry.name

            if entry.is_dir():
                if entry_name == '__pycache__' or entry_name.startswith('.'):
                    continue
            elif entry_name.endswith('.py'):
                entry_name = entry_name.removesuffix('.py')
            else:
                continue

            if entry_name in ignore:
                continue

            mod_path_tuple = pkgs + (entry_name,)
            mod_path = '.'.join(mod_path_tuple)

            if mod_path in console_scripts:
                continue

            mod = import_module(mod_path)

            try:
                mod_all.extend(mod.__all__)
                for name in mod.__all__:
                    if name in module_dict and name != entry_name:
                        print(
                            f'Colliding name "{name}" in module "{mod_path}"',
                            file=sys.stderr,
                        )
                    module_dict[name] = getattr(mod, name)
            except AttributeError:
                pass

        module_dict['__all__'] = tuple(mod_all)
    finally:
        del module_dict
