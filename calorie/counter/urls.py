from django.urls import path
from counter import views

urlpatterns = [
    path('', views.index, name="index"),
    path('login/', views.login, name="login")

]
