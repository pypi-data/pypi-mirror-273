from abc import abstractmethod

from flask_projects.interface.base import ProjectInterfaceBase
from flask_projects.interface.scanner import ScannerAbs


class ContainerAbs(ProjectInterfaceBase):

    name: str = '...'  # 每一个container必须要有唯一名称，用于core模块进行管理

    @abstractmethod
    def insert(self, path_dir: str, scanner: ScannerAbs):

        ...

    @abstractmethod
    def query(self):

        ...
