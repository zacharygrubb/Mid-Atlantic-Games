from django.contrib import admin

from .models import Game, GameOrder, Cart, Post


class GameAdmin(admin.ModelAdmin):
    list_display = ('title', 'genre', 'price', 'stock')


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'publish_date', 'cover_image',
                    'content_one', 'content_two', 'content_three',
                    'image_one', 'image_two', 'image_three')


class GameOrderAdmin(admin.ModelAdmin):
    list_display = ('game', 'cart', 'quantity')


class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'active', 'order_date')


admin.site.register(Game, GameAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(GameOrder, GameOrderAdmin)
admin.site.register(Cart, CartAdmin)
