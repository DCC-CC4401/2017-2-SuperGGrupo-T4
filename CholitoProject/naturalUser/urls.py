from django.conf import settings
from django.conf.urls import include, url

from .views import *

urlpatterns = [
    url(r'^login/$', LogInView.as_view(), name='login'),
    url(r'^signup/$', SignUpView.as_view(), name='signup'),
    url(r'^$', IndexView.as_view(), name='user-index'),
    url(r'^user/$', UserDetail.as_view(), name='user-update'),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
                      url(r'^__debug__/', include(debug_toolbar.urls)),
                  ] + urlpatterns
