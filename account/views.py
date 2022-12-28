from django.contrib import auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect , get_object_or_404
from django.urls import reverse, reverse_lazy
from django.core.files.storage import FileSystemStorage
from account.forms import *
from jobapp.permission import user_is_employee
from jobapp import forms as jforms
import pandas as pd

def get_success_url(request):

    """
    Handle Success Url After LogIN

    """
    if 'next' in request.GET and request.GET['next'] != '':
        return request.GET['next']
    else:
        return reverse('jobapp:home')


def employee_registration(request):

    """
    Handle Employee Registration

    """
    form = EmployeeRegistrationForm(request.POST or None)
    student_form = jforms.StudentForm()
    if form.is_valid():
        form = form.save()
        student = student_form.save(commit=False)
        student.user = form
        student.mobile = None
        student.address = None
        student.profile_pic = None
        student.save()
        return redirect('account:login')
    context = {

        'form': form,
        'studentform': student_form
    }

    return render(request,'account/employee-registration.html',context)


def employer_registration(request):

    """
    Handle Employee Registration 

    """

    form = EmployerRegistrationForm(request.POST or None)
    teacher_form = jforms.TeacherForm(request.POST, request.FILES)
    if form.is_valid():
        form = form.save()
        teacher = teacher_form.save(commit=False)
        teacher.user = form
        teacher.mobile = None
        teacher.address = None
        teacher.profile_pic = None
        teacher.salary = None
        teacher.save()
        return redirect('account:login')
    context={
        
            'form': form,
            'teacherform': teacher_form
        }

    return render(request,'account/employer-registration.html',context)


@login_required(login_url=reverse_lazy('accounts:login'))
@user_is_employee
def employee_edit_profile(request, id=id):

    """
    Handle Employee Profile Update Functionality

    """

    user = get_object_or_404(User, id=id)
    #upload_cv(request, str(id))
    form = EmployeeProfileEditForm(request.POST or None, instance=user)
    #print(fields)
    #print(fields['last_name'])
    #fieldname1=form.data('first_name')
    #fieldname2=form.data('last_name')
    fieldsfname = form.data.get('first_name')
    fieldslname = form.data.get('last_name')
    print(str(fieldsfname)+'_'+str(fieldslname))
    if form.is_valid():
        form = form.save()
        if 'document' in request.FILES:
            uploaded_file = request.FILES['document']
            fs = FileSystemStorage()
            filename=str(fieldsfname)+' '+str(fieldslname)+'.pdf'
            name = fs.save(filename, uploaded_file)
            url = fs.url(name)
        messages.success(request, 'Your Profile Was Successfully Updated!')

        return redirect(reverse("account:edit-profile", kwargs={
                                    'id': form.id
                                    }))
    context={
        
            'form':form
        }

    return render(request,'account/employee-edit-profile.html',context)



def user_logIn(request):

    """
    Provides users to logIn

    """

    form = UserLoginForm(request.POST or None)
    

    if request.user.is_authenticated:
        return redirect('/')
    
    else:
        if request.method == 'POST':
            if form.is_valid():
                auth.login(request, form.get_user())
                return HttpResponseRedirect(get_success_url(request))
    context = {
        'form': form,
    }

    return render(request,'account/login.html',context)


def user_logOut(request):
    """
    Provide the ability to logout
    """
    auth.logout(request)
    messages.success(request, 'You are Successfully logged out')
    return redirect('account:login')