from flask_projects.core.vars.application import application
from flask_projects.core.vars.http import http
from flask_projects.default.router.NameFactory import name_extend
from flask_projects.default.router.convention import RouterBasic
from flask_projects.interface.container import ContainerAbs
from flask_projects.interface.logic import LogicAbs


class Plan0RouterLogic(LogicAbs):
    name = name_extend

    def execute(self, container: ContainerAbs):

        list_cls_route: list = container.query()

        for cls_route in list_cls_route:
            instance: RouterBasic = cls_route(application, http)
            instance.register()
            instance.bind()
