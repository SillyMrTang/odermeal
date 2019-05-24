# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     adminx
   Description :
   Author :       Administrator
   date：          2019/5/21 0021
-------------------------------------------------
   Change Activity:
                   2019/5/21 0021:
-------------------------------------------------
"""
from xadmin import views
from .models import DishesType, Banner, RemindTime, TemplateReceiver
import xadmin


class DishesAdmin(object):
    list_display = ['id', 'name', 'image']
    search_fields = ['name', ]
    ordering = ('id',)


class BannerAdmin(object):
    list_display = ['id', 'image']
    search_fields = ['id', ]
    ordering = ('id',)


class TemplateAdmin(object):
    list_display = ['id', 'user']
    search_fields = ['user', ]
    ordering = ('id',)


class TimeAdmin(object):
    list_display = ['id', 'breakfast_time', 'lunch_time', 'dinner_time']
    search_fields = ['id', ]
    ordering = ('id',)


class BaseSetting(object):
    """xadmin的基本配置"""
    enable_themes = True  # 开启主题切换功能
    use_bootswatch = True  # 支持切换主题


class GlobalSettings(object):
    """修改后台标题"""
    site_title = "食堂后台管理"


xadmin.site.register(views.CommAdminView, GlobalSettings)
xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(DishesType, DishesAdmin)
xadmin.site.register(Banner, BannerAdmin)
xadmin.site.register(TemplateReceiver, TemplateAdmin)
xadmin.site.register(RemindTime, TimeAdmin)
