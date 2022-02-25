from django.shortcuts import render,redirect,reverse
from . import forms,models
from django.db.models import Sum,Q
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.conf import settings
from datetime import date, timedelta
from django.core.mail import send_mail
from django.contrib.auth.models import User
from blood import forms as bforms
from blood import models as bmodels
from django.contrib.auth.views import LoginView

class myloginview(LoginView):
    from django.utils.decorators import method_decorator
    from django.views.decorators.cache import never_cache
    from django.views.decorators.csrf import csrf_protect
    from django.views.decorators.debug import sensitive_post_parameters
    template_name="patient/patientlogin.html"
    @method_decorator(sensitive_post_parameters())
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        print('###########')
        print(f'{request.method}')
        if self.redirect_authenticated_user and self.request.user.is_authenticated:
            redirect_to = self.get_success_url()
            if redirect_to == self.request.path:
                raise ValueError(
                    "Redirection loop for authenticated user detected. Check that "
                    "your LOGIN_REDIRECT_URL doesn't point to a login page."
                )
            return HttpResponseRedirect(redirect_to)
        return super().dispatch(request, *args, **kwargs)


def patient_signup_view(request):
    userForm=forms.PatientUserForm()
    patientForm=forms.PatientForm()
    mydict={'userForm':userForm,'patientForm':patientForm}
    if request.method=='POST':
        userForm=forms.PatientUserForm(request.POST)
        patientForm=forms.PatientForm(request.POST,request.FILES)
        if userForm.is_valid() and patientForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            patient=patientForm.save(commit=False)
            patient.user=user
            patient.bloodgroup=patientForm.cleaned_data['bloodgroup']
            patient.save()
            my_patient_group = Group.objects.get_or_create(name='PATIENT')
            my_patient_group[0].user_set.add(user)
        return HttpResponseRedirect('patient-login')
    return render(request,'patient/patientsignup.html',context=mydict)

def patient_dashboard_view(request):
    patient= models.Patient.objects.get(user_id=request.user.id)
    dict={
        'requestpending': bmodels.BloodRequest.objects.all().filter(request_by_patient=patient).filter(status='Pending').count(),
        'requestapproved': bmodels.BloodRequest.objects.all().filter(request_by_patient=patient).filter(status='Approved').count(),
        'requestmade': bmodels.BloodRequest.objects.all().filter(request_by_patient=patient).count(),
        'requestrejected': bmodels.BloodRequest.objects.all().filter(request_by_patient=patient).filter(status='Rejected').count(),

    }
   
    return render(request,'patient/patient_dashboard.html',context=dict)

def make_request_view(request):
    request_form=bforms.RequestForm()
    if request.method=='POST':
        request_form=bforms.RequestForm(request.POST)
        if request_form.is_valid():
            blood_request=request_form.save(commit=False)
            blood_request.bloodgroup=request_form.cleaned_data['bloodgroup']
            patient= models.Patient.objects.get(user_id=request.user.id)
            blood_request.request_by_patient=patient
            blood_request.save()
            return HttpResponseRedirect('my-request')  
    return render(request,'patient/makerequest.html',{'request_form':request_form})

def my_request_view(request):
    patient= models.Patient.objects.get(user_id=request.user.id)
    blood_request=bmodels.BloodRequest.objects.all().filter(request_by_patient=patient)
    return render(request,'patient/my_request.html',{'blood_request':blood_request})
