from django.conf.urls import include, url

from django.conf import settings

from ong.views import ONGNaturalView

urlpatterns = [
    url(r'^(?P<pk>\d+)/$', ONGNaturalView.as_view(), name='see-natural-ong'),
]
