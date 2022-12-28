from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.middleware.csrf import CsrfViewMiddleware, get_token
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.http import Http404, HttpResponseRedirect, JsonResponse
from django.core.serializers import serialize
from jobapp.resume_nlp import cvanalysis,rankall
from account.models import User
from jobapp.forms import *
from jobapp.models import *
from jobapp.permission import *
from django.conf import settings
from django.template import RequestContext


User = get_user_model()


def home_view(request):

    published_jobs = Job.objects.filter(is_published=True).order_by('-timestamp')
    jobs = published_jobs.filter(is_closed=False)
    total_candidates = User.objects.filter(role='employee').count()
    total_companies = User.objects.filter(role='employer').count()
    paginator = Paginator(jobs, 3)
    page_number = request.GET.get('page',None)
    page_obj = paginator.get_page(page_number)

    if request.is_ajax():
        job_lists=[]
        job_objects_list = page_obj.object_list.values()
        for job_list in job_objects_list:
            job_lists.append(job_list)
        

        next_page_number = None
        if page_obj.has_next():
            next_page_number = page_obj.next_page_number()

        prev_page_number = None       
        if page_obj.has_previous():
            prev_page_number = page_obj.previous_page_number()

        data={
            'job_lists':job_lists,
            'current_page_no':page_obj.number,
            'next_page_number':next_page_number,
            'no_of_page':paginator.num_pages,
            'prev_page_number':prev_page_number
        }    
        return JsonResponse(data)
    
    context = {

    'total_candidates': total_candidates,
    'total_companies': total_companies,
    'total_jobs': len(jobs),
    'total_completed_jobs':len(published_jobs.filter(is_closed=True)),
    'page_obj': page_obj
    }
    print('ok')
    return render(request, 'jobapp/index.html', context)


