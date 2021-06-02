from django.urls import path

from . import views

app_name = 'api'
urlpatterns = [
    path('', views.index, name='index'),
    path('people/', views.people, name='people'),
    path('people/<int:person_id>/', views.person_detail, name='person detail'),
    path('pets/', views.pets, name='pets'),
    path('pets/<int:pet_id>/', views.pet_detail, name='person detail'),
]
