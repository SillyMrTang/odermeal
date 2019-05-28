from django.shortcuts import render
from django.views import View
from OderMeal import settings
from django.http import JsonResponse
from django.db.models import Q
from django.core.serializers import serialize
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import UserInfo, ReserveStatus, FormId, Banner, DishesType, DishesList
from .serializer import ReserveSerializer, BannerSerializer, DishesListSerializer, DishesTypeSerializer
import requests
import json
import datetime


# Create your views here.
class GetOpenid(View):
    """
    获取openid返回
    """

    def get(self, request):
        code = request.GET.get('code')
        params = {
            'appid': settings.APPID,
            'secret': settings.AppSECRET,
            'js_code': code,
            'grant_type': 'authorization_code'
        }
        response = requests.get('https://api.weixin.qq.com/sns/jscode2session', params=params).json()
        print(response)
        try:
            user = UserInfo.objects.filter(openid=response['openid'])
            if user:
                pass
            else:
                user = UserInfo()
                user.openid = response['openid']
                user.save()
        except AttributeError as e:
            pass
        return JsonResponse(response)


class Users(View):
    """
    根据openid对user信息进行存储
    """

    def get(self, request):
        openid = request.GET.get('openid')
        data = serialize('json', UserInfo.objects.filter(openid=openid))
        return JsonResponse(json.loads(data), safe=False)

    def post(self, request):
        print(request.body)
        data = json.loads(request.body)
        openid = data['openid']
        name = data['name']
        image = data['image']
        user = UserInfo.objects.filter(openid=openid)
        if user:
            user[0].name = name
            user[0].image = image
            user[0].save()
        return JsonResponse({'res': 'ok'})


class ReserveViewSet(viewsets.ModelViewSet):
    """
    预订当日餐，利用filter过滤进行查询
    create serializer进行保存
    """
    queryset = ReserveStatus.objects.all()
    serializer_class = ReserveSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('status', 'user', 'create')

    def create(self, request, *args, **kwargs):
        user_id = request.data['user']
        user = UserInfo.objects.get(id=user_id)
        serializer = ReserveSerializer(data=request.data, context={'user': user})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Form(View):
    """
    formId 的保存
    """

    def post(self, request):
        data = json.loads(request.body)
        form_id = data['form']
        form = FormId()
        form.forId = form_id
        form.save()
        return JsonResponse({"res": 'ok'})


class BannerViewSet(viewsets.ModelViewSet):
    """
    banner管理
    """
    queryset = Banner.objects.all()
    serializer_class = BannerSerializer


class DishesTypeViewSet(viewsets.ModelViewSet):
    """
    菜谱管理
    """
    queryset = DishesType.objects.all()
    serializer_class = DishesTypeSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('types',)


class DishesListViewSet(viewsets.ModelViewSet):
    """
    每日菜单查询，利用filter过滤器
    """
    queryset = DishesList.objects.all()
    serializer_class = DishesListSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('types', 'create')

    def create(self, request, *args, **kwargs):
        for i in request.data['dishe']:
            dishe = DishesList()
            types = DishesType.objects.get(id=i)
            dishe.types = request.data['types']
            dishe.dishes = types
            dishe.save()
        return JsonResponse({'code': 200})
