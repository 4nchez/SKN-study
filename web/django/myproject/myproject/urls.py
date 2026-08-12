"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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

# include 는 App별 urls.py를 연결할 때 사용함
from django.urls import path, include

from members.views import home

# settings 값을 읽음
from django.conf import settings

# 개발 서버에서 media 파일을 제공하기 위함
from django.conf.urls.static import static


urlpatterns = [
    # Django 관리자 페이지
    path('admin/', admin.site.urls),

    # 사이트 첫 화면
    # 로그인 성공시 출력되는 페이지
    path('', home, name='home'),

    # 회원 App url 추가
    path(
        'members/',
        include('members.urls', namespace="members")
    ),

    # boards 앱에 대한 urls 추가
    path(
        'boards/',
        include('boards.urls', namespace="boards")
    ),
]

# 개발 환경에서 사용자가 업로드한 파일을 Django 개발 서버가 제공하도록 설정함
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)