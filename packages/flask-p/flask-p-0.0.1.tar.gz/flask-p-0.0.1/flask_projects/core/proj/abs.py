from abc import ABCMeta, abstractmethod

from flask_projects.interface.factory import AppFactoryAbs


class ProjectAbs(metaclass=ABCMeta):

    @abstractmethod
    def setter_extend(
            self,
            scanner,
            container,
            logic,
            order=None
    ):
        """
            该方法包含方法链特性，每次都会返回self
            该方法用于添加项目运行时的扩展配置
        :param scanner: 扫描器，用于扫描工程路径下的文件并导入对应文件所包含的类/对象，并将其放入container中
        :param container: 存放扫描器所得类/对象的存储容器
        :param logic: 用于在container中存在内容后，执行项目启动前的必要逻辑，如：挂载、初始化、关系构造等
        :param order: 用于向项目增加该扩展所对应的命令行对象
        :return:
        """
        ...

    @abstractmethod
    def setter_app(
            self,
            app_factory: AppFactoryAbs
    ):
        """
            扩展配置方法的变种，特殊之处在于
            1.该方法可不用实现，内部存在默认app配置
            2.这里的参数，其接口类型应当是指定的app相关接口类型
        :param app_factory:
        :return:
        """
        ...

    @abstractmethod
    def setter_args(
            self,
            ip: str = '0.0.0.0',
            port: int = 8080,
            *args,
            **kwargs
    ):
        """
            这里其实就是为了设置app运行时的启动参数，譬如ip和端口，同样拥有默认实现(其中*args、**kwargs主要是受flask限制而不得不加入的参数)
        :param ip:
        :param port:
        :return:
        """
        ...

    @abstractmethod
    def byOrder(self):
        """
            用于接受并执行命令行内容
        :return:
        """
        ...
