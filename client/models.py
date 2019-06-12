from django.db import models
from django.contrib.auth.models import User
from partner.models import Menu, Partner
from django.utils import timezone

# Create your models here.
class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(
        max_length=30,
        verbose_name = "고객 이름"
    )

    def __str__(self):
        return self.name

class Order(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    partner = models.ForeignKey(Partner, on_delete=models.CASCADE)
    contact = models.CharField(
        max_length=20,
        verbose_name = "연락처"
    )
    address = models.CharField(
        max_length=100,
        verbose_name = "주소"
    )
    requestment = models.CharField(
        max_length=30,
        verbose_name = "요청사항"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
         ordering = ['-created_at']

    items = models.ManyToManyField(
        Menu,
        through='OrderItem',
        through_fields=('order', 'menu'),
    )

    # is_delivered = models.BooleanField(default=False)
    # delivered_at = models.DateTimeField(null=True, blank=True, editable=True)
    # def deliver(self):
    #     self.is_delivered = True
    #     self.delivered_at = timezone.now()
    #     self.save()
    def __str__(self):
        return self.client.name

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    count = models.PositiveSmallIntegerField()
