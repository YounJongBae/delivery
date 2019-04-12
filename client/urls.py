from django.conf.urls import url, include
from .views import (
    index, signup, login, order, signup_cong, order_client, logout,
)

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^signup/$', signup, name='signup'),
    url(r'^login/$', login, name='login'),
    url(r'^(?P<partner_id>\d+)/$', order, name='order'),
    url(r'^signup/cong/$', signup_cong, name='signup_cong'),
    url(r'^logout/$', logout, name='logout'),
    url(r'^order/$', order_client, name='order_client'),
]
