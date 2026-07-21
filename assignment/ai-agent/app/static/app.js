// 통합 에이전트 실행 버튼 요소를 가져옵니다.
const button = document.getElementById("sendButton");
// 사용자 질문 입력 요소를 가져옵니다.
const message = document.getElementById("message");
// 최종 답변을 표시할 요소를 가져옵니다.
const answer = document.getElementById("answer");
// 선택된 실행 경로를 표시할 요소를 가져옵니다.
const route = document.getElementById("route");
// LangGraph 실행 추적을 표시할 요소를 가져옵니다.
const trace = document.getElementById("trace");

// 사용자가 실행 버튼을 눌렀을 때 비동기 요청을 수행합니다.
button.addEventListener("click", async () => {
    // 입력 질문의 앞뒤 공백을 제거합니다.
    const text = message.value.trim();
    // 질문이 비어 있으면 API를 호출하지 않고 안내합니다.
    if (!text) {
        answer.textContent = "질문을 입력하세요.";
        return;
    }
    // 중복 요청을 막기 위해 버튼을 비활성화합니다.
    button.disabled = true;
    // 실행 상태를 답변 영역에 표시합니다.
    answer.textContent = "실행 중...";
    // 이전 실행 경로를 초기화합니다.
    route.textContent = "-";
    // 이전 실행 추적을 초기화합니다.
    trace.textContent = "-";
    try {
        // FastAPI 통합 채팅 엔드포인트에 JSON POST 요청을 전송합니다.
        const response = await fetch("/api/v1/chat", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({
                message: text,
                provider: document.getElementById("provider").value,
                thread_id: document.getElementById("threadId").value.trim() || "business-session"
            })
        });
        // 응답 본문을 JSON 객체로 변환합니다.
        const data = await response.json();
        // HTTP 오류이면 FastAPI의 detail 메시지를 예외로 변환합니다.
        if (!response.ok) {
            throw new Error(data.detail || "요청 실패");
        }
        // 최종 답변을 화면에 표시합니다.
        answer.textContent = data.answer || "답변 없음";
        // LangGraph 분류 경로와 A2A 대상을 표시합니다.
        route.textContent = `${data.route || "-"} → ${data.target_agent || "-"}`;
        // 단계별 실행 추적을 줄바꿈 문자열로 변환해 표시합니다.
        trace.textContent = (data.trace || []).map((item) => `[${item.stage}] ${item.detail}`).join("\n") || "-";
    } catch (error) {
        // 네트워크 또는 서버 오류 메시지를 답변 영역에 표시합니다.
        answer.textContent = `오류: ${error.message}`;
    } finally {
        // 성공 또는 실패와 관계없이 다시 요청할 수 있도록 버튼을 활성화합니다.
        button.disabled = false;
    }
});

const promptType = document.getElementById("promptType");
// const promptPresets = JSON.parse(`{{ prompt_data | safe }}`);
// 템플릿 변수를 그대로 출력하면 자바스크립트 객체로 바로 할당됩니다.
const promptPresets = window.promptPresets;
promptType.addEventListener(
    "change",
    applySelectedPreset
);

function applySelectedPreset() {
    const preset = promptPresets.find(
        (item) => item.value === promptType.value
    );

    if (!preset) {
        message.value = "";
        return;
    }

    message.value = preset.prompt;
}