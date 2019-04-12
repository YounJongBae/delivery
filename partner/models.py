from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Partner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    KOREAN = 'KR'
    WESTURN = 'WE'
    JAPANESE = 'JP'
    DESSERT = 'DE'
    FOOD_CATEGORY = (
        (KOREAN, '한식'),
        (WESTURN, '양식'),
        (JAPANESE, '일식'),
        (DESSERT, '디저트'),
    )

    category = models.CharField(
        max_length=10,
        choices=FOOD_CATEGORY,
        verbose_name = "카테고리"
    )

    name = models.CharField(
        max_length=30,
        verbose_name = "가게 이름"
    )
    contact= models.CharField(
        max_length=30,
        verbose_name = "연락처"
    )
    address = models.CharField(
        max_length=100,
        verbose_name = "주소"
    )
    description = models.TextField(
        verbose_name = "가게 소개"
    )
    image = models.ImageField(
        verbose_name = "가게 사진"
    )

    def __str__(self):
        return self.name

class Menu(models.Model):
    partner = models.ForeignKey('Partner', on_delete=models.CASCADE)
    name = models.CharField(
        max_length=30,
        verbose_name = "메뉴 이름"
    )
    price = models.PositiveIntegerField(
        verbose_name = "가격"
    )
    image = models.ImageField(
        verbose_name = "메뉴 이미지"
    )
    description = models.TextField(
        verbose_name = "메뉴 소개"
    )

    def __str__(self):
        return self.name
