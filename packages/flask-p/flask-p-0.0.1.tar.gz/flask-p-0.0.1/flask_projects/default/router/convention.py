from abc import ABCMeta, abstractmethod
from typing import List

from flask_projects.core.vars.abs import ApplicationAbs, HttpAbs


class RouterBasic(metaclass=ABCMeta):
    """
        路由基类
    """

    def __init__(self, application: ApplicationAbs = None, http: HttpAbs = None):
        self.application = application
        self.http = http

        self.route: List[str] = list()

    def init_router(self, application: ApplicationAbs, http: HttpAbs):
        self.application = application
        self.http = http

    def bind(self):
        app = self.application.getter_app()

        for route in self.route:
            detail = self.http.query(route)
            app.add_url_rule(route, None, detail.resource, methods=detail.methods)

    def add_route(self, route: str, method: List[str], resource):
        self.route.append(route)
        self.http.insert(route, method, resource)

    @abstractmethod
    def register(self):
        ...
