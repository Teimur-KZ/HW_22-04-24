from django.shortcuts import render

# Create your views here.
import logging
from django.shortcuts import render, get_object_or_404
from .models import Client, Order, Product
from datetime import datetime, timedelta
import django.utils.timezone

logger = logging.getLogger(__name__) # создание объекта логгера

# Представление главной страницы
def index(request): # определение представления index
    logger.info('Страница "Главная страница" была посещена') # запись сообщения в лог
    html = """
    <h1>Главная страница</h1>
    <p>Фреймворк Django - Урок 3. Работа с представлениями и шаблонами</p>
    <p>Задание:</p>
    <p>
    Создайте шаблон, который выводит список заказанных клиентом товаров из всех его заказов с сортировкой по времени:
    </p><p>
    — за последние 7 дней (неделю)
    </p><p>
    — за последние 30 дней (месяц)
    </p><p>
    — за последние 365 дней (год)
    </p><p>
    Товары в списке не должны повторятся.
    </p>
    """
    title = "Главная страница"
    return render(request, 'index.html', {'html': html, 'title': title}) # возврат ответа

# Представление "О себе"
def about(request):
    # Логирование данных о посещении страницы
    logger.info('Страница "О себе" была посещена')

    html = """
    <h1>Обо мне</h1>
    <p>Информация о себе....</p>
    <p>Меня зовут Теймур - это домашнее задание по Django.</p>
    """
    title = "О себе"
    return render(request, 'about.html', {'html': html, 'title': title})

# Обработчик ошибки 404
def error_404(request, exception):
    #return render(request, '404.html', status=404) или так:
    logger.error(f'Страница не найдена')
    title = 'Страница не найдена'
    return render(request, '404.html', {'title': title}, status=404)

'''Задание:
Создайте шаблон, который выводит список заказанных клиентом товаров из всех его заказов с сортировкой по времени:

— за последние 7 дней (неделю)

— за последние 30 дней (месяц)

— за последние 365 дней (год)

Товары в списке не должны повторятся
'''


'''работа с командами через view'''
def client_orders_post(request, client_id):
    client = get_object_or_404(Client, pk=client_id)
    orders = Order.objects.filter(client=client)
    request.session['client_id'] = client_id # сохраняем id клиента в сессии, что бы мог вернуться на страницу клиента из товара

    # Получаем текущую дату и время
    #now = datetime.now()
    now = django.utils.timezone.now()

    # Создаем словарь для хранения товаров за разные периоды времени
    products_by_time = {
        'week': set(),
        'month': set(),
        'year': set(),
        'count_orders_week': 0,
        'count_orders_month': 0,
        'count_orders_year': 0,
        'sum_orders_week': 0,
        'sum_orders_month': 0,
        'sum_orders_year': 0,
    }

    # Проходим по каждому заказу
    for order in orders:
        # Получаем товары из заказа
        products = Product.objects.filter(order=order)

        # Сортируем товары по времени и добавляем в соответствующие списки
        for product in products:
            if order.order_data >= now - timedelta(days=7):
                products_by_time['week'].add(product)
                products_by_time['count_orders_week'] += 1
                products_by_time['sum_orders_week'] += order.total_price * order.quantity # сумма заказа за неделю
            elif order.order_data >= now - timedelta(days=30):
                products_by_time['month'].add(product)
                products_by_time['count_orders_month'] += 1
                products_by_time['sum_orders_month'] += order.total_price * order.quantity # сумма заказа за месяц
            elif order.order_data >= now - timedelta(days=365):
                products_by_time['year'].add(product)
                products_by_time['count_orders_year'] += 1
                products_by_time['sum_orders_year'] += order.total_price * order.quantity # сумма заказа за год

    #print(products_by_time, 'products_by_time') # вывод в консоль - проверка
    return render(request, 'client_orders.html', {'client': client, 'products_by_time': products_by_time, 'orders': orders})

def product_full(request, product_id):
    product = get_object_or_404(Product, pk=product_id) # объект товара по его id
    client_id = request.session.get('client_id')
    client = get_object_or_404(Client, pk=client_id) # объект клиента по его id
    return render(request, 'product_full.html', {'product': product, 'client': client, 'title': 'Полный товар', 'price': product.price, 'add_data': product.add_data})

# Запуск сервера: py manage.py runserver