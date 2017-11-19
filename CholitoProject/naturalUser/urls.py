from django.conf import settings
from django.conf.urls import include, url

from naturalUser.views import LogInView, SignUpView, IndexView, UserDetail, \
    ONGListView, AnimalListView

urlpatterns = [
    url(r'^login/$', LogInView.as_view(), name='login'),
    url(r'^signup/$', SignUpView.as_view(), name='signup'),
    url(r'^$', IndexView.as_view(), name='user-index'),
    url(r'^update/$', UserDetail.as_view(), name='user-update'),
    url(r'^show/ong/$', ONGListView.as_view(), name='show-ong'),
    url(r'^show/animals/$', AnimalListView.as_view(), name='show-animals'),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
                      url(r'^__debug__/', include(debug_toolbar.urls)),
                  ] + urlpatterns
