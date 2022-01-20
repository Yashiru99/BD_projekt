from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('warsaw', views.warsaw, name='warsaw'),
    path('cracow', views.cracow, name='cracow'),
    path('poznan', views.poznan, name='poznan'),
    path('results', views.result, name='results'),
    path('annoucement', views.add_an_annoucement, name='annoucement'),
    path('success', views.success, name='success'),
    path('comparing', views.comparing, name='comparing')
]

urlpatterns += staticfiles_urlpatterns()