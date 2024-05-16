from typing import Optional

from abc import ABCMeta, abstractmethod

from flask_projects.core.vars.abs import ApplicationAbs


class BasicConfig(metaclass=ABCMeta):
    """
        配置基类——所有的配置必须继承并实现该基类
    """

    sort: Optional[int] = None

    def __init__(self, application: ApplicationAbs = None):
        self.application = application
        if application:
            self.init_application(application)

    @abstractmethod
    def init_application(self, application: ApplicationAbs):
        # 实际上就是达到了配置类对应的配置内容加载效果
        ...
