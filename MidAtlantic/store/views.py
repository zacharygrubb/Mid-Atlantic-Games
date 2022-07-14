from django.shortcuts import render, redirect
from .models import Game, Cart, Review, GameOrder
from django.core.exceptions import ObjectDoesNotExist


def index(request):
    return render(request, 'template.html')


def store(request):
    games = Game.objects.all()
    context = {
        'games': games,
    }
    return render(request, "base.html", context)


def game_details(request, game_id):
    context = {
        'game': Game.objects.get(pk=game_id),
    }
    return render(request, 'store/detail.html', context)


def add_to_cart(request, game_id):
    if request.user.is_authenticated:
        try:
            game = Game.objects.get(pk=game_id)
        except ObjectDoesNotExist:
            pass
        else:
            try:
                cart = Cart.objects.get(user=request.user, active=True)
            except ObjectDoesNotExist:
                cart = Cart.objects.create(
                    user=request.user
                )
                cart.save()
            cart.add_to_cart(game_id)
        return redirect('cart')
    else:
        return redirect('index')


def remove_from_cart(request, game_id):
    if request.user.is_authenticated:
        try:
            game = Game.objects.get(pk=game_id)
        except ObjectDoesNotExist:
            pass
        else:
            cart = Cart.objects.get(user=request.user, active=True)
            cart.remove_from_cart(game_id)
        return redirect('cart')
    else:
        return redirect('index')


def cart(request):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user.id, active=True)[0]
        orders = GameOrder.objects.filter(cart=cart)
        total = 0
        count = 0
        for order in orders:
            total = (order.game.price * order.quantity)
            count = order.quantity
        context = {
            'cart': orders,
            'total': total,
            'count': count,
        }
        return render(request, 'store/cart.html', context)
    else:
        return redirect('index')
