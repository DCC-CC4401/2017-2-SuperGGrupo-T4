from django.conf.urls import url

from ong.views import ONGDispatcherView, ONGIndexView, ONGAdoptedView, \
    ONGStatisticsView, ONGEditView, ONGAddAnimalView, ONGRequestsView, \
    ONGFavView, ONGEditAnimalView, ONGCreateAnimalView, \
    ONGEUpdateAnimalView, ONGAnimalView

urlpatterns = [
    url(r'^(?P<pk>\d+)/$', ONGDispatcherView.as_view(), name='see-natural-ong'),
    url(r'^$', ONGIndexView.as_view(), name='ong-index'),
    url(r'^adopted/$', ONGAdoptedView.as_view(), name='ong-adopted'),
    url(r'^statistics/$', ONGStatisticsView.as_view(), name='ong-statistics'),
    url(r'^edit/$', ONGEditView.as_view(), name='ong-edit'),
    url(r'^add/$', ONGAddAnimalView.as_view(), name='add-animal'),
    url(r'^add/animal/$', ONGCreateAnimalView.as_view(),
        name='create-animal'),
    url(r'^requests/(?P<pk>\d+)/$', ONGRequestsView.as_view(),
        name='see-requests'),
    url(r'^favourite/$', ONGFavView.as_view(), name='fav-ong'),
    url(r'^edit/animal/(?P<pk>\d+)$', ONGEditAnimalView.as_view(),
        name='edit-animal'),
    url(r'^update/animal/(?P<pk>\d+)$', ONGEUpdateAnimalView.as_view(),
        name='update-animal'),
    url(r'^animal/(?P<pk>\d+)$', ONGAnimalView.as_view(),
        name='see-animal-ong'),
]
