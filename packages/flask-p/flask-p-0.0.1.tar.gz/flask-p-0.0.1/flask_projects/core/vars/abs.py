from abc import ABCMeta, abstractmethod
from typing import Any, List, Optional

from flask import Flask

from flask_projects.core.proj.abs import ProjectAbs
from flask_projects.interface.container import ContainerAbs
from flask_projects.interface.logic import LogicAbs
from flask_projects.interface.order import OrderAbs
from flask_projects.interface.scanner import ScannerAbs


class VarAbs(metaclass=ABCMeta):

    @abstractmethod
    def insert(self, *args, **kwargs) -> bool:
        """
            用于向存储对象插入对应的变量
        :param args:
        :param kwargs:
        :return: 为真表示正常，为false表异常
        """
        ...

    @abstractmethod
    def query(self, *args, **kwargs):
        """
            用于从对象中查询对应的变量
        :param args:
        :param kwargs:
        :return:
        """
        ...

    @abstractmethod
    def destroy(self, *args, **kwargs) -> bool:
        """
            用于从对象中删除对应的变量
        :param args:
        :param kwargs:
        :return:为真表示正常，为false表异常
        """
        ...


class ProjectInfoAbs(VarAbs):

    @abstractmethod
    def insert(self, name: str, var: Any) -> bool:
        ...

    @abstractmethod
    def query(self, name: str):

        ...

    @abstractmethod
    def destroy(self, name) -> bool:

        ...


class ExtendsAbs(VarAbs):

    @abstractmethod
    def setter_project(self, project: ProjectAbs):

        ...

    @abstractmethod
    def insert(
            self,
            scanner,
            container,
            logic,
            shell
    ) -> bool:
        ...

    @abstractmethod
    def query(self, name: str):
        ...

    @abstractmethod
    def query_names_scanner(self):

        ...

    @abstractmethod
    def query_names_container(self):

        ...

    @abstractmethod
    def query_names_logics(self):

        ...

    @abstractmethod
    def query_names_order(self):

        ...

    @abstractmethod
    def query_scanner(self, name: str) -> Optional[ScannerAbs]:
        ...

    @abstractmethod
    def query_container(self, name: str) -> Optional[ContainerAbs]:

        ...

    @abstractmethod
    def query_logic(self, name: str) -> Optional[LogicAbs]:

        ...

    @abstractmethod
    def query_order(self, name: str) -> Optional[OrderAbs]:

        ...

    @abstractmethod
    def destroy(self, name) -> bool:
        ...


class ApplicationAbs(VarAbs):

    @abstractmethod
    def setter_app(self, app: Flask):
        ...

    @abstractmethod
    def getter_app(self) -> Flask:

        ...

    @abstractmethod
    def judge_exists_app(self) -> bool:
        ...

    @abstractmethod
    def insert(self, name: str, var: Any) -> bool:
        ...

    @abstractmethod
    def query(self, name: str):
        ...

    @abstractmethod
    def destroy(self, name) -> bool:
        ...


class HttpAbs(VarAbs):

    @abstractmethod
    def insert(self, router: str, methods: List[str], resource: Any, **kwargs) -> bool:
        """
            添加flask路由相关数据/信息
        :param router:
        :param methods:
        :param resource: fvb/cvb，因为可能后续extends会用restframework，它与flask原生的cbv有些区别，所以暂定any，校验留待实现完成
        :return:
        """
        pass

    @abstractmethod
    def query(self, router: str):
        pass

    @abstractmethod
    def query_router(self):
        ...

    @abstractmethod
    def destroy(self, router: str) -> bool:
        pass


class OthersAbs(VarAbs):
    @abstractmethod
    def insert(self, name: str, var: Any) -> bool:
        ...

    @abstractmethod
    def query(self, name: str):
        ...

    @abstractmethod
    def destroy(self, name) -> bool:
        ...
