from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth.models import User, Group
from django.shortcuts import render, redirect
from client.models import OrderItem, Order
from client.views import common_login, common_signup
from .forms import PartnerForm, MenuForm
from .models import Menu
import datetime
from datetime import datetime, timedelta
from django.utils import timezone


URL_LOGIN="/partner/login/"
def partner_group_check(user):
    return "partner" in [group.name for group in user.groups.all()]
# Create your views here.
def index(request):
    ctx = {"is_partner":True}
    if request.method == "GET":
        partner_form = PartnerForm()
        ctx.update({"form" : partner_form})
    elif request.method == "POST":
        partner_form = PartnerForm(request.POST, request.FILES)
        if partner_form.is_valid():
            partner = partner_form.save(commit=False)
            partner.user = request.user
            partner.save()
            return redirect("/partner/")
        else:
            ctx.update({"form" : partner_form})

    return render(request, "index.html", ctx)

def login(request):
    ctx = {"is_partner":True}
    return common_login(request, ctx, "partner")

def signup(request):

        # if email is not None:
        #     user.email = email
        #     user.save()
        # else:
        #     user.email = default
        #     user.save()

    ctx = {"is_partner":True}
    return common_signup(request, ctx, "partner")

def logout(request):
    auth_logout(request)
    return redirect("/partner/")

@login_required(login_url=URL_LOGIN)
@user_passes_test(partner_group_check, login_url=URL_LOGIN)
def edit_info(request):
    ctx = {"is_partner":True}
    if request.method == "GET":
        partner_form = PartnerForm(instance=request.user.partner)
        ctx.update({"form" : partner_form})
    elif request.method == "POST":
        partner_form = PartnerForm(request.POST, request.FILES, instance=request.user.partner)
        if partner_form.is_valid():
            partner = partner_form.save(commit=False)
            partner.user = request.user
            partner.save()
            return redirect("/partner/")
        else:
            ctx.update({"form" : partner_form})

    return render(request, "edit_info.html", ctx)

@login_required(login_url=URL_LOGIN)
@user_passes_test(partner_group_check, login_url=URL_LOGIN)
def menu(request):
    ctx = {"is_partner":True}
    menu_list = Menu.objects.filter(partner=request.user.partner)
    ctx.update({"menu_list":menu_list})

    return render(request, "menu_list.html", ctx)

@login_required(login_url=URL_LOGIN)
@user_passes_test(partner_group_check, login_url=URL_LOGIN)
def menu_add(request):
    ctx = {"is_partner":True}
    if request.method == "GET":
        form = MenuForm()
        ctx.update({"form" : form})
    elif request.method == "POST":
        form = MenuForm(request.POST, request.FILES)
        if form.is_valid():
            menu = form.save(commit=False)
            menu.partner = request.user.partner
            menu.save()
            return redirect("/partner/menu/")
        else:
            ctx.update({"form" : form})

    return render(request, "menu_add.html", ctx)

@login_required(login_url=URL_LOGIN)
@user_passes_test(partner_group_check, login_url=URL_LOGIN)
def menu_detail(request, menu_id):
    ctx= {"is_partner":True}
    menu = Menu.objects.get(id=menu_id)
    ctx.update({"menu" : menu})

    return render(request, "menu_detail.html", ctx)

@login_required(login_url=URL_LOGIN)
@user_passes_test(partner_group_check, login_url=URL_LOGIN)
def menu_edit(request, menu_id):
    ctx = { "replacement" : "수정",
            "is_partner":True,
     }
    menu = Menu.objects.get(id=menu_id)
    if request.method == "GET":
        form = MenuForm(instance=menu)
        ctx.update({"form" : form})
    elif request.method == "POST":
        form = MenuForm(request.POST, request.FILES, instance=menu)
        if form.is_valid():
            menu = form.save(commit=False)
            menu.partner = request.user.partner
            menu.save()
            return redirect("/partner/menu/")
        else:
            ctx.update({"form" : form})

    return render(request, "menu_add.html", ctx)

@login_required(login_url=URL_LOGIN)
@user_passes_test(partner_group_check, login_url=URL_LOGIN)
def menu_delete(request, menu_id):
    menu = Menu.objects.get(id=menu_id)
    menu.delete()
    return redirect("/partner/menu/")

def order(request):
    ctx = {"is_partner":True}
    # menu_list = Menu.objects.filter(partner=request.user.partner)
    # item_list = []
    # for menu in menu_list:
    #     item_list.extend([item for item in OrderItem.objects.filter(menu=menu, delivered_at__lte=timezone.now()).order_by('delivered_at')])
    # order_set = set([item.order for item in item_list])
    # item_set = set([item for item in item_list])
    orders = Order.objects.filter(partner=request.user.partner, created_at__lte=timezone.now()).order_by('-created_at')
    item_list = []
    for order in orders:
        item_list.extend([item for item in OrderItem.objects.filter(order=order).distinct()])
    # item_set = (item for item in item_list)
    # menu_list = Menu.objects.filter(partner=partner_dict)
    # orders = Order.objects.filter(partner=request.user.partner)
    # order_dict = {}
    # for order in orders:
    #     date_and_hour = order.created_at.now()
    #     if date_and_hour in order_dict:
    #         order_dict[date_and_hour].append(order)
    #     else:
    #         order_dict[date_and_hour] = [ order ]
    #     order_list = Order.objects.filter(delivered_at=date_and_hour)

    ctx.update({
        "item_list" : item_list,
    })
    return render(request, "order_list_for_partner.html", ctx)
