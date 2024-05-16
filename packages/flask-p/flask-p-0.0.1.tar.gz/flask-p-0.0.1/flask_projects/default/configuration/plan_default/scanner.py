import importlib
import os
import traceback

from flask_projects.default.configuration.NameFactory import name_extend
from flask_projects.default.configuration.convention import BasicConfig
from flask_projects.interface.scanner import ScannerAbs


class DefaultConfigurationScanner(ScannerAbs):
    name = name_extend

    def scan(self, path_dir: str):

        # 老版本的代码了，不想动，其实可以用更成熟的模块去代替的
        configs = []
        for r, d, filenames in os.walk(path_dir):
            if 'business' not in r or 'config' not in r:
                continue
            for filename in filenames:
                if filename == '__init__.py' or not filename.endswith('.py'):
                    continue

                try:
                    module = importlib.machinery.SourceFileLoader(
                        filename.replace(',py', ''), os.path.join(r, filename)
                    ).load_module()
                    class_imported = getattr(module, filename.replace('.py', ''))
                    if issubclass(class_imported, BasicConfig):
                        configs.append(class_imported)
                except Exception:
                    print(traceback.format_exc())
        configs.sort(key=lambda x: x.sort)

        return configs
