# boards 앱에 작성된 View 들의 url만 등록 처리함

from django.urls import path
from . import views


app_name = "boards"

urlpatterns = [
    # 게시판 목록: http://web_ip주소:port번호/boards/
    path('', views.board_list, name='list'),

    # 게시글 등록: http://web_ip주소:port번호/boards/create
    path('create', views.board_create, name='create'),

    # 게시글 상세: http://web_ip주소:port번호/boards/{board_id}
    path('<int:board_id>', views.board_detail, name='detail'),

    # 게시글 수정: http://web_ip주소:port번호/boards/update/{board_id}
    path('edit/<int:board_id>', views.board_update, name='update'),

    # 게시글 삭제: http://web_ip주소:port번호/boards/delete/{board_id}
    path('delete/<int:board_id>', views.board_delete, name='delete'),
]