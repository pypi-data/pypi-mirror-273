# Flask_Project系列

## 项目进度

进行中

## 项目介绍

* 本项目基于flask及其生态
* 本项目属于手脚架性质
* 借助本项目以及后续补充甚至自定义的扩展，可以快速开发工程化业务代码

## 环境依赖

* 本项目开发时使用的python版本为3.8
* 核心部分代码依赖flask、click(flask最新版本已包含对click的安装需要，仅安装flask即可顺带完成对click的安装)，可直接执行`pip install flask`完成安装
* 临时文件夹(tamp)中的扩展(extends)中，restful扩展依赖flask_restful，可直接执行`pip install flask-restful`完成安装

## 项目结构

```│
│  README.md
│
├─core
│  │  __init__.py
│  │
│  ├─order
│  │  │  executor.py
│  │  │  __init__.py
│  │  │
│  │  └─unity
│  │        run.py
│  │        shell.py
│  │        __init__.py
│  │
│  ├─proj
│  │     abs.py
│  │     project.py
│  │     __init__.py
│  │
│  └─vars
│        abs.py
│        application.py
│        extends.py
│        http.py
│        info.py
│        others.py
│        __init__.py
│
├─default
│  │  __init__.py
│  │
│  ├─app
│  │     factory.py
│  │     __init__.py
│  │
│  ├─business
│  │     __init__.py
│  │
│  ├─configuration
│  │  │  convention.py
│  │  │  NameFactory.py
│  │  │  __init__.py
│  │  │
│  │  ├─plan_1
│  │  │      __init__.py
│  │  │
│  │  └─plan_default
│  │        container.py
│  │        logic.py
│  │        scanner.py
│  │        __init__.py
│  │
│  ├─resource
│  │     __init__.py
│  │
│  └─router
│     │  convention.py
│     │  NameFactory.py
│     │  __init__.py
│     │
│     └─plan_0
│           container.py
│           logic.py
│           order.py
│           scanner.py
│           __init__.py
│
├─example
│  │  main.py
│  │
│  ├─business
│  │  └─router
│  │         Restful.py
│  │         Unity.py
│  │         __init__.py
│  │
│  └─resource
│      └─test
│            example.http
│
└─tamp
│  __init__.py
│
└──extends
    │  │  __init__.py
    │  │
    │  ├─ddd
    │  │      __init__.py
    │  │
    │  ├─health
    │  │      __init__.py
    │  │
    │  ├─mvc
    │  │      __init__.py
    │  │
    │  └─restful
    │        container.py
    │        convertion.py
    │        logic.py
    │        scanner.py
    │        __init__.py
    │
    │
    └─interface
          base.py
          container.py
          factory.py
          logic.py
          order.py
          scanner.py
          init__.py

```

## 设计概述

* 本项目主要围绕extend——扩展的概念展开设计，项目本身仅提供core、default两个模块
* core模块作为项目运行的核心，尽可能削减了运行时，除扩展以外所需要的一切外部依赖，其在flask提供的基础网络能力的基础上，参考django的设计，提供了以下模块及其对应的能力：
  * proj：
    * proj即project的缩写，旨在为项目的运行提供机制
    * 其内仅包含两个文件，abs、project，abs是project模块的抽象基类，project则是当前提供机制的根本模块
  * order：
    * order即命令，其设计参考django的指令设计，基于click为本项目提供了命令行执行的能力
    * 其内部由executor与unity两个部分组成，其中，executor为项目集成命令行能力提供了基础，使得project能够借此为项目添加各式各样的命令行，同时，unity也为项目提供了一些内置的命令(run、shell，run用于运行项目，shell则可以使开发人员将现有的代码设计作为依赖，通过命令行的形式对设计进行验证)
    * order除去使用内置指令之外，也可以通过extend的方式进行增加
  * vars：
    * vars即变量，参考flask对于app各种扩展的绑定机制，为项目在其内部提供了变量的概念，一切的扩展、数据、信息，均统一存放在各式各样的变量当中，并集成到project，以此为项目的运行提供支持
    * abs，一切项目变量最根本的抽象基类，为变量规定了所必须具备的能力(插入、查询、删除)；由此也可以看出，变量的概念，其实一定程度上，是为了让project能够使用为各种数据、信息专门定制的数据结构/数据容器对项目进行管理而演变出来的
    * application：管理flask app的变量绑定
    * extends：管理项目运行所需的扩展
    * http：管理项目中与http通讯相关的数据，如：url
    * info：管理项目本身的一些基础信息
    * others：管理一些不成体系，但又必须记录的数据/信息
    * 所有的变量均采用单例的设计，即在该项目运行的进程内，仅会存在一个对应类型的变量
    * 变量是支持开发人员自行增加的(但不支持删减)，可以通过extends，在其真正绑定和影响项目时，为其添加变量，为快速开发提供便利
* defualt模块中存放的主要是内置的扩展(即extends)，包括app、配置、目录结构、路由能力等
  * app：为flask app提供支持，同时方便在特殊情况下，使用第三方所写就的更多类型的app进行替换
  * business、resource：规定该扩展规定了业务代码中必须包含business、resource两个文件目录，具体原因及设计初衷可见该扩展的注释
  * configuration：为业务代码所必须要进行的配置提供统一的支持与管理
  * router：为项目提供最基本的路由能力
