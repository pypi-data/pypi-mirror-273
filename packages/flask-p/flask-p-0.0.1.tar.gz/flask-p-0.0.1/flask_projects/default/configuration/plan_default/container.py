from typing import Optional

from flask_projects.default.configuration.NameFactory import name_extend
from flask_projects.interface.container import ContainerAbs
from flask_projects.interface.scanner import ScannerAbs


class DefaultConfigurationContainer(ContainerAbs):
    name = name_extend

    def __init__(self, project):
        self.configs: Optional = None
        super().__init__(project)

    def insert(self, path_dir: str, scanner: ScannerAbs):
        self.configs = scanner.scan(path_dir)

    def query(self):

        return self.configs