def job_list_View(request):
    """

    """
    job_list = Job.objects.filter(is_published=True,is_closed=False).order_by('-timestamp')
    paginator = Paginator(job_list, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {

        'page_obj': page_obj,

    }
    return render(request, 'jobapp/job-list.html', context)


@login_required(login_url=reverse_lazy('account:login'))
@user_is_employer
def create_job_View(request):
    """
    Provide the ability to create job post
    """
    form = JobForm(request.POST or None)

    user = get_object_or_404(User, id=request.user.id)
    categories = Category.objects.all()

    if request.method == 'POST':

        if form.is_valid():

            instance = form.save(commit=False)
            instance.user = user
            instance.save()
            # for save tags
            form.save_m2m()
            messages.success(
                    request, 'You are successfully posted your job! Please wait for review.')
            dict = {

                'total_course': Course.objects.all().count(),
                'total_question':Question.objects.all().count(),
                'total_student': Student.objects.all().count()
            }
            render(request, 'teacher/teacher_dashboard.html', context=dict)
            return redirect(reverse("jobapp:single-job", kwargs={
                                   'id': instance.id
                                    }))

    context = {
        'form': form,
        'categories': categories
    }
    return render(request, 'jobapp/post-job.html', context)


def single_job_view(request, id):
    """
    Provide the ability to view job details
    """

    job = get_object_or_404(Job, id=id)
    related_job_list = job.tags.similar_objects()

    paginator = Paginator(related_job_list, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'job': job,
        'page_obj': page_obj,
        'total': len(related_job_list)

    }
    return render(request, 'jobapp/job-single.html', context)


def search_result_view(request):
    """
        User can search job with multiple fields

    """

    job_list = Job.objects.order_by('-timestamp')

    # Keywords
    if 'job_title_or_company_name' in request.GET:
        job_title_or_company_name = request.GET['job_title_or_company_name']

        if job_title_or_company_name:
            job_list = job_list.filter(title__icontains=job_title_or_company_name) | job_list.filter(
                company_name__icontains=job_title_or_company_name)

    # location
    if 'location' in request.GET:
        location = request.GET['location']
        if location:
            job_list = job_list.filter(location__icontains=location)

    # Job Type
    if 'job_type' in request.GET:
        job_type = request.GET['job_type']
        if job_type:
            job_list = job_list.filter(job_type__iexact=job_type)

    # job_title_or_company_name = request.GET.get('text')
    # location = request.GET.get('location')
    # job_type = request.GET.get('type')

    #     job_list = Job.objects.all()
    #     job_list = job_list.filter(
    #         Q(job_type__iexact=job_type) |
    #         Q(title__icontains=job_title_or_company_name) |
    #         Q(location__icontains=location)
    #     ).distinct()

    # job_list = Job.objects.filter(job_type__iexact=job_type) | Job.objects.filter(
    #     location__icontains=location) | Job.objects.filter(title__icontains=text) | Job.objects.filter(company_name__icontains=text)

    paginator = Paginator(job_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {

        'page_obj': page_obj,

    }
    return render(request, 'jobapp/result.html', context)


@login_required(login_url=reverse_lazy('account:login'))
@user_is_employee
def apply_job_view(request, id):

    form = JobApplyForm(request.POST or None)

    user = get_object_or_404(User, id=request.user.id)
    applicant = Applicant.objects.filter(user=user, job=id)

    if not applicant:
        if request.method == 'POST':

            if form.is_valid():
                instance = form.save(commit=False)
                instance.user = user
                instance.save()

                messages.success(
                    request, 'You have successfully applied for this job!')
                return redirect(reverse("jobapp:single-job", kwargs={
                    'id': id
                }))

        else:
            return redirect(reverse("jobapp:single-job", kwargs={
                'id': id
            }))

    else:

        messages.error(request, 'You already applied for the Job!')

        return redirect(reverse("jobapp:single-job", kwargs={
            'id': id
        }))


@login_required(login_url=reverse_lazy('account:login'))
def dashboard_view(request,id=id):
    """
    """
    jobs = []
    savedjobs = []
    appliedjobs = []
    total_applicants = {}
    if request.user.role == 'employer':

        jobs = Job.objects.filter(user=request.user.id)
        for job in jobs:
            count = Applicant.objects.filter(job=job.id).count()
            total_applicants[job.id] = count

    if request.user.role == 'employee':
        savedjobs = BookmarkJob.objects.filter(user=request.user.id)
        appliedjobs = Applicant.objects.filter(user=request.user.id)
    context = {

        'jobs': jobs,
        'savedjobs': savedjobs,
        'appliedjobs':appliedjobs,
        'total_applicants': total_applicants,
        'id' :id
    }

    return render(request, 'jobapp/dashboard.html', context)


@login_required(login_url=reverse_lazy('account:login'))
@user_is_employer
def delete_job_view(request, id):

    job = get_object_or_404(Job, id=id, user=request.user.id)

    if job:

        job.delete()
        messages.success(request, 'Your Job Post was successfully deleted!')

    return redirect('jobapp:dashboard')


@login_required(login_url=reverse_lazy('account:login'))
@user_is_employer
def make_complete_job_view(request, id):
    job = get_object_or_404(Job, id=id, user=request.user.id)

    if job:
        try:
            job.is_closed = True
            job.save()
            messages.success(request, 'Your Job was marked closed!')
        except:
            messages.success(request, 'Something went wrong !')
            
    return redirect('jobapp:dashboard')



@login_required(login_url=reverse_lazy('account:login'))
@user_is_employer
def all_applicants_view(request, id):
    job = get_object_or_404(Job, id=id, user=request.user.id)
    print(job.category)
    category=job.category.name
    print(type(category),category)
    all_applicants = Applicant.objects.filter(job=id)
    applicantnames=[]
    applicantresults=[]
    print(all_applicants )
    course = Course.objects.get(course_name=job.title)
    #print(applicant.user.get_full_name)
    for applicant in all_applicants:
        username=applicant.user.get_full_name()
        student = Student.objects.get(user=applicant.user)
        results = Result.objects.all().filter(exam=course).filter(student=student)
        for t in results:
            if t.exam ==course:
                applicantresults.append(t.marks)
        applicantnames.append(username)
        print(username)

    print(applicantnames)
    print(applicantresults)
    #urls=
    #for
    #    settings.MEDIA_ROOT+'/'all_applicants.user.username
    path=settings.MEDIA_ROOT
    cvsresults= rankall(path,applicantnames)
    print('cvsresults=',cvsresults)
    cvsresults1=cvsresults['Resumepath']
    cvsresults2=cvsresults[[category]]
    print(cvsresults1,cvsresults2)
    results= []
    keys=['name','score','marks']
    names=cvsresults1.values
    score=cvsresults2.values
    for i in range(len(all_applicants)):
        results.append({'name':names[i],'score':score[i][0],'marks':applicantresults[i]})
    context = {

        'all_applicants': all_applicants,
        'cvsresults1': cvsresults1.values,
        'cvsresults2':cvsresults2.values,
        'category':category,
        'applicantresults':applicantresults,
        'results': results
    }

    return render(request, 'jobapp/all-applicants.html', context)


@login_required(login_url=reverse_lazy('account:login'))
@user_is_employee
def delete_bookmark_view(request, id):

    job = get_object_or_404(BookmarkJob, id=id, user=request.user.id)

    if job:

        job.delete()
        messages.success(request, 'Saved Job was successfully deleted!')

    return redirect('jobapp:dashboard')

import os
from django.templatetags.static import static
STATIC_URL = '/static/'

@login_required(login_url=reverse_lazy('account:login'))
@user_is_employer
def applicant_details_view(request, id):

    applicant = get_object_or_404(User, id=id)
    print(applicant.get_full_name())
    filepath=settings.MEDIA_ROOT+str(applicant.get_full_name())+'.pdf'
    resultpath=settings.STATIC_IMAGE+str(applicant.get_full_name())+'.png'
    #resultpath=static('media/' + str(applicant.get_full_name()) + '.png')
    print(resultpath)
    Resumepath,CV,Categories,Score= cvanalysis(filepath, resultpath)

    context = {

        'applicant': applicant,
        'Categories' : Categories,
        'Score' : Score,
        'CV':filepath,
        'imageurl':static('images/'+str(applicant.get_full_name())+'.png')
    }

    return render(request, 'jobapp/applicant-details.html', context)


@login_required(login_url=reverse_lazy('account:login'))
@user_is_employee
def job_bookmark_view(request, id):

    form = JobBookmarkForm(request.POST or None)

    user = get_object_or_404(User, id=request.user.id)
    applicant = BookmarkJob.objects.filter(user=request.user.id, job=id)

    if not applicant:
        if request.method == 'POST':

            if form.is_valid():
                instance = form.save(commit=False)
                instance.user = user
                instance.save()

                messages.success(
                    request, 'You have successfully save this job!')
                return redirect(reverse("jobapp:single-job", kwargs={
                    'id': id
                }))

        else:
            return redirect(reverse("jobapp:single-job", kwargs={
                'id': id
            }))

    else:
        messages.error(request, 'You already saved this Job!')

        return redirect(reverse("jobapp:single-job", kwargs={
            'id': id
        }))


@login_required(login_url=reverse_lazy('account:login'))
@user_is_employer
def job_edit_view(request, id=id):
    """
    Handle Job Update

    """

    job = get_object_or_404(Job, id=id, user=request.user.id)
    categories = Category.objects.all()
    form = JobEditForm(request.POST or None, instance=job)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        # for save tags
        # form.save_m2m()
        messages.success(request, 'Your Job Post Was Successfully Updated!')
        return redirect(reverse("jobapp:single-job", kwargs={
            'id': instance.id
        }))
    context = {

        'form': form,
        'categories': categories
    }

    return render(request, 'jobapp/job-edit.html', context)


@login_required(login_url=reverse_lazy('account:login'))
@user_is_employee
def student_dashboard_view(request):
    dict = {

        'total_course': Course.objects.all().count(),
        'total_question': Question.objects.all().count(),
    }
    return render(request, 'student/student_dashboard.html', context=dict)


@login_required(login_url=reverse_lazy('account:login'))
@user_is_employee
def student_exam_view(request):
    courses = Course.objects.all()
    return render(request, 'student/student_exam.html', {'courses': courses})


@login_required(login_url=reverse_lazy('account:login'))
@user_is_employee
def take_exam_view(request, pk):
    course = Course.objects.get(id=pk)
    total_questions = Question.objects.all().filter(course=course).count()
    questions = Question.objects.all().filter(course=course)
    total_marks = 0
    for q in questions:
        total_marks = total_marks + q.marks

    return render(request, 'student/take_exam.html',
                  {'course': course, 'total_questions': total_questions, 'total_marks': total_marks})


@login_required(login_url=reverse_lazy('account:login'))
@user_is_employee
def start_exam_view(request, pk):
    course = Course.objects.get(id=pk)
    questions = Question.objects.all().filter(course=course)
    if request.method == 'POST':
        pass
    response = render(request, 'student/start_exam.html', {'course': course, 'questions': questions})
    response.set_cookie('course_id', course.id)
    return response


@login_required(login_url=reverse_lazy('account:login'))
@user_is_employee
def calculate_marks_view(request):

    if request.COOKIES.get('course_id') is not None:
        course_id = request.COOKIES.get('course_id')
        course = Course.objects.get(id=course_id)

        total_marks = 0
        questions = Question.objects.all().filter(course=course)
        for i in range(len(questions)):

            selected_ans = request.COOKIES.get(str(i + 1))
            actual_answer = questions[i].answer
            if selected_ans == actual_answer:
                total_marks = total_marks + questions[i].marks
        student = Student.objects.get(user_id=request.user.id)
        print(student)
        result = Result()
        result.marks = total_marks
        result.exam = course
        result.student = student
        result.save()

        courses = Course.objects.all()

        return render(request, 'student/view_result.html', {'courses': courses})


@login_required(login_url=reverse_lazy('account:login'))
@user_is_employee
def view_result_view(request):
    courses = Course.objects.all()
    return render(request, 'student/view_result.html', {'courses': courses})


@login_required(login_url=reverse_lazy('account:login'))
@user_is_employee
def check_marks_view(request, pk):
    course = Course.objects.get(id=pk)
    student = Student.objects.get(user_id=request.user.id)
    results = Result.objects.all().filter(exam=course).filter(student=student)
    return render(request, 'student/check_marks.html', {'results': results})


@login_required(login_url=reverse_lazy('account:login'))
@user_is_employee
def student_marks_view(request):
    courses = Course.objects.all()
    return render(request, 'student/student_marks.html', {'courses': courses})


@login_required(login_url=reverse_lazy('account:login'))
@user_is_employer
def teacher_dashboard_view(request):
    dict = {

        'total_course': Course.objects.all().count(),
        'total_question': Question.objects.all().count(),
        'total_student': Student.objects.all().count()
    }
    return render(request, 'teacher/teacher_dashboard.html', context=dict)


@login_required(login_url=reverse_lazy('account:login'))
@user_is_employer
def teacher_exam_view(request):
    return render(request, 'teacher/teacher_exam.html')


@login_required(login_url=reverse_lazy('account:login'))
@user_is_employer
def teacher_add_exam_view(request):
    courseForm = CourseForm()
    if request.method == 'POST':
        courseForm = CourseForm(request.POST)
        if courseForm.is_valid():
            courseForm.save()
        else:
            print("form is invalid")
        courses = Course.objects.all()
        return render(request, 'teacher/teacher_view_exam.html', {'courses': courses})
    return render(request, 'teacher/teacher_add_exam.html', {'courseForm': courseForm})


@login_required(login_url=reverse_lazy('account:login'))
@user_is_employer
def teacher_view_exam_view(request):
    courses = Course.objects.all()
    return render(request, 'teacher/teacher_view_exam.html', {'courses': courses})


@login_required(login_url=reverse_lazy('account:login'))
@user_is_employer
def delete_exam_view(request, pk):
    course = Course.objects.get(id=pk)
    course.delete()
    return HttpResponseRedirect('/teacher/teacher-view-exam')


@login_required(login_url=reverse_lazy('account:login'))
@user_is_employer
def teacher_question_view(request):
    return render(request, 'teacher/teacher_question.html')


@login_required(login_url=reverse_lazy('account:login'))
@user_is_employer
def teacher_add_question_view(request):
    questionForm =QuestionForm()
    if request.method == 'POST':
        questionForm =QuestionForm(request.POST)
        if questionForm.is_valid():
            question = questionForm.save(commit=False)
            course = Course.objects.get(id=request.POST.get('courseID'))
            question.course = course
            question.save()
        else:
            print("form is invalid")
        courses = Course.objects.all()
        return render(request, 'teacher/teacher_view_question.html', {'courses': courses})
    return render(request, 'teacher/teacher_add_question.html', {'questionForm': questionForm})


@login_required(login_url=reverse_lazy('account:login'))
@user_is_employer
def teacher_view_question_view(request):
    courses = Course.objects.all()
    return render(request, 'teacher/teacher_view_question.html', {'courses': courses})


@login_required(login_url=reverse_lazy('account:login'))
@user_is_employer
def see_question_view(request, pk):
    questions = Question.objects.all().filter(course_id=pk)
    return render(request, 'teacher/see_question.html', {'questions': questions})


@login_required(login_url=reverse_lazy('account:login'))
@user_is_employer
def remove_question_view(request, pk):
    question = Question.objects.get(id=pk)
    question.delete()
    courses = Course.objects.all()
    return render(request, 'teacher/teacher_view_question.html', {'courses': courses})