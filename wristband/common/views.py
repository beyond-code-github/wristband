from django.contrib.auth import authenticate, logout
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from wristband.authentication.utils import login


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
        data = {'message': 'Invalid credential details'}
        status = 403 #forbidden
    return JsonResponse(data=data, status=status)


@csrf_exempt
def logout_view(request):
    logout(request)
    data = {'message': 'User logged out'}
    return JsonResponse(data=data)

