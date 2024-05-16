"""
    这个模块是用来确保整个工程必须要有business包的，\n
    (
        与resource的默认扩展类似，之所以强硬规定必须要有business，\n
        是因为业务代码总是需要有一个统一的归放处，\n
        而且从开发者的角度去看，业务代码的代码结构、文件结构越是趋同，那么设计、理解、优化代码的效率也会越高，\n
        因此反倒不如从工程设计之初就规定——必须存在一个叫做business的包，用来存放业务代码等\n
        当然，business默认扩展与resource的默认扩展还是存在不同的——business扩展本身不建议对其内的代码结构、文件结构进行管理\n
        因为随着时间的推进，总是会出现更加适应当下需要的设计结构出现——它总是会演进的，譬如当前出现的mvc、ddd等设计结构\n
        倘若从本扩展开始就进行干预，反而是对本项目寿命和发展的一种极大的限制——开发者仅能遵循一种设计结构进行快速开发\n
        但应该允许所有人去尝试和体验最新的设计理念，对于本项目来说更是这样\n
        因此本扩展不对开发者所需要的业务代码结构设计进行干预\n
        当然，倘若出现了mvc、ddd等第三方扩展为开发者提供构建结构的帮助，这个是支持的，\n
        本项目不希望从手脚架本身的角度出发就对使用者造成限制，\n
        但倘若是以第三方扩展的形式出现，\n
        那么这种结构上的规范意味着是可拔插的，它仅会为开发者提供如同本项目一样的便利，而不会造成限制
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


class DefaultBusinessScanner(ScannerAbs):
    name = name_extend

    def scan(self, path_dir: str):
        list_dir_current = [d for d in os.listdir(path_dir) if os.path.isdir(os.path.join(path_dir, d))]

        assert 'business' in list_dir_current, "package named ‘business’ must be existed in project， but not， at this moment"


class DefaultBusinessContainer(ContainerAbs):
    name = name_extend

    def insert(self, path_dir: str, scanner: ScannerAbs):

        scanner.scan(path_dir)

    def query(self):
        pass


class DefaultBusinessLogic(LogicAbs):
    name = name_extend

    def execute(self, container: ContainerAbs):
        pass
