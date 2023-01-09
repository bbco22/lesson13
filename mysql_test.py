import datetime
import uuid

from models import Users, Products, Tickets, Orders

# Добавляем товары в магазин
# Products.create(name="Картинка с котиком", cost=20, count=50)
# Products.create(name="Наклейка синего цвета", cost=15, count= 45)
# Products.create(name="Игральные кости (белые)", cost=25, count=25)

# Создаём тикеты
# ticket_uuid = str(uuid.uuid4())
# Tickets.create(uuid=ticket_uuid, avaliable=True, user_id=Users)
# print(Tickets.uuid)


print("   === Добро пожаловать в 'Не магазин' ===")
print()
print( "Здесь вы можете обменивать тикеты для того, чтобы приобретать товары")
print()
print("Для взаимодействия используйте команды:")
print("> Товары")
print("> Зарегистрироваться")
print("> Войти")

key = input("> ")

#
# query_prod = Products.select().execute()

# if key == "Товары" or key == "товары":
#     print(f"{'ID':<10}{'Стоимость':<20}{'Количество':<20}{'Название':<30}")
#     print("=" * 100)
#     for prod in query_prod:
#         if prod.count > 0:
#             print(f"{prod.id:<10}{prod.count:<20}{prod.cost:<20}{prod.name:<30}")
#
if key == "Зарегистрироваться" or key == "зарегистрироваться":
    user_log = input("Введите логин > ")
    user_pas = input("Введите пароль >  ")
    if Users.is_exist(user_log) == False:
        user_new = Users.create(username=user_log, password=user_pas, point=0)
        ticket_uuid = str(uuid.uuid4())
        Tickets.create(uuid=ticket_uuid, avaliable=True, user_id=user_new)
        print(Tickets.uuid)
    else:
        print("   === Добро пожаловать в 'Не Магазин' ===   ")
        print()
        print("Здесь вы можете обменивать тикеты для того, чтобы приобретать товары")
        print()
        print("для взаимодействия используйте команды:")
        print()
        print()
        print("> Товары")
        print("> Купить")
        print("> Профиль")
        print("> Тикет")

user_reg = Users.get(Users.username == user_log)
# Создали номера тикетов к уже созданным пользователям
# for user in Users.select().execute():
#     ticket_uuid = str(uuid.uuid4())
#     Tickets.create(uuid=ticket_uuid, avaliable=True, user_id=user)
#     print(user.username)

# смотрим какие тикеты есть уже у пользователей
for ticket in Tickets.select().execute():
    print(f"{ticket.user_id.username:<15}{ticket.uuid:<50}{ticket.user_id.point:<15}")

key = input("> ")

if key == "Тикет" or key == "тикет":
    promo= input("Введите ваш номер тикета: ")
    if Tickets.valid_ticket(promo) == True:
        Tickets.update(avaliable=False).where(Tickets.uuid == promo)
        print("Вы успешно обменяли тикет на 20 поинтов!"
              "Теперь у вас - 20 поинтов")
        Users.update(point=20).where(Users.username == user_log) #не работает
    else:
        print("Ваш тикет неактивен")


key = input("> ")

if key == "Купить" or key == "купить":
    new_id = input("товар: ")
    new_count = input("кол-во: ")
    new_order = Orders.create(user_id=user_reg, product_id=new_id, count=new_count, order_datetime=datetime.datetime.now())
    Products.update(count=(Products.count - new_count)).where(Orders.product_id == new_id)
    print(f"Вы успешно купили '{Orders.product_id.name}' в количестве: {new_count}")  # название продукта не выводится
    Users.update(Users.point - Products.cost).where(Orders.product_id == new_id)
    print(f"У вас осталось - {Users.point} поинтов")  # поинты не выводятся

key = input("> ")
if key == "Профиль" or key == "профиль":
    print("=== ", user_log, " ===")
    print("Поинтов: ", Users.point) # поинты не выводятся
    print()
    print("Заказы: ")
    print()
    print(f"{'Дата заказа':<50}{'Кол-во':<20}{'Сумма':<20}{'Название':<30}")
    print("-" * 120)
    for order in Orders.select().execute():
        order: Orders
        # ОШИБКА: отступ '<50'  в дате здесь не срабатывает
        print(f"{order.order_datetime}{order.count:<20}{order.product_id.cost:<20}{order.product_id.name:<30}")






