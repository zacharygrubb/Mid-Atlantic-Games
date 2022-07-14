from django.contrib import admin

from .models import Game, GameOrder, Cart


class GameAdmin(admin.ModelAdmin):
    list_display = ('title', 'genre', 'price', 'stock')


class GameOrderAdmin(admin.ModelAdmin):
    list_display = ('game', 'cart', 'quantity')


class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'active', 'order_date')


admin.site.register(Game, GameAdmin)
admin.site.register(GameOrder, GameOrderAdmin)
admin.site.register(Cart, CartAdmin)