* tamp仅作为临时目录，存放当前开发进行中所需的依赖，如自定义扩展所需实现的接口、目前已实现的，但不适合作为内置扩展的extend，后续将分别将其打做第三方包的形式为项目提供支持，目前仅作便利考虑，存放在本项目源代码目录中
* extend，作为项目的核心概念，其参考spring生态、flask生态、日常业务代码开发的各种小工具，为项目提供各式各样的能力，期望在此基础上，借助扩展的力量，实现业务代码的工程化和业务代码开发的便捷化；其本身要求必须依照规定的接口进行实现，包括scanner、container、logic、order
  * scanner：扫描器，用于扫描项目中指定位置的模块/文件，并读取目标数据/信息，以提供给container
  * container：存放扩展所需管理/操作的数据，建议在这一步当中，组合上述vars的能力，方便进行统一管理，同时，该概念本身也如同var一样，从某种程度上是为了方便定制该扩展对应数据所需的数据结构而产生
  * logic：对container所保存的数据进行统一处理，同时也是真正意义上扩展的能力集成到项目中这一过程的代码实现
  * order(可选)：该接口是否需要实现由扩展开发者自行决定；order本身是借助click，为项目添加各式各样命令行所用
  * extend有一个子类替代的机制，即：当在后续绑定到项目的扩展，出现了已有扩展的子类，且该子类的扩展名称变量name与父类相同(倘若name不同，则不会出现子类替代的现象)，则直接到该父类在var变量中的位置进行替换，而不在变量中进行追加

## 使用说明

* 项目运行：
  * 必须确保项目中，main文件同级存在resource、business两个文件夹/模块包(内置扩展business、resource规定)                              ![img_0.png](assets/img_0.png?t=1715328226489)
  * main文件必须导入并配置project，而后调用byorder方法
    ```
    from core import project


    project.setter_args(
        ip='0.0.0.0',
        port='8080',
        path=__file__
    )


    if __name__ == '__main__':
        project.byOrder()
    ```
  * 在命令行使用`python main.py run`运行项目，或者使用`python main.py shell`进入python shell进行验证，同时，也可以通过`python main.py --help`查看当前项目所支持的命令行
  * 也可以通过pycharm，为main文件添加脚本参数run/shell/--help直接进行运行或调试
* 扩展配置
  * 扩展配置可以通过调用project提供的setter_extend方法完成，且可以多次调用

    ```
    from core import project
    from tamp.extends.restful.container import RestfulContainer
    from tamp.extends.restful.logic import RestfulLogic
    from tamp.extends.restful.scanner import RestfulScanner


    project.setter_args(
        ip='0.0.0.0',
        port='8080',
        path=__file__
    ).setter_extend(
        RestfulScanner,
        RestfulContainer,
        RestfulLogic
    )


    if __name__ == '__main__':
        project.byOrder()

    ```
* app替换、参数配置可参考project初始化方法
  * ![image_1.png](assets/image_1.png?t=1715326870305)
* 所有setter方法均参考方法链思想，返回值均为对象本身，可连续调用
* 扩展编写(以restful举例)
  * scanner
    ```scanner.py
    import importlib
    import os
    import traceback

    from default.router.convention import RouterBasic
    from default.router.plan_0.scanner import Plan0RouterScanner
    from tamp.extends.restful.convertion import RestfulRouterBasic


    class RestfulScanner(Plan0RouterScanner):

        def scan(self, path_dir: str):
            cls_route = []

            for r, d, filenames in os.walk(path_dir):
                if 'business' not in r or 'router' not in r:
                    continue

                for filename in filenames:
                    if filename == '__init__.py' or not filename.endswith('.py'):
                        continue

                    try:
                        module = importlib.machinery.SourceFileLoader(
                            filename.replace(',py', ''), os.path.join(r, filename)
                        ).load_module()

                        class_imported = getattr(module, filename.replace('.py', ''))
                        if issubclass(class_imported, RouterBasic) or issubclass(class_imported, RestfulRouterBasic):
                            cls_route.append(class_imported)

                    except Exception:
                        print(traceback.format_exc())

            return cls_route

    ```
  * contaniner(借用了子类重载机制)
    ```container.py
    from default.router.plan_0.container import Plan0RouterContainer


    class RestfulContainer(Plan0RouterContainer):

        ...

    ```
  * logic(借用了子类重载机制)
    ```logic.py
    from default.router.plan_0.logic import Plan0RouterLogic


    class RestfulLogic(Plan0RouterLogic):

        ...

    ```
  * order(以内置模块router为例)
    ```order.py
    import click

    from core.vars.http import http
    from default.router.NameFactory import name_extend
    from tamp.interface.order import OrderAbs


    @click.command('routes')
    def routes():

        for route in http.query_router():

            click.echo(route)


    orders = [routes]


    class Plan0RouterOrder(OrderAbs):
        name = name_extend

        def get_orders(self) -> list:

            return orders

    ```

## 后续计划

* 补充内置extend——middle，为中间件的编写提供基础能力支持
* 参考spring生态各类集成，逐步增加各种extend
* 将扩展接口作为第三方包，支持pip下载，便于在不依赖本项目的前提下开发外部extend，并对当前项目做出对应调整
* 将tamp中的各类extends打作第三方包，支持pip下载
