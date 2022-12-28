from django.urls import path
from jobapp import views

app_name = "jobapp"


urlpatterns = [

    path('', views.home_view, name='home'),
    path('jobs/', views.job_list_View, name='job-list'),
    path('job/create/', views.create_job_View, name='create-job'),
    path('job/<int:id>/', views.single_job_view, name='single-job'),
    path('apply-job/<int:id>/', views.apply_job_view, name='apply-job'),
    path('bookmark-job/<int:id>/', views.job_bookmark_view, name='bookmark-job'),
    path('about/', views.single_job_view, name='about'),
    path('contact/', views.single_job_view, name='contact'),
    path('result/', views.search_result_view, name='search_result'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('dashboard/employer/job/<int:id>/applicants/', views.all_applicants_view, name='applicants'),
    path('dashboard/employer/job/edit/<int:id>', views.job_edit_view, name='edit-job'),
    path('dashboard/employer/applicant/<int:id>/', views.applicant_details_view, name='applicant-details'),
    path('dashboard/employer/close/<int:id>/', views.make_complete_job_view, name='complete'),
    path('dashboard/employer/delete/<int:id>/', views.delete_job_view, name='delete'),
    path('dashboard/employee/delete-bookmark/<int:id>/', views.delete_bookmark_view, name='delete-bookmark'),
    path('student-dashboard', views.student_dashboard_view,name='student-dashboard'),
    path('student-exam', views.student_exam_view,name='student-exam'),
    path('take-exam/<int:pk>', views.take_exam_view,name='take-exam'),
    path('start-exam/<int:pk>', views.start_exam_view,name='start-exam'),
    path('calculate-marks', views.calculate_marks_view,name='calculate-marks'),
    path('view-result', views.view_result_view,name='view-result'),
    path('check-marks/<int:pk>', views.check_marks_view,name='check-marks'),
    path('applicant-marks', views.student_marks_view,name='student-marks'),
    path('teacher-dashboard', views.teacher_dashboard_view,name='teacher-dashboard'),
    path('teacher-exam', views.teacher_exam_view,name='teacher-exam'),
    path('teacher-add-exam', views.teacher_add_exam_view,name='teacher-add-exam'),
    path('teacher-view-exam', views.teacher_view_exam_view,name='teacher-view-exam'),
    path('delete-exam/<int:pk>', views.delete_exam_view,name='delete-exam'),
    path('teacher-question', views.teacher_question_view,name='teacher-question'),
    path('teacher-add-question', views.teacher_add_question_view,name='teacher-add-question'),
    path('teacher-view-question', views.teacher_view_question_view,name='teacher-view-question'),
    path('see-question/<int:pk>', views.see_question_view,name='see-question'),
    path('remove-question/<int:pk>', views.remove_question_view,name='remove-question'),

]
