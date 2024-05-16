from flask import Flask

from flask_projects.interface.factory import AppFactoryAbs


class DefaultAppFactory(AppFactoryAbs):
    def get_app(self) -> Flask:
        app = Flask('project')

        return app


default_factory = DefaultAppFactory()
