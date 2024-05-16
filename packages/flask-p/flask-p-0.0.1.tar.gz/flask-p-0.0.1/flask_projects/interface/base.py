from abc import ABCMeta


class ProjectInterfaceBase(metaclass=ABCMeta):

    def __init__(self, project):

        self.project = project
