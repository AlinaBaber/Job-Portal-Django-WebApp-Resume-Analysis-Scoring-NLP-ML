# Generated by Django 3.0 on 2022-07-20 00:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('jobapp', '0020_auto_20220720_0332'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_name', models.CharField(max_length=50)),
                ('question_number', models.PositiveIntegerField()),
                ('total_marks', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('marks', models.PositiveIntegerField()),
                ('question', models.CharField(max_length=600)),
                ('option1', models.CharField(max_length=200)),
                ('option2', models.CharField(max_length=200)),
                ('option3', models.CharField(max_length=200)),
                ('option4', models.CharField(max_length=200)),
                ('answer', models.CharField(choices=[('Option1', 'Option1'), ('Option2', 'Option2'), ('Option3', 'Option3'), ('Option4', 'Option4')], max_length=200)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jobapp.Course')),
            ],
        ),
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('marks', models.PositiveIntegerField()),
                ('date', models.DateTimeField(auto_now=True)),
                ('exam', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jobapp.Course')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_pic', models.ImageField(blank=True, null=True, upload_to='profile_pic/Student/')),
                ('address', models.CharField(max_length=40)),
                ('mobile', models.CharField(max_length=20)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_pic', models.ImageField(blank=True, null=True, upload_to='profile_pic/Teacher/')),
                ('address', models.CharField(max_length=40)),
                ('mobile', models.CharField(max_length=20)),
                ('status', models.BooleanField(default=False)),
                ('salary', models.PositiveIntegerField(null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='employeeexam_db',
            name='applicant',
        ),
        migrations.RemoveField(
            model_name='employeeexam_db',
            name='qpaper',
        ),
        migrations.RemoveField(
            model_name='employeeexam_db',
            name='questions',
        ),
        migrations.RemoveField(
            model_name='employeeresults_db',
            name='applicant',
        ),
        migrations.RemoveField(
            model_name='employeeresults_db',
            name='exams',
        ),
        migrations.RemoveField(
            model_name='exam_model',
            name='employer',
        ),
        migrations.RemoveField(
            model_name='exam_model',
            name='job',
        ),
        migrations.RemoveField(
            model_name='exam_model',
            name='question_paper',
        ),
        migrations.RemoveField(
            model_name='question_db',
            name='employer',
        ),
        migrations.RemoveField(
            model_name='question_paper',
            name='employer',
        ),
        migrations.RemoveField(
            model_name='question_paper',
            name='questions',
        ),
        migrations.DeleteModel(
            name='Employee_Question',
        ),
        migrations.DeleteModel(
            name='EmployeeExam_DB',
        ),
        migrations.DeleteModel(
            name='EmployeeResults_DB',
        ),
        migrations.DeleteModel(
            name='Exam_Model',
        ),
        migrations.DeleteModel(
            name='Question_DB',
        ),
        migrations.DeleteModel(
            name='Question_Paper',
        ),
    ]
