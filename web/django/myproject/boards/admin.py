from django.contrib import admin
from .models import Board

# Register your models here.

@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):

    # 게시글 목록에 표시할 커럼
    list_display = (
        'id',
        'title',
        'author',
        'read_count',
        'create_at'
    )

    # 검색 가능한 필드 지정
    search_fields = (
        'title',
        'content',
    )