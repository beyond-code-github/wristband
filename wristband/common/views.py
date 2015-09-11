from django.http import HttpResponse
from django.views.decorators.http import require_GET


@require_GET
def healthcheck_view(request):
    return HttpResponse()
