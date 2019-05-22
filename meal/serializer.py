# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     serializer
   Description :
   Author :       Administrator
   date：          2019/5/20 0020
-------------------------------------------------
   Change Activity:
                   2019/5/20 0020:
-------------------------------------------------
"""
from .models import *
from rest_framework import serializers
import django_filters


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInfo
        fields = '__all__'


class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = '__all__'


class ReserveSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReserveStatus
        fields = '__all__'
        depth = 1

    def create(self, validated_data):
        return ReserveStatus.objects.create(user=self.context['user'], **validated_data)


class DishesListSerializer(serializers.ModelSerializer):
    class Meta:
        model = DishesList
        fields = '__all__'
        depth = 1


class DishesTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DishesType
        fields = '__all__'
