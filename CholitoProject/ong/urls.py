from django.conf.urls import url

from ong.views import ONGNaturalView, ONGIndexView

urlpatterns = [
    url(r'^(?P<pk>\d+)/$', ONGNaturalView.as_view(), name='see-natural-ong'),
    url(r'^$', ONGIndexView.as_view(), name='ong-index'),
]
