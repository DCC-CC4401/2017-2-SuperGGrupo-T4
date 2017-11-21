from django.conf.urls import url

from municipality.views import IndexView, UserDetail, StatisticsView, \
    ShowOngView

urlpatterns = [
    url(r'^update/$', UserDetail.as_view(), name='muni-profile-update'),
    url(r'^$', IndexView.as_view(), name='municipality-index'),
    url(r'^statistics/$', StatisticsView.as_view(),
        name='complaint-statistics'),
    url(r'^show/ong/$', ShowOngView.as_view(), name='muni-show-ong'),
]
