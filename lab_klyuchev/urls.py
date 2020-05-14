"""lab_klyuchev URL Configuration

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
from django.contrib import admin
from django.urls import path, re_path
from django.conf.urls import url

from lab_app.views import insert
from lab_app.views import like
from lab_app.views import all
from lab_app.views import all_like
from lab_app.views import all_user
from lab_app.views import insert_user, insert_comment, get_comment, comment
from lab_app.views import ReportListView
from lab_app.views import UserListView
from lab_app.views import LikeListView
from lab_app.views import signIn
from lab_app.views import postsign
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from lab_klyuchev import settings

urlpatterns = [
        path('insert', insert),
    path('insert_user', insert_user),
    re_path('comment/(\d+)/(\d+)', insert_comment),
    re_path('comment/(\d+)', get_comment),
    re_path('comment', comment),
    path('all', all),
    #path('all', ReportListView.as_view()),
    #path('all_user', UserListView.as_view()),
    #path('all_like', LikeListView.as_view()),
    path('all_user', all_user),
    path('all_like', all_like),

    re_path('like/(\d+)/(\d+)', like),
    url(r'^admin/', admin.site.urls),
    re_path('^login/$', signIn),
    re_path('^postsign/', postsign)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
