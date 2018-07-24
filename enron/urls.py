from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<staff_name>/', views.staff_detail, name='staffdetail'),
]