// app/static/app.js
// ------------------------------------------------------------
// 챗봇 화면의 동작을 담당하는 JavaScript 파일입니다.
// 사용자의 입력을 FastAPI /api/chat 엔드포인트로 전송하고 응답을 화면에 출력합니다.
// ------------------------------------------------------------

// 챗봇 열기 버튼 요소를 가져옵니다.
const chatIcon = document.getElementById("chatIcon");

// 챗봇 모달 요소를 가져옵니다.
const chatModal = document.getElementById("chatModal");

// 챗봇 닫기 버튼 요소를 가져옵니다.
const closeChat = document.getElementById("closeChat");

// 메시지 목록이 표시될 영역을 가져옵니다.
const chatMessages = document.getElementById("chatMessages");

// 메시지 입력 폼 요소를 가져옵니다.
const chatForm = document.getElementById("chatForm");

// 사용자가 질문을 입력하는 input 요소를 가져옵니다.
const messageInput = document.getElementById("messageInput");

// 이전 대화 내역을 저장하는 배열입니다.
// 서버에 함께 전달하면 문맥을 이어서 답변할 수 있습니다.
const history = [];

// 챗봇 버튼을 클릭하면 모달의 hidden 클래스를 제거하여 화면에 표시합니다.
chatIcon.addEventListener("click", () => {
    chatModal.classList.remove("hidden");
    // 챗봇을 다시 열 때는 혹시 열려 있던 설정 패널을 닫아둔 상태로 초기화합니다.
    settingsPanel.classList.add("hidden");
    messageInput.focus();
});

// 닫기 버튼을 클릭하면 모달에 hidden 클래스를 추가하여 화면에서 숨깁니다.
closeChat.addEventListener("click", () => {
    chatModal.classList.add("hidden");
});

// 채팅 설정 영역
// 설정 버튼 요소를 가져옵니다.
const settingsBtn = document.getElementById("settingsBtn");

// 설정 패널 요소를 가져옵니다.
const settingsPanel = document.getElementById("settingsPanel");

// 설정 닫기 버튼 요소를 가져옵니다.
const closeSettings = document.getElementById("closeSettings");

// 설정 각 입력 요소들을 가져옵니다.
const settingSystemInstruction = document.getElementById("settingSystemInstruction");
const settingModel = document.getElementById("settingModel");
const settingTemperature = document.getElementById("settingTemperature");
const settingTemperatureValue = document.getElementById("settingTemperatureValue");
const settingTopP = document.getElementById("settingTopP");
const settingTopPValue = document.getElementById("settingTopPValue");
const settingMaxTokens = document.getElementById("settingMaxTokens");
const resetSettingsBtn = document.getElementById("resetSettings");
const saveSettingsBtn = document.getElementById("saveSettings");

// 서버로 전송할 설정값의 기본값입니다. (Pydantic 모델 기본값과 동일하게 맞춥니다.)
const DEFAULT_SETTINGS = {
    system_instruction: "친절하고 정확한 AI 강사처럼 답변하시오.",
    model: null,
    temperature: 0.7,
    top_p: 0.95,
    max_output_tokens: 800,
};

// 현재 적용 중인 설정값을 담는 객체입니다. 기본값으로 초기화합니다.
let chatSettings = { ...DEFAULT_SETTINGS };

// 설정값 객체를 화면 입력 요소에 반영하는 함수입니다.
function renderSettingsToForm(settings) {
    settingSystemInstruction.value = settings.system_instruction;
    settingModel.value = settings.model ?? "";
    settingTemperature.value = settings.temperature;
    settingTemperatureValue.textContent = settings.temperature.toFixed(2);
    settingTopP.value = settings.top_p;
    settingTopPValue.textContent = settings.top_p.toFixed(2);
    settingMaxTokens.value = settings.max_output_tokens;
}

// 화면 입력 요소의 값을 읽어 설정값 객체로 만드는 함수입니다.
function readSettingsFromForm() {
    // 모델명은 빈 문자열이면 null로 처리하여 서버 기본 모델이 사용되도록 합니다.
    const modelValue = settingModel.value.trim();

    return {
        system_instruction: settingSystemInstruction.value.trim() || DEFAULT_SETTINGS.system_instruction,
        model: modelValue === "" ? null : modelValue,
        temperature: Number(settingTemperature.value),
        top_p: Number(settingTopP.value),
        max_output_tokens: Number(settingMaxTokens.value),
    };
}

