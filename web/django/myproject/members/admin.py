# Django 관리자 기능임
from django.contrib import admin

# 기본 User 관리자 기능임
from django.contrib.auth.admin import UserAdmin

# 사용자 정의 회원 모델임
from .models import Member

# Register your models here.

@admin.register(Member)
class MemberAdmin(UserAdmin):
    """회원 관리 화면을 구성함"""

    # 회원 목록에 표시할 항목
    list_display = (
        'username',
        'display_name',
        'email',
        'is_active',
        'is_staff',
    )