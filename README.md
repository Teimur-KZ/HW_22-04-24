Урок 3. Работа с представлениями и шаблонами

Задание

Продолжаем работать с товарами и заказами.

Создайте шаблон, который выводит список заказанных клиентом товаров из всех его заказов с сортировкой по времени:

— за последние 7 дней (неделю)
— за последние 30 дней (месяц)
— за последние 365 дней (год)

Товары в списке не должны повторятся.

сделаны представления и прописана логика фильтрации:

https://github.com/Teimur-KZ/HW_22-04-24/blob/master/myapp/views.py

def client_orders_post(request, client_id)

def product_full(request, product_id)

сделаны шаблоны клиента и товаров: 

https://github.com/Teimur-KZ/HW_22-04-24/blob/master/myapp/templates/client_orders.html

https://github.com/Teimur-KZ/HW_22-04-24/blob/master/myapp/templates/product_full.html

