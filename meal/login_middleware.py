import re
import logging
from django.conf import settings
from django.http.response import JsonResponse
from rest_framework.authentication import TokenAuthentication


class RequireLoginMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response
        self.api_required = tuple(re.compile(url) for url in settings.LOGIN_REQUIRED_API_URLS)
        self.api_exceptions = tuple(re.compile(url) for url in settings.LOGIN_REQUIRED_API_EXCEPTIONS)

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):

        # 尝试Token认证 拿到用户
        if not request.user.is_authenticated:
            try:
                result = TokenAuthentication().authenticate(request)
                if result:
                    user, token = result
                    request.user = user
            except Exception as e:
                logger = logging.getLogger()
                logger.warning(e)

        # No need to process URLs if user already logged in
        if request.user.is_authenticated:
            if not request.user.is_active:
                return json_response_suspended()
            return None
        for url in self.api_exceptions:
            if url.match(request.path):
                return None
        for url in self.api_required:
            if url.match(request.path):
                return json_response_unauthorized()
        # Explicitly return None for all non-matching requests
        return None


def json_response_unauthorized(message=''):
    if not message:
        message = '用户登录验证失败 检查Token'
    return JsonResponse({'resultCode': '10100', 'resultDesc': message}, status=401,
                        json_dumps_params={'ensure_ascii': False})


def json_response_suspended(message=''):
    if not message:
        message = '用户冻结'
    return JsonResponse({'resultCode': '10101', 'resultDesc': message}, status=401,
                        json_dumps_params={'ensure_ascii': False})
