from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


def cover_upload_path(instance, filename):
    return '/'.join(['games', str(instance.id), filename])


class Game(models.Model):
    title = models.CharField(max_length=100)
    genre = models.CharField(max_length=50)
    description = models.TextField()
    publish_date = models.DateField(default=timezone.now)
    price = models.DecimalField(decimal_places=2, max_digits=8)
    stock = models.IntegerField(default=0)
    cover_image = models.ImageField(upload_to=cover_upload_path, default='games/empty_cover.jpg')


class Review(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    publish_date = models.DateField(default=timezone.now)
    text = models.TextField()


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    order_date = models.DateField(default=timezone.now, null=True)
    payment_type = models.CharField(max_length=100, null=True)
    payment_id = models.CharField(max_length=100, null=True)

    def add_to_cart(self, game_id):
        game = Game.objects.get(pk=game_id)
        try:
            preexisting_order = GameOrder.objects.get(game=game, cart=self)
            preexisting_order.quantity += 1
            preexisting_order.save()
        except GameOrder.DoesNotExist:
            new_order = GameOrder.objects.create(
                game=game,
                cart=self,
                quantity=1
            )
            new_order.save()

    def remove_from_cart(self, game_id):
        game = Game.objects.get(pk=game_id)
        try:
            preexisting_order = GameOrder.objects.get(game=game, cart=self)
            if preexisting_order.quantity > 1:
                preexisting_order.quantity -= 1
                preexisting_order.save()
            else:
                preexisting_order.delete()
        except GameOrder.DoesNotExist:
            pass


class GameOrder(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.IntegerField()
