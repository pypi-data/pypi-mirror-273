from flask_projects.core.proj.project import project

from flask_projects.core.vars.http import http
from flask_projects.core.vars.info import info
from flask_projects.core.vars.application import application
from flask_projects.core.vars.extends import extends
from flask_projects.core.vars.others import others


__all__ = [
    'project',
    'http', 'info', 'application', 'extends', 'others'
]
