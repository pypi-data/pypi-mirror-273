import os.path
from typing import Optional

from flask_projects.core.order.executor import loader
from flask_projects.core.proj.abs import ProjectAbs
from flask_projects.core.vars.abs import ProjectInfoAbs, ExtendsAbs, ApplicationAbs, OthersAbs, HttpAbs
from flask_projects.core.vars.application import application
from flask_projects.core.vars.extends import extends
from flask_projects.core.vars.http import http
from flask_projects.core.vars.info import info
from flask_projects.core.vars.others import others
from flask_projects.default.app.factory import default_factory
from flask_projects.default.business import DefaultBusinessScanner, DefaultBusinessContainer, DefaultBusinessLogic
from flask_projects.default.configuration import DefaultConfigurationScanner, DefaultConfigurationContainer, \
    DefaultConfigurationLogic
from flask_projects.default.resource import DefaultResourceScanner, DefaultResourceContainer, DefaultResourceLogic
from flask_projects.default.router import DefaultRouterScanner, DefaultRouterContainer, DefaultRouterLogic, \
    DefaultRouterOrder
from flask_projects.interface.factory import AppFactoryAbs


class Project(ProjectAbs):

    def __init__(self):
        # 初始化，生成必要的容器/对象作为属性
        self.info: Optional[ProjectInfoAbs] = info
        self.extends: Optional[ExtendsAbs] = extends.setter_project(self)
        self.application: Optional[ApplicationAbs] = application
        self.http: Optional[HttpAbs] = http

        self.others: Optional[OthersAbs] = others

        # 向容器属性中加入默认/内置内容
        self.setter_app().setter_args().setter_extend(
            DefaultResourceScanner,
            DefaultResourceContainer,
            DefaultResourceLogic
        ).setter_extend(
            DefaultBusinessScanner,
            DefaultBusinessContainer,
            DefaultBusinessLogic
        ).setter_extend(
            DefaultConfigurationScanner,
            DefaultConfigurationContainer,
            DefaultConfigurationLogic
        ).setter_extend(
            DefaultRouterScanner,
            DefaultRouterContainer,
            DefaultRouterLogic,
            DefaultRouterOrder
        )

    def setter_extend(
            self,
            scanner,
            container,
            logic,
            order=None
    ):
        self.extends.insert(scanner, container, logic, order)

        return self

    def setter_app(self,
                   app_factory: AppFactoryAbs = None
                   ):
        factory = app_factory if app_factory else default_factory

        self.application.setter_app(factory.get_app())

        return self

    def setter_args(
            self,
            ip: str = '0.0.0.0',
            port: int = 8080,
            *args,
            **kwargs
    ):
        self.info.insert('ip', ip)
        self.info.insert('port', port)
        self.info.insert('args', list(args))

        if 'path' in kwargs.keys():
            path = kwargs.pop('path')
            self.info.insert('path_dir_code', os.path.abspath(path).replace('main.py', ''))

        self.info.insert('kwargs', kwargs)

        return self

    def byOrder(self):
        """
            加载、运行extends
            加载命令、执行命令
        :return:
        """
        for name_extends in self.extends.query_names_scanner():
            scanner = self.extends.query_scanner(name_extends)
            container = self.extends.query_container(name_extends)
            logic = self.extends.query_logic(name_extends)

            container.insert(self.info.query('path_dir_code'), scanner)
            logic.execute(container)

        executor = loader(self)
        executor()

    def __call__(self, *args, **kwargs):
        # TODO 2024/4/21 老版本里面重写了这个，既解决了部分配置，也从编码上使其看起来像创建对象，可以考虑设计一下

        return self


project = Project()
