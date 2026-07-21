# -*- coding: utf-8 -*-
"""LLM 호출 없이 확인 가능한 FastAPI 기본 엔드포인트 테스트입니다."""

# FastAPI 테스트 클라이언트를 가져옵니다.
from fastapi.testclient import TestClient
# 실제 애플리케이션 객체를 가져옵니다.
from app.main import app

# 테스트 요청에 사용할 클라이언트를 생성합니다.
client = TestClient(app)


def test_health() -> None:
    """헬스 체크가 정상 상태와 전체 아키텍처를 반환하는지 확인합니다."""
    # 헬스 체크 API를 호출합니다.
    response = client.get("/api/v1/health")
    # HTTP 상태 코드가 200인지 확인합니다.
    assert response.status_code == 200
    # 응답 JSON에 LangGraph가 포함되는지 확인합니다.
    assert "LangGraph" in response.json()["architecture"]


def test_mcp_monthly_sales_tool() -> None:
    """HTTP MCP 호환 월별 매출 도구가 API 키 없이 동작하는지 확인합니다."""
    # 특정 월 매출 도구를 호출합니다.
    response = client.post("/api/v1/tools/call", json={"tool_name": "monthly_sales", "month": "2026-05", "filename": "monthly_sales.csv", "limit": 10})
    # HTTP 상태 코드가 200인지 확인합니다.
    assert response.status_code == 200
    # 결과 문자열에 대상 월이 포함되는지 확인합니다.
    assert "2026-05" in response.json()["result"]
