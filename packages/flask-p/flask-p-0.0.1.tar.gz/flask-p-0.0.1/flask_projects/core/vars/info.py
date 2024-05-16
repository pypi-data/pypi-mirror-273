from typing import Any

from flask_projects.core.vars.abs import ProjectInfoAbs


class ProjectInfo(ProjectInfoAbs):
    """
        本对象存在的立意是——存储与当前项目相关的项目信息，譬如项目路径等
        而具体存储哪些内容，删改哪些内容，可由extends和项目自行决定
        至于限制和校验，目前认为不应当由core和var本身去考虑
    """

    def insert(self, name: str, var: Any) -> bool:
        setattr(self, name, var)

        return True

    def query(self, name: str):

        return getattr(self, name, None)

    def destroy(self, name) -> bool:

        delattr(self, name)

        return True


info = ProjectInfo()
