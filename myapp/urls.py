from django.urls import path
from . import views # импорт представлений из текущего пакета
from .views import index, about, error_404, client_orders_post

# настройка маршрутов

urlpatterns = [
    path('', views.index, name='index'), # путь к представлению index
    path('about/', views.about, name='about'), # путь к представлению about
    path('error_404/', views.error_404, name='error_404'), # путь к представлению error_404
    path('clients/<int:client_id>/', views.client_orders_post, name='client_orders'), # путь к представлению client_orders
    path('products/<int:product_id>/', views.product_full, name='product_full'),



]