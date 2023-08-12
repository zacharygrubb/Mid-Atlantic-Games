import paypalrestsdk
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.urls import reverse
from django.utils import timezone

from .models import Game, Cart, GameOrder, Post


def index(request):
    return render(request, 'template.html')


def home(request):
    games = Game.objects.all()
    posts = Post.objects.all()
    context = {
        'games': games,
        'posts': posts,
    }
    return render(request, "base.html", context)


def store(request):
    games = Game.objects.all()
    context = {
        'games': games,
    }
    return render(request, "store.html", context)


def about(request):
    posts = Post.objects.all()
    context = {
        'posts': posts,
    }
    return render(request, "about.html", context)


def blog(request):
    posts = Post.objects.all()
    context = {
        'posts': posts,
    }
    return render(request, "blog.html", context)


def game_details(request, game_id):
    context = {
        'game': Game.objects.get(pk=game_id),
    }
    return render(request, 'store/detail.html', context)


def post(request, post_id):
    context = {
        'post': Post.objects.get(pk=post_id),
    }
    return render(request, 'blog/post.html', context)


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
            total += (order.game.price * order.quantity)
            count = order.quantity
        context = {
            'cart': orders,
            'total': total,
            'count': count,
        }
        return render(request, 'store/cart.html', context)
    else:
        return redirect('index')


def checkout(request, processor):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user.id, active=True)[0]
        orders = GameOrder.objects.filter(cart=cart)
        if processor == "paypal":
            redirect_url = checkout_paypal(request, cart, orders)
            return redirect(redirect_url)
    else:
        return redirect('index')


def checkout_paypal(request, cart, orders):
    if request.user.is_authenticated:
        items = []
        total = 0
        for order in orders:
            total += (order.game.price * order.quantity)
            game = order.game
            item = {
                'name': game.title,
                'sku': game.id,
                'price': str(game.price),
                'currency': 'USD',
                'quantity': order.quantity
            }
            items.append(item)

        paypalrestsdk.configure({
          "mode": "sandbox",
          "client_id": "AWxrKbNz6vKvsTIlkK5FX1t0CLdYVqbS0nXhJ0b8ULhKJOdQyockDfj69NHiq0e-FZadj4tqujkrifkD",
          "client_secret": "EDdFuE0cvlT0f554rMhHU7WZs5BQdZSksydMi0MZ4Vxpqox9ZOaJ5fYdc_lLNKE0yeIeh_Tbe6JWQ8sI" })
        payment = paypalrestsdk.Payment({
            "intent": "sale",
            "payer": {
                "payment_method": "paypal"},
            "redirect_urls": {
                "return_url": "http://localhost:8000/store/process/paypal",
                "cancel_url": "http://localhost:8000/store"},
            "transactions": [{
                "item_list": {
                    "items": items},
                "amount": {
                    "total": str(total),
                    "currency": "USD"},
                "description": "Mid Atlantic Games order."}]})
        if payment.create():
            cart.payment_id = payment.id
            cart.save()
            for link in payment.links:
                if link.method == "REDIRECT":
                    redirect_url = str(link.href)
                    return redirect_url
        else:
            return reverse('order_error')
    else:
        return redirect('index')


def order_error(request):
    if request.user.is_authenticated:
        return render(request, 'store/order_error.html')
    else:
        return redirect('index')


def process_order(request, processor):
    if request.user.is_authenticated:
        if processor == "paypal":
            payment_id = request.GET.get('paymentId')
            cart = Cart.objects.filter(payment_id=payment_id)[0]
            orders = GameOrder.objects.filter(cart=cart)
            total = 0
            for order in orders:
                total += (order.game.price * order.quantity)
            context = {
                'cart': orders,
                'total': total,
            }
            return render(request, 'store/process_order.html', context)
        elif processor == "stripe":
            return JsonResponse({'redirect_url': reverse('complete_order', args=['stripe'])})
        else:
            return redirect('index')


def complete_order(request, processor):
    if request.user.is_authenticated:
        cart = Cart.objects.get(user=request.user.id, active=True)
        if processor == 'paypal':
            payment = paypalrestsdk.Payment.find(cart.payment_id)
            if payment.execute({"payer_id": payment.payer.payer_info.payer_id}):
                message = "Success! Your order has been completed, and is being processed. Payment ID: %s" % (payment.id)
                cart.active = False
                cart.order_date = timezone.now()
                cart.payment_type = "Paypal"
                cart.save()
            else:
                message = "There was a problem with the transaction. Error: %s" % (payment.error.message)
            context = {
                'message': message,
            }
            return render(request, 'store/order_complete.html', context)
    else:
        return redirect('index')
