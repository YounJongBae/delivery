from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth.models import User, Group
from django.shortcuts import render, redirect
from partner.models import Partner, Menu
from .models import Client, Order, OrderItem
import random
import datetime
from django.utils import timezone
from django.db.models import Sum, F, ExpressionWrapper

URL_LOGIN="/login/"

# Create your views here.
def index(request):
    ctx = {"is_client":True}
    category = request.GET.get("category")

    if not category:
        partner_list = Partner.objects.all()
    else:
        partner_list = Partner.objects.filter(category=category)
        category_list = set([
            partner.get_category_display()
            for partner in partner_list
        ])
        ctx.update({"category_list" : category_list})

    list_partner = Partner.objects.all()
    list_category = [partner.category for partner in list_partner]
    choice = random.choice(list_category)

    ctx.update({
        "partner_list" : partner_list,
        "choice" : choice,
    })
    return render(request, "main.html", ctx)

def common_login(request, ctx, group):
    if request.method == "GET":
        pass
    elif request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)
        if user is not None:
            if group not in [group.name for group in user.groups.all()]:
                ctx.update({"error" : "접근 권한이 없습니다."})
                # for group in user.groups.all():
                #     print("group:",group)
            else:
                auth_login(request, user)
                next_value = request.GET.get("next")
                if next_value:
                    return redirect(next_value)
                else:
                    if group == "partner":
                        return redirect("/partner/")
                    else:
                        return redirect("/")
        else:
            ctx.update({"error" : "사용자가 없습니다."})

    return render(request, "login.html", ctx)

def login(request):
    ctx = {"is_client":True}
    return common_login(request, ctx, "client")

def common_signup(request, ctx, group):
    if request.method == "GET":
        pass
    elif request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = User.objects.create_user(username, email, password)
        target_group = Group.objects.get(name=group)
        user.groups.add(target_group)

        if group == "client":
            Client.objects.create(user=user, name=username)

        return redirect("/signup/cong/")

    return render(request, "signup.html", ctx)

def signup(request):
    ctx = {"is_client":True}
    return common_signup(request, ctx, "client")

def signup_cong(request):
    ctx = {}
    return render(request, "signup_cong.html", ctx)

def logout(request):
    auth_logout(request)
    return redirect("/")

@login_required(login_url=URL_LOGIN)
def order(request, partner_id):
    ctx = {"is_client":True}
    partner = Partner.objects.get(id=partner_id)
    menu_list = Menu.objects.filter(partner=partner)
    if request.method == "GET":
        ctx.update({
            "partner": partner,
            "menu_list": menu_list,
        })
    elif request.method == "POST":
        # contact = request.POST.get('contact')
        # address = request.POST.get('address')
        # requestment = request.POST.get('requestment')
        order = Order.objects.create(
            client=request.user.client,
            partner=partner,
            contact="contact",
            address="address",
            requestment="requestment",
        )
        for menu in menu_list:
            menu_count = request.POST.get(str(menu.id))
            menu_count = int(menu_count)
            if menu_count > 0:
                item = OrderItem.objects.create(
                    order=order,
                    menu=menu,
                    count=menu_count
                )

            return redirect("/")

    return render(request, "order_menu_list.html", ctx)

def order_client(request):
    ctx = {"is_client":True}
    orders = Order.objects.filter(client=request.user.client, created_at__lte=timezone.now())
    item_list = []
    for order in orders:
        # item_list.extend([item for item in OrderItem.objects.filter(order=order).distinct()])
        for item in OrderItem.objects.filter(order=order).distinct():
            item.menu.price *= item.count
            item.save()
            item_list.extend([item])


    ctx.update({
        "item_list" : item_list,
    })

    return render(request, "order_list_for_client.html", ctx)
