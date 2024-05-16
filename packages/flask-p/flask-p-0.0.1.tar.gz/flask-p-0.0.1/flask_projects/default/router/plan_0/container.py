from flask_projects.default.router.NameFactory import name_extend
from flask_projects.interface.container import ContainerAbs
from flask_projects.interface.scanner import ScannerAbs


class Plan0RouterContainer(ContainerAbs):
    name = name_extend

    def __init__(self, project):
        self.cls_route = []
        super().__init__(project)

    def insert(self, path_dir: str, scanner: ScannerAbs):

        self.cls_route = scanner.scan(path_dir)

    def query(self):

        return self.cls_route
