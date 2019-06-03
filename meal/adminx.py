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
from .models import DishesType, Banner, RemindTime, TemplateReceiver, UserInfo, DishesList, ReserveStatus
import xadmin


class DishesAdmin(object):
    list_display = ['id', 'name', 'image', 'types']
    search_fields = ['name', ]
    ordering = ('id',)


class DishesListAdmin(object):
    list_display = ['id', 'types', 'dishes', 'create']
    search_fields = ['dishes', ]
    ordering = ('id',)


class UserAdmin(object):
    list_display = ['id', 'name', 'openid']
    search_fields = ['name', ]
    ordering = ('id',)


class BannerAdmin(object):
    list_display = ['id', 'image']
    search_fields = ['id', ]
    ordering = ('id',)


class TemplateAdmin(object):
    list_display = ['id', 'user']
    search_fields = ['user__name', ]
    ordering = ('id',)


class ReserveAdmin(object):
    list_display = ['id', 'num', 'status', 'user', 'create']
    list_filter = ['status']
    search_fields = ['create', 'status']
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
    """
    修改后台标题
    修改后台页脚
    设置菜单折叠
    """
    site_title = "食堂后台管理"
    # site_footer = '我的公司'
    # menu_style = "accordion"


xadmin.site.register(views.CommAdminView, GlobalSettings)
xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(DishesType, DishesAdmin)
xadmin.site.register(DishesList, DishesListAdmin)
xadmin.site.register(Banner, BannerAdmin)
xadmin.site.register(TemplateReceiver, TemplateAdmin)
xadmin.site.register(RemindTime, TimeAdmin)
xadmin.site.register(UserInfo, UserAdmin)
xadmin.site.register(ReserveStatus, ReserveAdmin)
