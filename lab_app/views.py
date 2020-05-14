from django.http import HttpResponse

from lab_app.models import LabUser, LabReport, LabUserReport, LabComment
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin
from lab_app.forms import UploadForm
from lab_app.forms import UserUploadForm, CommentForm
from .tables import LabReportTable, UserReportTable, LikeReportTable, CommentTable
from django.views.generic import ListView
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
from django_tables2 import SingleTableView
from django.core import serializers
import datetime
import json

import pyrebase
from django.shortcuts import render

# config = {
#     'apiKey': "AIzaSyD756fzVNb6lpn3wumsTmtKQOllpM3AjYY",
#     'authDomain': "klyuchev-ee7ab.firebaseapp.com",
#     'databaseURL': "https://klyuchev-ee7ab.firebaseio.com",
#     'projectId': "klyuchev-ee7ab",
#     'storageBucket': "klyuchev-ee7ab.appspot.com",
#     'messagingSenderId': "5241417359719",
#     'appId': "1:241417359719:web:82be17c0bed3733318dfc2",
#     'measurementId': "G-4GL1JG8373"
# }

config = {
    'apiKey': "AIzaSyD7x4Fc9GinoE9wOb9ZoomQ1JwiIUpJFps",
    'authDomain': "smart-transport-a991e.firebaseapp.com",
    'databaseURL': "https://smart-transport-a991e.firebaseio.com",
    'projectId': "smart-transport-a991e",
    'storageBucket': "smart-transport-a991e.appspot.com",
    'messagingSenderId': "739232366451",
    'appId': "1:739232366451:web:37791d77b99c115fc98f06",
    'measurementId': "G-S189ZMGJDR"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()


def signIn(request):
    return render(request, "SignIn.html")


def postsign(request):
    email = request.POST.get('email')
    password = request.POST.get("pass")
    try:
        user = auth.sign_in_with_email_and_password(email, password)
        role = LabUser.objects.get(email=user['email']).role
        print(role)
        request.session['email'] = user['email']
        request.session['role'] = role
    except:
        message = "Неправильные логин или пароль"
        return render(request, "SignIn.html", {"msg": message})
    return redirect('/all')
    return render(request, "Welcome.html", {"e": email})




@csrf_exempt
def insert(request):
    if request.method != "POST":
        return HttpResponse("{status: not_post}")
    form = UploadForm(request.POST, request.FILES)

    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = LabUser.objects.get(pk=request.POST['user_id'])
        instance.save()
    else:
        return HttpResponse("{form: " + str(form) + "}")
    return HttpResponse("{status: success}")


@csrf_exempt
def insert_user(request):
    if request.method != "POST":
        return HttpResponse("{status: not_post}")
    form = UserUploadForm(request.POST)
    if form.is_valid():
        form.save()
    else:
        return HttpResponse("{form: " + str(form) + "}")
    return HttpResponse("{status: success}")


@csrf_exempt
def insert_comment(request, user, report):
    try:
        lu = LabComment()
        lu.user = LabUser.objects.get(id=user)
        lu.report = LabReport.objects.get(id=report)
        lu.text = request.GET['text']
        lu.time = datetime.datetime.now()
        lu.save()
        return HttpResponse('{"status:" "success"}')
    except Exception as e:
        return HttpResponse('{"status:" "wrong ids"}')


def get_comment(request, report):
    try:
        objects = LabComment.objects.filter(report=report)
        data = serializers.serialize("json", objects)
        print(data)
        print(type(data))
        return HttpResponse(data)
    except Exception as e:
        return HttpResponse('{"status:" "wrong id"}')


class ReportListView(SingleTableView):
    model = LabReport
    table_class = LabReportTable
    template_name = 'LabReport.html'


class UserListView(SingleTableView):
    model = LabUser
    table_class = UserReportTable
    template_name = 'LabReport.html'


class LikeListView(SingleTableView):
    model = LabUserReport
    table_class = LikeReportTable
    template_name = 'LabReport.html'



class CommentListView(SingleTableView):
    model = LabComment
    table_class = CommentTable
    template_name = 'LabReport.html'

@csrf_exempt
def all(request):
    status_d = {
        1: 'Поступила',
        2: 'Передана в работу',
        3: 'Отклонена'
    }
    print('email' not in request.session.keys())
    print('token' not in request.GET.keys())
    if not('email' in request.session.keys() or 'token' in request.GET.keys() and\
        request.GET['token'] == '123'):
        return redirect('/login/')
    if 'PreviousReceiver' in request.GET and\
            'role' in request.session.keys() and \
            request.session['role'] != 'user':
        button = int(request.GET['PreviousReceiver'][-1])
        _id = int(request.GET['PreviousReceiver'][:-2])
        print(button, _id)
        record = LabReport.objects.get(pk=_id)
        record.status = status_d[button]
        record.save()
        print(record.status)
    return ReportListView.as_view()(request)


def all_like(request):
    if not('email' in request.session.keys() or 'token' in request.GET.keys() and\
        request.GET['token'] == '123'):
        return redirect('/login/')
    return LikeListView.as_view()(request)


def comment(request):
    return CommentListView.as_view()(request)


def all_user(request):
    if not('email' in request.session.keys() or 'token' in request.GET.keys() and\
        request.GET['token'] == '123'):
        return redirect('/login/')
    status_d = {
        1: 'user',
        2: 'moderator',
        3: 'admin'
    }
    if 'PreviousReceiver' in request.GET and\
            'role' in request.session.keys() and \
            request.session['role'] == 'admin':
        button = int(request.GET['PreviousReceiver'][-1])
        _id = int(request.GET['PreviousReceiver'][:-2])
        print(button, _id)
        record = LabUser.objects.get(pk=_id)
        record.role = status_d[button]
        record.save()
        print(record.role)
    return UserListView.as_view()(request)


def like(request, report, user):
    try:
        q = LabUserReport.objects.filter(user=user, report=report)
        print(type(q))
        if len(q) > 0:
            return HttpResponse('{"status:" "already liked"}')

        lu = LabUserReport()
        lu.user = LabUser.objects.get(id=user)
        lu.report = LabReport.objects.get(id=report)
        lu.save()
        r = LabReport.objects.get(id=report)
        r.likes += 1
        r.save()
        return HttpResponse('{"status:" "success"}')
    except Exception as e:
        return HttpResponse('{"status:" "wrong ids"}')