from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('summery/', views.comm_brief, name='comm_brief'),
    path('<staff_name>/', views.staff_detail, name='staffdetail'),
]