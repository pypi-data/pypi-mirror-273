import click

from flask_projects.core.vars.http import http
from flask_projects.default.router.NameFactory import name_extend
from flask_projects.interface.order import OrderAbs


@click.command('routes')
def routes():

    for route in http.query_router():

        click.echo(route)


orders = [routes]


class Plan0RouterOrder(OrderAbs):
    name = name_extend

    def get_orders(self) -> list:

        return orders