// 페이지 로드 시 기본값을 폼에 반영합니다.
renderSettingsToForm(chatSettings);

// 설정 버튼을 클릭하면 설정 패널을 표시합니다.
settingsBtn.addEventListener("click", () => {
    // 패널을 열 때는 현재 적용된 설정값 기준으로 폼을 다시 그립니다.
    renderSettingsToForm(chatSettings);
    settingsPanel.classList.remove("hidden");
});

// 설정 닫기 버튼을 클릭하면 저장 없이 패널만 닫습니다.
closeSettings.addEventListener("click", () => {
    settingsPanel.classList.add("hidden");
});

// 슬라이더를 움직일 때마다 옆의 숫자 표시를 갱신합니다.
settingTemperature.addEventListener("input", () => {
    settingTemperatureValue.textContent = Number(settingTemperature.value).toFixed(2);
});

settingTopP.addEventListener("input", () => {
    settingTopPValue.textContent = Number(settingTopP.value).toFixed(2);
});

// 기본값으로 초기화 버튼을 클릭하면 폼과 실제 설정값을 모두 기본값으로 되돌립니다.
resetSettingsBtn.addEventListener("click", () => {
    chatSettings = { ...DEFAULT_SETTINGS };
    renderSettingsToForm(chatSettings);
});

// 저장 버튼을 클릭하면 폼의 값을 읽어 실제 설정값에 반영하고 패널을 닫습니다.
saveSettingsBtn.addEventListener("click", () => {
    chatSettings = readSettingsFromForm();
    settingsPanel.classList.add("hidden");
});


// 화면에 메시지 말풍선을 추가하는 함수입니다.
function addMessage(role, content) {
    // div 요소를 새로 생성합니다.
    const messageElement = document.createElement("div");

    // role에 따라 user 또는 assistant 스타일이 적용되도록 클래스를 지정합니다.
    messageElement.className = `message ${role}`;

    // textContent를 사용하여 사용자가 입력한 HTML이 실행되지 않도록 안전하게 출력합니다.
    messageElement.textContent = content;

    // 생성한 메시지 요소를 메시지 목록 영역에 추가합니다.
    chatMessages.appendChild(messageElement);

    // 새 메시지가 추가되면 스크롤을 가장 아래로 이동합니다.
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// 메시지 전송 폼이 제출될 때 실행되는 이벤트입니다.
chatForm.addEventListener("submit", async (event) => {
    // form의 기본 동작인 페이지 새로고침을 막습니다.
    event.preventDefault();

    // 입력값 앞뒤 공백을 제거합니다.
    const message = messageInput.value.trim();

    // 빈 문자열이면 서버로 전송하지 않습니다.
    if (!message) {
        return;
    }

    // 사용자 메시지를 화면에 먼저 출력합니다.
    addMessage("user", message);

    // 대화 기록에도 사용자 메시지를 저장합니다.
    history.push({ role: "user", content: message });

    // 입력창을 비워 다음 질문을 입력할 수 있게 합니다.
    messageInput.value = "";

    // 응답 대기 중임을 사용자에게 알려줍니다.
    addMessage("assistant", "답변을 생성하는 중입니다...");

    // 방금 추가한 대기 메시지 요소를 기억합니다.
    const loadingMessage = chatMessages.lastElementChild;

    // try 블록에서 서버 API를 호출합니다.
    try {
        // FastAPI의 /api/chat 엔드포인트에 POST 요청을 보냅니다.
        const response = await fetch("/api/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                message: message,
                history: history.slice(0, -1),
                system_instruction: chatSettings.system_instruction,
                model: chatSettings.model,
                temperature: chatSettings.temperature,
                top_p: chatSettings.top_p,
                max_output_tokens: chatSettings.max_output_tokens,
            }),
        });

        // HTTP 응답이 실패 상태이면 오류를 발생시킵니다.
        if (!response.ok) {
            throw new Error(`서버 오류: ${response.status}`);
        }

        // 서버에서 받은 JSON 응답을 파싱합니다.
        const data = await response.json();

        // 대기 메시지 내용을 실제 답변으로 교체합니다.
        loadingMessage.textContent = data.reply;

        // 대화 기록에도 챗봇 답변을 저장합니다.
        history.push({ role: "assistant", content: data.reply });
    } catch (error) {
        // 오류가 발생하면 화면에 오류 안내를 표시합니다.
        loadingMessage.textContent = `오류가 발생했습니다. ${error.message}`;
    }
});
