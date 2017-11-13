from django.conf import settings
from django.conf.urls import include, url

from .views import *

urlpatterns = [
    url(r'^login/$', LogInView.as_view(), name='login'),
    url(r'^signup/$', SignUpView.as_view(), name='signup'),
    url(r'^$', IndexView.as_view(), name='user-index'),

    url(r'^favourite/$', ONGFavView.as_view(), name='fav-ong'),

    # for now
    url(r'^user/$', UserDetail.as_view(), name='user-update'),
    url(r'^user-ong-in/$', OngInViewTemplate.as_view(), name='user-ong-in'),
    url(r'^user-ong-out/$', OngOutViewTemplate.as_view(), name='user-ong-out'),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
                      url(r'^__debug__/', include(debug_toolbar.urls)),
                  ] + urlpatterns
