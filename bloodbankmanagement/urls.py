"""bloodbankmanagement URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from urllib import request
from django.contrib import admin
from django.urls import path,include
from django.contrib.auth.views import LogoutView,LoginView
from blood import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),

    
    path('donor/',include('donor.urls')),
    path('patient/',include('patient.urls')),

    
    path('',views.home_view,name='home'),
    path('patient/patient-login', views.myloginview.as_view(template_name="patient/patientlogin.html"),name='patient-login'),
    path('donor/donor-login', views.myloginview.as_view(template_name="donor/donorlogin.html"),name='donor-login'),
    path('admin/admin-login', views.myloginview.as_view(template_name="blood/adminlogin.html"),name='admin-login'),
    path('logout', LogoutView.as_view(template_name='blood/logout.html'),name='logout'),
    path('logout', LogoutView.as_view(template_name='blood/index.html'),name='error-logout'),
    path('afterlogin', views.afterlogin_view,name='afterlogin'),
    path('adminlogin', LoginView.as_view(template_name='blood/adminlogin.html'),name='adminlogin'),
    path('admin-dashboard', views.admin_dashboard_view,name='admin-dashboard'),
    path('admin-blood', views.admin_blood_view,name='admin-blood'),
    path('admin-donor', views.admin_donor_view,name='admin-donor'),
    path('admin-patient', views.admin_patient_view,name='admin-patient'),
    path('update-donor/<int:pk>', views.update_donor_view,name='update-donor'),
    path('delete-donor/<int:pk>', views.delete_donor_view,name='delete-donor'),
    path('admin-request', views.admin_request_view,name='admin-request'),
    path('update-patient/<int:pk>', views.update_patient_view,name='update-patient'),
    path('delete-patient/<int:pk>', views.delete_patient_view,name='delete-patient'),
    path('admin-donation', views.admin_donation_view,name='admin-donation'),
    path('approve-donation/<int:pk>', views.approve_donation_view,name='approve-donation'),
    path('reject-donation/<int:pk>', views.reject_donation_view,name='reject-donation'),
    path('admin-request-history', views.admin_request_history_view,name='admin-request-history'),
    path('update-approve-status/<int:pk>', views.update_approve_status_view,name='update-approve-status'),
    path('update-reject-status/<int:pk>', views.update_reject_status_view,name='update-reject-status'),
   
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
