from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('summery/', views.email_matrix, name='email_matrix'),
    path('<emailId>/emaildetails', views.emailcontent, name='emailcontent'),
    path('<staff_from>/<staff_to>/detail', views.email_timeline, name='timeline'),
    path('staff-alias/', views.staff_alias_a, name='staff-alias-a'),
    path('<staff_name>/staff', views.staffsummery, name='staffsummery'),
    path('dirlist', views.dirlist, name='dirlist'),
    path('dirlist/<dirname>', views.sta_same_timestamp, name='sta_same_timestamp'),
    path('staff-alias/log', views.alais_process_log, name='alais-log'),
    path('emailexplore/', views.email_explore, name='email_explore'),
    path('emailexploretest/', views.email_explore, name='email_explore'),
    path('content/<id>', views.processContent, name='email_con'),

]
