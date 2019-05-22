from django.db import models


# Create your models here.

class UserInfo(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    openid = models.CharField(max_length=100, blank=True, null=True)
    image = models.CharField(max_length=400, blank=True, null=True)
    role = models.IntegerField(choices=((0, '员工'), (1, '厨师')), default=0)

    class Meta:
        verbose_name_plural = '用户信息'
        db_table = 'user'

    def __str__(self):
        return self.name if self.name else self.openid


class ReserveStatus(models.Model):
    num = models.CharField(max_length=32)
    status = models.IntegerField(choices=((0, '未预定'), (1, ' 已预订')), default=0)
    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE, related_name='status')
    create = models.DateField(auto_now=True)

    class Meta:
        verbose_name_plural = '预订信息'
        db_table = 'reserve'


class Banner(models.Model):
    image = models.ImageField(upload_to='banner/')

    class Meta:
        verbose_name_plural = 'banner信息'
        db_table = 'banner'


class DishesType(models.Model):
    name = models.CharField(max_length=32)
    image = models.ImageField(upload_to='type/')

    class Meta:
        verbose_name_plural = '菜单信息'
        db_table = 'dishes_type'

    def __str__(self):
        return self.name


class DishesList(models.Model):
    types = models.IntegerField(choices=((0, '早餐'), (1, '午餐'), (2, '晚餐')))
    dishes = models.ForeignKey(DishesType, on_delete=models.CASCADE, related_name='list')
    create = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name_plural = '菜品选择'
        db_table = 'dishes_list'

    def __str__(self):
        return self.dishes.name


class FormId(models.Model):
    forId = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'formID表'
        db_table = 'form'
