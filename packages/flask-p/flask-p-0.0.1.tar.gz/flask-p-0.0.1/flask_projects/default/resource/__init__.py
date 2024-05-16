"""
    这个模块是用来确保整个工程必须要有resource包的，同时也可以用来对resource包进行管理\n
    (
        之所以强硬规定必须要有resource，\n
        是因为从业务代码的角度去看，\n
        配置文件、第三方所需额外文件、代码运行所产生的文件，甚至极端一些地说，一些类似于环境的依赖文件、对工程进行后续处理的脚本等\n
        它们或多或少总是会存在的，而且就算没有，单单就这么一个空包，也无甚影响\n
        因此反倒不如将这些文件归纳到一处，形成所谓的resource包，以此形成惯例——凡工程所需额外文件，必在resource中\n
        既减轻了设计、存放这些额外文件的心智负担，使得项目交流时能够如同常识一般知道有这样一个包用于存放这样那样的文件，各种项目总是如此;\n
        同时也能为这些额外文件的管理和二次开发提供一些意识上的铺垫，使得后续的处理总归算得上是有迹可循
    )\n
    这个模块是一个内置的默认扩展\n
    这个模块允许继承和修改
"""
import os
import uuid

from flask_projects.interface.container import ContainerAbs
from flask_projects.interface.logic import LogicAbs
from flask_projects.interface.scanner import ScannerAbs


def get_name():

    return uuid.uuid4()


name_extend = get_name()


class DefaultResourceScanner(ScannerAbs):
    name = name_extend

    def scan(self, path_dir: str):

        list_dir_current = [d for d in os.listdir(path_dir) if os.path.isdir(os.path.join(path_dir, d))]

        assert 'resource' in list_dir_current, "package named ‘resource’ must be existed in project， but not， at this moment"


class DefaultResourceContainer(ContainerAbs):
    name = name_extend

    def insert(self, path_dir: str, scanner: ScannerAbs):

        scanner.scan(path_dir)

    def query(self):
        pass


class DefaultResourceLogic(LogicAbs):
    name = name_extend

    def execute(self, container: ContainerAbs):
        pass
