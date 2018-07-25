from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('summery/', views.comm_brief, name='comm_brief'),
    path('<staff_from>/<staff_to>/detail', views.mail_history, name='staffdetail'),
]