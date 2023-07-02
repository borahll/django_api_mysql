from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token
urlpatterns = [
    path('', views.apiOverView, name = 'apioverview'),
    path('add/', views.addUser),
    path('deleteUser/', views.delete),
    path('updateAll/', views.patch),
    path('update/', views.put),
    path('login/', obtain_auth_token, name="login")
]