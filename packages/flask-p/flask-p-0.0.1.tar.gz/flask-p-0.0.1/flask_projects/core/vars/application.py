from typing import Any, Optional, List

from flask import Flask

from flask_projects.core.vars.abs import ApplicationAbs


class Application(ApplicationAbs):
    """
        本对象用于存储app，并为app的挂载提供适配后的接口
    """

    private_attrs = [
        'g'
    ]   # app中受保护的属性

    def __init__(self, app: Flask = None):
        self.app: Optional[Flask] = app
        self.record: List[str] = list()

    def setter_app(self, app: Flask):

        for name_attr in self.record:
            setattr(app, name_attr, self.query(name_attr))

        self.app = app

        return self

    def getter_app(self) -> Flask:

        return self.app

    def judge_exists_app(self) -> bool:

        if not self.app:
            return False

        return True

    def insert(self, name: str, var: Any) -> bool:
        # TODO 2024/5/5 我感觉这一段其实还需要再想想再改改，
        #  因为其他开发者很有可能直接突破对于app属性的规定增改流程，导致增删的属性未被记录，
        #  目前我能想到的思路就是，直接重写__setter__和__getter__方法，使得属性的增删只能通过规定的流程进行
        assert name not in self.private_attrs, "the attribute is private in application object"

        setattr(self.app, name, var)
        if name not in self.record:
            self.record.append(name)

        return True

    def query(self, name: str):

        return getattr(self.app, name, None)

    def destroy(self, name) -> bool:
        # TODO: 有些变量的删除必须阻止

        assert name not in self.private_attrs, "the attribute is private in application object"

        delattr(self.app, name)
        self.record.remove(name)

        return True


application = Application()
