import click
from flask_projects.core.proj.abs import ProjectAbs
from flask_projects.core.order.unity import orders


@click.group()
def executor():
    msg = r"""
                                      _ooOoo_
                                     o8888888o
                                    888" . "888
                                   ( |  -_-  | )
                                    O\   =   /O
                                   ___/`---'\___
                                  . ' \\| |// ` .
                                 / \\||| : |||// \
                               / _||||| -:- |||||- \
                                 | | \\\ - /// | |
                               | \_| ''\---/'' | |  |
                                \ .-\__ `-` ___/-. /
                             ___`. .' /--.--\ `. . __
                          ."" '< `.___\_<|>_/___.' >'"".
                         | | : `- \`.;`\ _ /`;.`/ - ` : | |
                           \ \ `-. \_ __\ /__ _/ .-` / /
                   ======`-.____`-.___\_____/___.-`____.-'======
                                      `=---='
                   .............................................
                            佛祖保佑             永无BUG
                   .............................................
    """

    click.echo(msg)


def unity_order_loader(e):
    for order in orders:
        e.add_command(order)


def extends_order_loader(e, project: ProjectAbs):
    extends = project.extends

    commands = []
    for name in extends.query_names_order():
        commands.extend(extends.query_order(name).get_orders())

    for command in commands:
        e.add_command(command)


def loader(project: ProjectAbs):
    e = executor
    unity_order_loader(e)
    extends_order_loader(e, project)

    return e
