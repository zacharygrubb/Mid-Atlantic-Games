from . import views
from django.urls import path

urlpatterns = [
    path('', views.store, name='store'),
    path('index', views.index, name='index'),
    path('game/<int:game_id>', views.game_details, name='game_details'),
    path('add/<int:game_id>', views.add_to_cart, name='add_to_cart'),
    path('remove/<int:game_id>', views.remove_from_cart, name='remove_from_cart'),
    path('cart', views.cart, name='cart'),
]
