from django.contrib.auth import authenticate, logout
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST
from rest_framework.authtoken.views import ObtainAuthToken as OriginalObtainAuthToken
from rest_framework.response import Response

from wristband.authentication.utils import login
from wristband.authentication.models import Token


@require_POST
@csrf_exempt
def login_view(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        data = {'session_key': request.session.session_key}
        status = 200
    else:
        data = {'details': 'Invalid credential details'}
        status = 401  # forbidden
    return JsonResponse(data=data, status=status)


@require_GET
def logout_view(request):
    logout(request)
    data = {'message': 'User logged out'}
    return JsonResponse(data=data)


class ObtainAuthToken(OriginalObtainAuthToken):
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})
