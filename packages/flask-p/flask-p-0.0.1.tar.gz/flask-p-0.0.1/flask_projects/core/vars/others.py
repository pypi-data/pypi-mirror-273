from typing import Any

from flask_projects.core.vars.abs import OthersAbs


class OthersVars(OthersAbs):
    """
        用来存储一些奇奇怪怪的数据/信息
    """
    def insert(self, name: str, var: Any) -> bool:
        setattr(self, name, var)

        return True

    def query(self, name: str):
        return getattr(self, name, None)

    def destroy(self, name) -> bool:
        delattr(self, name)

        return True


others = OthersVars()
