from typing import Dict, Optional, Tuple

from flask_projects.core.proj.abs import ProjectAbs
from flask_projects.core.vars.abs import ExtendsAbs
from flask_projects.interface.container import ContainerAbs
from flask_projects.interface.logic import LogicAbs
from flask_projects.interface.scanner import ScannerAbs
from flask_projects.interface.order import OrderAbs


class Judge:

    @staticmethod
    def judge_scanner(map_scanner: Dict[str, ScannerAbs], scanner_cls) -> Tuple[bool, str]:

        if not issubclass(scanner_cls, ScannerAbs):

            return False, "the argument of scanner must be subclass of ScannerAbs"

        scanner_saved = map_scanner.get(scanner_cls.name, None)

        if scanner_saved:
            if not issubclass(scanner_cls, scanner_saved.__class__):

                return False, "the name has been existed in scanners"

        return True, "pass"

    @staticmethod
    def judge_container(map_container: Dict[str, ContainerAbs], container_cls) -> Tuple[bool, str]:

        if not issubclass(container_cls, ContainerAbs):
            return False, "the argument of scanner must be subclass of ContainerAbs"

        container_saved = map_container.get(container_cls.name, None)

        if container_saved:
            if not issubclass(container_cls, container_saved.__class__):
                return False, "the name has been existed in containers"

        return True, "pass"

    @staticmethod
    def judge_logic(map_logic: Dict[str, LogicAbs], logic_cls) -> Tuple[bool, str]:

        if not issubclass(logic_cls, LogicAbs):
            return False, "the argument of scanner must be subclass of LogicAbs"

        logic_saved = map_logic.get(logic_cls.name, None)

        if logic_saved:
            if not issubclass(logic_cls, logic_saved.__class__):
                return False, "the name has been existed in logics"

        return True, "pass"

    @staticmethod
    def judge_order(map_order: Dict[str, OrderAbs], order_cls) -> Tuple[bool, str]:

        if not issubclass(order_cls, OrderAbs):
            return False, "the argument of scanner must be subclass of OrderAbs"

        order_saved = map_order.get(order_cls.name, None)

        if order_saved:
            if not issubclass(order_cls, order_saved.__class__):
                return False, "the name has been existed in orders"

        return True, "pass"


class Extends(ExtendsAbs):
    """
        本对象仅是为了方便集中管理扩展，用来存储所有的scanner、container、logic
    """

    def __init__(self):
        self.map_scanner: Dict[str, ScannerAbs] = dict()
        self.map_container: Dict[str, ContainerAbs] = dict()
        self.map_logic: Dict[str, LogicAbs] = dict()
        self.map_order: Dict[str, OrderAbs] = dict()

        self.project: Optional[ProjectAbs] = None

    def setter_project(self, project: ProjectAbs):
        self.project = project

        return self

    def insert(
            self,
            scanner,
            container,
            logic,
            order=None
    ) -> bool:
        # 校验名称
        if order:
            assert scanner.name == container.name and scanner.name == logic.name and scanner.name == order.name, "the name is not the universal name of this extend"
        else:
            assert scanner.name == container.name and scanner.name == logic.name, "the name is not the universal name of this extend"

        flag_scanner, message_scanner = Judge.judge_scanner(self.map_scanner, scanner)
        assert flag_scanner, flag_scanner
        flag_container, message_container = Judge.judge_container(self.map_container, container)
        assert flag_container, message_container
        flag_logics, message_logics = Judge.judge_logic(self.map_logic, logic)
        assert flag_logics, message_logics
        if order:
            flag_order, message_order = Judge.judge_order(self.map_order, order)
            assert flag_order, message_order

        self.map_scanner[scanner.name] = scanner(self.project)
        self.map_container[container.name] = container(self.project)
        self.map_logic[logic.name] = logic(self.project)
        if order:
            self.map_order[order.name] = order(self.project)

        return True

    def query(self, name: str):
        if name not in self.map_scanner.keys():
            return {}

        return {
            'scanner': self.map_scanner.get(name),
            'container': self.map_container.get(name),
            'logic': self.map_logic.get(name),
            'order': self.map_order.get(name)
        }

    def query_names_scanner(self):

        return list(self.map_scanner.keys())

    def query_names_container(self):

        return list(self.map_container.keys())

    def query_names_logics(self):

        return list(self.map_logic.keys())

    def query_names_order(self):

        return list(self.map_order.keys())

    def query_scanner(self, name: str):

        return self.map_scanner.get(name, None)

    def query_container(self, name: str):

        return self.map_container.get(name, None)

    def query_logic(self, name: str):

        return self.map_logic.get(name, None)

    def query_order(self, name: str) -> Optional[OrderAbs]:

        return self.map_order.get(name, None)

    def destroy(self, name) -> bool:
        del self.map_scanner[name]
        del self.map_container[name]
        del self.map_logic[name]
        del self.map_order[name]

        return True


extends = Extends()
