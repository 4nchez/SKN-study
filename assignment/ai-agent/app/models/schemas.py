# -*- coding: utf-8 -*-
"""FastAPI 요청과 응답 데이터의 Pydantic 스키마입니다."""

# 요청 필드 검증을 위해 BaseModel과 Field를 가져옵니다.
from pydantic import BaseModel, Field
# 허용된 공급자 문자열을 제한하기 위해 Literal을 가져옵니다.
from typing import Literal


class ChatRequest(BaseModel):
    """통합 비즈니스 에이전트 채팅 요청입니다."""
    message: str = Field(min_length=1, description="분석하거나 실행할 사용자 질문")
    provider: Literal["openai", "gemini"] = Field(default="openai", description="사용할 LLM 공급자")
    thread_id: str = Field(default="business-session", min_length=1, description="멀티턴 대화 구분 값")


class ToolCallRequest(BaseModel):
    """MCP 호환 도구 직접 호출 요청입니다."""
    tool_name: Literal["monthly_sales", "csv_preview", "data_summary", "data_files"]
    month: str = ""
    filename: str = "monthly_sales.csv"
    limit: int = Field(default=10, ge=1, le=100)


class A2AMessageRequest(BaseModel):
    """A2A 전문 에이전트 직접 위임 요청입니다."""
    agent_name: str = Field(min_length=1)
    message: str = Field(min_length=1)
    provider: Literal["openai", "gemini"] = "openai"
