from urllib import request
from django.urls import path
from django.contrib.auth.views import LoginView
from . import views
urlpatterns = [
    # path('add', views.myloginview.as_view(),name='patient-login'),
    path('patientsignup', views.patient_signup_view,name='patientsignup'),
    path('patient-dashboard', views.patient_dashboard_view,name='patient-dashboard'),
    path('make-request', views.make_request_view,name='make-request'),
    path('my-request', views.my_request_view,name='my-request'),
]