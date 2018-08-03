from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('summery/', views.summery, name='summery'),
    path('<emailId>/emaildetails', views.emailcontent, name='emailcontent'),
    path('<staff_from>/<staff_to>/detail', views.mail_history, name='staffdetail'),
    path('staff-alias/', views.staff_alias_a, name='staff-alias-a'),
    path('<staff_name>/staff', views.staffsummery, name='staffsummery'),
    path('dirlist', views.dirlist, name='dirlist'),
    path('dirlist/<dirname>', views.sta_same_timestamp, name='sta_same_timestamp'),

]