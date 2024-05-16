"""
    这个模块是用来为工程提供一个最基本的http路由绑定形式的\n
    这个模块是一个内置的默认扩展\n
    这个模块允许继承和修改——或者说，这个模块鼓励用扩展去替换，\n
    或者是用更多的第三方路由扩展模块去增加绑定和操作路由的能力——不一定非得使用本模块提供的绑定路由方式去进行业务的路由编写\n
    作为手脚架本身，第三方依赖应当尽可能少，方便使用，也使得手脚架更加的轻便和易扩展，省得依赖太多造成耦合之类的麻烦\n
    但毕竟是以提供快速开发帮助为目的，
    因此不得不承认，很多的flask第三方扩展是能够为路由的操作和管理提供极大便利的——不一定会比原生更优异，但至少是真的提供了很大的便利\n
    所以说，本模块非常支持使用更加快速、好用的模块去替换
"""


from flask_projects.default.router.plan_0.scanner import Plan0RouterScanner as DefaultRouterScanner
from flask_projects.default.router.plan_0.container import Plan0RouterContainer as DefaultRouterContainer
from flask_projects.default.router.plan_0.logic import Plan0RouterLogic as DefaultRouterLogic
from flask_projects.default.router.plan_0.order import Plan0RouterOrder as DefaultRouterOrder
