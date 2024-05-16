from flask_projects.core.vars.application import application
from flask_projects.default.configuration.NameFactory import name_extend
from flask_projects.interface.container import ContainerAbs
from flask_projects.interface.logic import LogicAbs


class DefaultConfigurationLogic(LogicAbs):
    name = name_extend

    def execute(self, container: ContainerAbs):
        configs = container.query()

        for config_cls in configs:
            config_cls(application)
