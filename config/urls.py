# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedSimpleRouter

from wristband.stages.views import StagesViewSet
from wristband.apps.views import NestedAppViewSet, AppViewSet, DeployAppView
from wristband.common.views import login_view

router = DefaultRouter()
router.register(r'stages', StagesViewSet, base_name='stages')
router.register(r'apps', AppViewSet, base_name='apps')

stages_router = NestedSimpleRouter(router, r'stages', lookup='stage')
stages_router.register(r'apps', NestedAppViewSet, base_name='apps')


urlpatterns = [
    url(r'^login/$', login_view, name='login'),
    url(r'^logout/$', login_view, name='logout'),
    url(r'^api/', include(router.urls)),
    url(r'^api/', include(stages_router.urls)),
    url(r'^api/apps/(?P<app_name>.*)/stages/(?P<stage>.*)/version/(?P<version>.*)/', DeployAppView.as_view()),
    url(r'^docs/', include('rest_framework_swagger.urls'))


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        url(r'^400/$', 'django.views.defaults.bad_request'),
        url(r'^403/$', 'django.views.defaults.permission_denied'),
        url(r'^404/$', 'django.views.defaults.page_not_found'),
        url(r'^500/$', 'django.views.defaults.server_error'),
    ]
