# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     urls
   Description :
   Author :       Administrator
   date：          2019/5/20 0020
-------------------------------------------------
   Change Activity:
                   2019/5/20 0020:
-------------------------------------------------
"""
from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from . import views
router = DefaultRouter()
router.register(r'reserves',  views.ReserveViewSet, base_name='reserves')
router.register(r'banners',  views.BannerViewSet, base_name='banners')
router.register(r'dishes',  views.DishesListViewSet, base_name='dishes')
router.register(r'types',  views.DishesTypeViewSet, base_name='types')
urlpatterns = [
    url(r'openid/', views.GetOpenid.as_view()),
    url(r'users/', views.Users.as_view()),
    url(r'forms/', views.Form.as_view()),
    url(r'^api/', include(router.urls)),
]
