from datetime import datetime
from peewee import *

db = MySQLDatabase(database=, host="127.0.0.1", user="root", password=)


class Users(db.Model):
    username = CharField(max_length=40, unique=True)
    password = CharField(max_length=128)
    point = SmallIntegerField()

    @staticmethod
    def is_exist(username: str) -> bool:
        try:
            Users.get(Users.username == username)
        except Users.DoesNotExist:
            return False
        else:
            return True

    def orders(self):
        for order in Orders.select().execute():
            print(Orders.order_datetime, Orders.count, Orders.product_id.cost, Orders.product_id.name)


class Tickets(db.Model):
    uuid = CharField(max_length=128)
    avaliable = BooleanField
    user_id = ForeignKeyField(Users, field="id", on_delete="CASCADE")

    @staticmethod
    def valid_ticket(uuid) -> bool:
        try:
            Tickets.get(Tickets.uuid == uuid)
        except Tickets.DoesNotExist:
            return False
        else:
            return True


class Products(db.Model):
    name = CharField(max_length=100, null=False)
    cost = SmallIntegerField()
    count = SmallIntegerField()


class Orders(db.Model):
    user_id = ForeignKeyField(Users, field="id", on_delete="CASCADE")
    product_id = ForeignKeyField(Products, field="id")
    count = SmallIntegerField()
    order_datetime = DateTimeField()
