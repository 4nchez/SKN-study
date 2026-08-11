from django.shortcuts import render
from .models import Board

# Create your views here.

def board_list(request):
    """게시글 목록 페이지입니다."""
    # ORM을 사용해서 전체 게시글을 조회함: all() 사용
    # 작성자 정보도 함께 조회할 것임: 역참조이용
    boards = Board.objects.select_related('author').all()

    return render(request, "boards/board_list.html", {"boards": boards})


# 새 게시글 등록 View 추가
# 등록용 from 필요함 => 추가 임포트함
# 로그인한 회원만 새 게시글 등록할 수 있음
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from .forms import BoardForm

@login_required
def board_create(request):
    """로그인 사용자만 게시글을 새로 작성할 수 있습니다."""
    form = BoardForm(request.POST or None, request.FILES or None)

    if request.method == "POST" and form.is_valid():
        # 바로 DB에 저장하지 않음
        board = form.save(commit=False)
        # 현재 로그인한 사용자를 작성자로 지정함
        board.author = request.user
        # DB에 저장
        form.save() # ORM에 의해 INSERT INTO 문 실행됨 > COMMIT 실행
        # 목록 View로 이동(View에서 View를 호출할 때: redirect 사용)
        return redirect("boards:list")

    return render(request, "boards/board_form.html", {"form": form, "mode": "등록"})


# 추가 임포트
from django.shortcuts import get_object_or_404

def board_detail(request, board_id):
    """게시글 상세 조회 View입니다."""

    # 받은 글번호로 select 조회해 옴
    board = get_object_or_404(Board, pk=board_id)
    # 조회수 1증가 처리
    board.read_count += 1
    # read_count 필드만 Update함
    board.save(update_fields=["read_count"])

    return render(request, "boards/board_detail.html", {"board": board})


# 게시글 수정 View
# 작성자 본인만 수정할 수 있음 => 예외처리
from django.core.exceptions import PermissionDenied

@login_required
def board_update(request, board_id):
    """본인 게시글만 수정하는 View입니다."""

    # 수정할 대상 게시글 조회해 옴
    board = get_object_or_404(Board, pk=board_id)

    # 현재 로그인한 사용자와 작성자 확인 (본인 글인지 확인)
    if not board.can_edit(request.user):
        # HTTP 403 Forbidden 예외 발생시킴
        raise PermissionDenied("본인이 작성한 글만 수정할 수 있습니다.")

    # form의 input과 textarea에 board의 값이 출력되게 처리함(instance 사용)
    form = BoardForm(request.POST or None, request.FILES or None, instance=board)

    if request.method == "POST" and form.is_valid():
        # 기존 게시글 update 실행 처리
        form.save() # pk인 id가 있으면 update 임, id가 없으면 insert 실행됨
        # 수정 성공하면, 상세보기 View를 작동시킴(View에서 View를 호출할 때: redirect 사용)
        return redirect("boards:detail", board_id)

    return render(request, "boards/board_form.html", {"form": form, "mode": "수정"})


# 게시물 삭제 View
@login_required
def board_delete(request, board_id):
    """ 본인 또는 관리자만 삭제하는 View입니다."""

    # 해당 글번호에 대한 게시글 조회해 옴(author가 로그인한 본인 글인지 확인)
    board = get_object_or_404(Board, pk=board_id)

    # 본인 글이 아니라면
    if not board.can_delete(request.user):
        raise PermissionDenied("삭제 권한이 없습니다.")

    # 실제 삭제는 POST 요청에서만 수행함
    if request.method == "POST":
        board.delete()
        return redirect("boards:list")

    return render(request, "boards/board_detail.html", {"board": board})