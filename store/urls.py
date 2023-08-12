from . import views
from django.urls import path

urlpatterns = [
    path('', views.home, name='home'),
    path('store/', views.store, name='store'),
    path('about/', views.about, name='about'),
    path('blog/', views.blog, name='blog'),
    path('index', views.index, name='index'),
    path('game/<int:game_id>', views.game_details, name='game_details'),
    path('add/<int:game_id>', views.add_to_cart, name='add_to_cart'),
    path('remove/<int:game_id>', views.remove_from_cart, name='remove_from_cart'),
    path('post/<int:post_id>', views.post, name='post'),
    path('cart/', views.cart, name='cart'),
    path('checkout/<processor>', views.checkout, name='checkout'),
    path('store/process/<processor>', views.process_order, name='process_order'),
    path('order_error', views.order_error, name='order_error'),
    path('complete_order/<processor>', views.complete_order, name='complete_order'),
]
