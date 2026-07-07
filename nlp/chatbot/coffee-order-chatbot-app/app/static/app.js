// ---------------------- 회원가입 / 로그인 처리 (모달 방식) ----------------------
// HTML에서 로그인 트리거(버튼)와 로그인 후 사용자 정보 영역을 가져옵니다.
const openLoginButton = document.getElementById("openLoginButton");
const authUserArea = document.getElementById("authUserArea");
const authWelcome = document.getElementById("authWelcome");
const logoutButton = document.getElementById("logoutButton");

// HTML에서 모달 전체와 닫기 버튼을 가져옵니다.
const authModalOverlay = document.getElementById("authModalOverlay");
const closeModalButton = document.getElementById("closeModalButton");

// HTML에서 로그인 화면 요소들을 가져옵니다.
const loginView = document.getElementById("loginView");
const loginUsername = document.getElementById("loginUsername");
const loginPassword = document.getElementById("loginPassword");
const submitLoginButton = document.getElementById("submitLoginButton");
const goSignupButton = document.getElementById("goSignupButton");

// HTML에서 회원가입 화면 요소들을 가져옵니다.
const signupView = document.getElementById("signupView");
const signupUsername = document.getElementById("signupUsername");
const signupPassword = document.getElementById("signupPassword");
const signupName = document.getElementById("signupName");
const submitSignupButton = document.getElementById("submitSignupButton");
const cancelSignupButton = document.getElementById("cancelSignupButton");

// 로그인 토큰과 사용자 이름을 브라우저에 저장해두는 키 이름입니다.
const TOKEN_KEY = "coffee_chatbot_access_token";
const USERNAME_KEY = "coffee_chatbot_username";

// 저장된 토큰이 있으면 Authorization 헤더에 담아 API 요청 시 함께 보내기 위한 함수입니다.
function authHeaders() {
    const token = localStorage.getItem(TOKEN_KEY);
    return token ? { Authorization: `Bearer ${token}` } : {};
}

// 로그인/비로그인 상태에 맞게 상단 트리거 영역을 갱신하는 함수입니다.
function renderAuthState() {
    const token = localStorage.getItem(TOKEN_KEY);
    const username = localStorage.getItem(USERNAME_KEY);
    if (token && username) {
        // 로그인 상태이면 로그인 버튼을 숨기고 사용자 정보를 보여줍니다.
        openLoginButton.style.display = "none";
        authUserArea.style.display = "flex";
        authWelcome.textContent = `${username}님, 환영합니다!`;
    } else {
        // 비로그인 상태이면 로그인 버튼을 보여줍니다.
        openLoginButton.style.display = "inline-block";
        authUserArea.style.display = "none";
    }
}

// 모달을 로그인 화면으로 맞춘 뒤 열어주는 함수입니다.
function openLoginModal() {
    showLoginView();
    authModalOverlay.style.display = "flex";
}

// 모달을 닫는 함수입니다.
function closeAuthModal() {
    authModalOverlay.style.display = "none";
}

// 모달 안에서 로그인 화면을 보여주는 함수입니다.
function showLoginView() {
    loginView.style.display = "flex";
    signupView.style.display = "none";
}

// 모달 안에서 회원가입 화면을 보여주는 함수입니다.
function showSignupView() {
    loginView.style.display = "none";
    signupView.style.display = "flex";
}

// 로그인 버튼(상단 트리거) 클릭 시 모달을 로그인 화면으로 엽니다.
openLoginButton.addEventListener("click", openLoginModal);

// 모달 닫기 버튼 클릭 시 모달을 닫습니다.
closeModalButton.addEventListener("click", closeAuthModal);

// 모달 바깥의 어두운 배경을 클릭하면 모달을 닫습니다.
authModalOverlay.addEventListener("click", (event) => {
    if (event.target === authModalOverlay) {
        closeAuthModal();
    }
});

// 로그인 화면의 "회원가입" 버튼을 누르면 회원가입 화면으로 전환합니다.
goSignupButton.addEventListener("click", showSignupView);

// 회원가입 화면의 "회원가입 취소" 버튼을 누르면 로그인 화면으로 돌아갑니다.
cancelSignupButton.addEventListener("click", () => {
    signupUsername.value = "";
    signupPassword.value = "";
    signupName.value = "";
    showLoginView();
});

// 회원가입 제출 버튼 클릭 이벤트를 처리합니다.
submitSignupButton.addEventListener("click", async () => {
    const username = signupUsername.value.trim();
    const password = signupPassword.value;
    const name = signupName.value.trim();
    if (!username || !password || !name) {
        alert("아이디, 비밀번호, 이름을 모두 입력해주세요.");
        return;
    }
    const response = await fetch("/auth/signup", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password, name }),
    });
    if (response.ok) {
        alert("회원가입이 완료되었습니다. 로그인해주세요.");
        // 가입 완료 후 방금 입력한 아이디를 로그인 화면에 채워주고 로그인 화면으로 돌아갑니다.
        signupPassword.value = "";
        signupName.value = "";
        loginUsername.value = username;
        showLoginView();
    } else {
        const data = await response.json().catch(() => ({}));
        alert(data.detail || "회원가입에 실패했습니다.");
    }
});

// 로그인 제출 버튼 클릭 이벤트를 처리합니다.
submitLoginButton.addEventListener("click", async () => {
    const username = loginUsername.value.trim();
    const password = loginPassword.value;
    if (!username || !password) {
        alert("아이디와 비밀번호를 입력해주세요.");
        return;
    }
    // 로그인 API는 OAuth2 표준에 맞춰 form-urlencoded 형식을 사용합니다.
    const body = new URLSearchParams();
    body.set("username", username);
    body.set("password", password);
    const response = await fetch("/auth/login", { method: "POST", body });
    if (response.ok) {
        const data = await response.json();
        localStorage.setItem(TOKEN_KEY, data.access_token);
        localStorage.setItem(USERNAME_KEY, username);
        loginPassword.value = "";
        renderAuthState();
        closeAuthModal();
        appendMessage("bot", `${username}님, 로그인되었습니다. 이제부터 장바구니와 주문내역이 회원님 계정에 저장됩니다.`);
        // 로그인 직후 회원 전용 장바구니를 다시 불러옵니다.
        await refreshCart();
    } else {
        const data = await response.json().catch(() => ({}));
        alert(data.detail || "로그인에 실패했습니다.");
    }
});

// 로그아웃 버튼 클릭 이벤트를 처리합니다.
logoutButton.addEventListener("click", async () => {
    localStorage.removeItem(TOKEN_KEY);
    localStorage.removeItem(USERNAME_KEY);
    renderAuthState();
    appendMessage("bot", "로그아웃되었습니다.");
    await refreshCart();
});

// 현재 장바구니를 서버에서 다시 불러와 화면을 갱신하는 함수입니다.
async function refreshCart() {
    const response = await fetch("/api/cart", { headers: { ...authHeaders() } });
    const data = await response.json();
    renderCart(data.cart, data.total);
}

// HTML에서 채팅창 요소를 가져옵니다.
const chatWindow = document.getElementById("chatWindow");
// HTML에서 입력 폼 요소를 가져옵니다.
const chatForm = document.getElementById("chatForm");
// HTML에서 사용자 메시지 입력창을 가져옵니다.
const messageInput = document.getElementById("messageInput");
// HTML에서 추천 개수 선택상자를 가져옵니다.
const topKSelect = document.getElementById("topK");
// HTML에서 전송 버튼을 가져옵니다.
const submitButton = document.getElementById("submitButton");
// HTML에서 서버 상태 표시 요소를 가져옵니다.
const serverStatus = document.getElementById("serverStatus");
// HTML에서 의도 표시 요소를 가져옵니다.
const intentText = document.getElementById("intentText");
// HTML에서 신뢰도 텍스트 요소를 가져옵니다.
const confidenceText = document.getElementById("confidenceText");
// HTML에서 신뢰도 막대 요소를 가져옵니다.
const confidenceBar = document.getElementById("confidenceBar");
// HTML에서 추천 목록 영역을 가져옵니다.
const recommendList = document.getElementById("recommendList");
// HTML에서 장바구니 목록 영역을 가져옵니다.
const cartList = document.getElementById("cartList");
// HTML에서 총액 표시 요소를 가져옵니다.
const totalPrice = document.getElementById("totalPrice");
// HTML에서 장바구니 비우기 버튼을 가져옵니다.
const clearCartButton = document.getElementById("clearCartButton");
// HTML에서 결제 버튼을 가져옵니다.
const checkoutButton = document.getElementById("checkoutButton");

// 금액 숫자를 원화 문자열로 변환하는 함수입니다.
function formatWon(value) {
    // Intl.NumberFormat을 사용하여 천 단위 쉼표를 적용합니다.
    return new Intl.NumberFormat("ko-KR").format(value) + "원";
}

// 채팅창에 메시지를 추가하는 함수입니다.
function appendMessage(role, text) {
    // 메시지 전체를 감싸는 div를 생성합니다.
    const messageDiv = document.createElement("div");
    // 역할에 따라 user 또는 bot 클래스를 추가합니다.
    messageDiv.className = `message ${role}`;
    // 봇 메시지이면 아바타를 추가합니다.
    if (role === "bot") {
        // 아바타 div를 생성합니다.
        const avatar = document.createElement("div");
        // 아바타 클래스를 적용합니다.
        avatar.className = "avatar";
        // 아바타 이모지를 설정합니다.
        avatar.textContent = "🤖";
        // 메시지 div에 아바타를 추가합니다.
        messageDiv.appendChild(avatar);
    }
    // 말풍선 div를 생성합니다.
    const bubble = document.createElement("div");
    // 말풍선 클래스를 적용합니다.
    bubble.className = "bubble";
    // XSS 방지를 위해 innerHTML 대신 textContent를 사용합니다.
    bubble.textContent = text;
    // 메시지 div에 말풍선을 추가합니다.
    messageDiv.appendChild(bubble);
    // 사용자 메시지이면 아바타를 오른쪽에 추가합니다.
    if (role === "user") {
        // 사용자 아바타 div를 생성합니다.
        const avatar = document.createElement("div");
        // 아바타 클래스를 적용합니다.
        avatar.className = "avatar";
        // 사용자 아바타 이모지를 설정합니다.
        avatar.textContent = "👤";
        // 메시지 div에 아바타를 추가합니다.
        messageDiv.appendChild(avatar);
    }
    // 채팅창에 메시지를 추가합니다.
    chatWindow.appendChild(messageDiv);
    // 새 메시지가 보이도록 스크롤을 맨 아래로 이동합니다.
    chatWindow.scrollTop = chatWindow.scrollHeight;
}

// 분석 결과 UI를 업데이트하는 함수입니다.
function updateAnalysis(intent, confidence) {
    // 의도 텍스트를 화면에 표시합니다.
    intentText.textContent = intent;
    // 신뢰도를 백분율로 계산합니다.
    const percent = Math.round(confidence * 100);
    // 신뢰도 텍스트를 화면에 표시합니다.
    confidenceText.textContent = `${percent}%`;
    // 신뢰도 막대 너비를 변경합니다.
    confidenceBar.style.width = `${percent}%`;
}

// 추천 메뉴 목록을 화면에 그리는 함수입니다.
function renderRecommendations(items, temperature, quantity) {
    // 기존 추천 목록을 초기화합니다.
    recommendList.innerHTML = "";
    // 추천 결과가 없으면 안내 문구를 표시합니다.
    if (!items || items.length === 0) {
        // 안내 문구를 설정합니다.
        recommendList.textContent = "추천 메뉴가 없습니다.";
        // 함수 실행을 종료합니다.
        return;
    }
    // 추천 메뉴 배열을 순회합니다.
    items.forEach((item) => {
        // 메뉴 카드 요소를 생성합니다.
        const card = document.createElement("article");
        // 메뉴 카드 클래스를 적용합니다.
        card.className = "menu-card";
        // 제목 행 요소를 생성합니다.
        const titleRow = document.createElement("div");
        // 제목 행 클래스를 적용합니다.
        titleRow.className = "menu-card-title";
        // 메뉴 이름 요소를 생성합니다.
        const name = document.createElement("span");
        // 메뉴 이름을 설정합니다.
        name.textContent = item.name;
        // 메뉴 가격 요소를 생성합니다.
        const price = document.createElement("span");
        // 메뉴 가격을 설정합니다.
        price.textContent = formatWon(item.price);
        // 제목 행에 메뉴 이름을 추가합니다.
        titleRow.appendChild(name);
        // 제목 행에 가격을 추가합니다.
        titleRow.appendChild(price);
        // 설명 요소를 생성합니다.
        const desc = document.createElement("p");
        // 설명 클래스를 적용합니다.
        desc.className = "menu-desc";
        // 메뉴 설명을 설정합니다.
        desc.textContent = item.description;
        // 태그 행 요소를 생성합니다.
        const tagRow = document.createElement("div");
        // 태그 행 클래스를 적용합니다.
        tagRow.className = "tag-row";
        // 맛 태그 배열을 순회합니다.
        item.taste_tags.forEach((tag) => {
            // 태그 요소를 생성합니다.
            const tagSpan = document.createElement("span");
            // 태그 클래스를 적용합니다.
            tagSpan.className = "tag";
            // 태그 텍스트를 설정합니다.
            tagSpan.textContent = tag;
            // 태그 행에 태그를 추가합니다.
            tagRow.appendChild(tagSpan);
        });
        // 담기 버튼을 생성합니다.
        const addButton = document.createElement("button");
        // 담기 버튼 클래스를 적용합니다.
        addButton.className = "add-button";
        // 담기 버튼 타입을 지정합니다.
        addButton.type = "button";
        // 담기 버튼 텍스트를 설정합니다.
        addButton.textContent = `${temperature.toUpperCase()} ${quantity}개 담기`;
        // 담기 버튼 클릭 이벤트를 등록합니다.
        addButton.addEventListener("click", () => addToCart(item.id, temperature, quantity));
        // 카드에 제목 행을 추가합니다.
        card.appendChild(titleRow);
        // 카드에 설명을 추가합니다.
        card.appendChild(desc);
        // 카드에 태그 행을 추가합니다.
        card.appendChild(tagRow);
        // 카드에 담기 버튼을 추가합니다.
        card.appendChild(addButton);
        // 추천 목록에 카드를 추가합니다.
        recommendList.appendChild(card);
    });
}

// 장바구니를 화면에 그리는 함수입니다.
function renderCart(cart, total) {
    // 기존 장바구니 목록을 초기화합니다.
    cartList.innerHTML = "";
    // 장바구니가 비어 있으면 안내 문구를 표시합니다.
    if (!cart || cart.length === 0) {
        // 비어 있음 문구를 설정합니다.
        cartList.textContent = "담긴 메뉴가 없습니다.";
    } else {
        // 장바구니 항목을 순회합니다.
        cart.forEach((item) => {
            // 항목 div를 생성합니다.
            const row = document.createElement("div");
            // 항목 클래스를 적용합니다.
            row.className = "cart-item";
            // 항목 내용을 설정합니다.
            row.textContent = `${item.name} / ${item.temperature.toUpperCase()} / ${item.quantity}개 / ${formatWon(item.subtotal)}`;
            // 장바구니 목록에 항목을 추가합니다.
            cartList.appendChild(row);
        });
    }
    // 총액을 화면에 표시합니다.
    totalPrice.textContent = formatWon(total || 0);
}

// 추천 메뉴를 장바구니에 추가하는 함수입니다.
async function addToCart(menuId, temperature, quantity) {
    // 장바구니 추가 API를 호출합니다.
    const response = await fetch("/api/cart/add", {
        // POST 방식으로 요청합니다.
        method: "POST",
        // JSON 형식의 요청임을 지정하고, 로그인 상태이면 Authorization 헤더도 함께 보냅니다.
        headers: { "Content-Type": "application/json", ...authHeaders() },
        // 요청 본문에 메뉴 ID, 온도, 수량을 담습니다.
        body: JSON.stringify({ menu_id: menuId, temperature, quantity, option_note: "" }),
    });
    // 응답 JSON을 파싱합니다.
    const data = await response.json();
    // 성공이면 장바구니 UI를 갱신합니다.
    if (data.ok) {
        // 봇 메시지로 담기 완료를 안내합니다.
        appendMessage("bot", `${data.item.name} ${data.item.quantity}개를 장바구니에 담았습니다.`);
        // 장바구니 목록과 총액을 갱신합니다.
        renderCart(data.cart, data.total);
    } else {
        // 실패 메시지를 안내합니다.
        appendMessage("bot", data.message || "장바구니에 담지 못했습니다.");
    }
}

// 챗봇 메시지를 서버로 전송하는 함수입니다.
async function sendChat(message) {
    // 전송 버튼을 비활성화합니다.
    submitButton.disabled = true;
    // 전송 버튼 텍스트를 로딩 상태로 변경합니다.
    submitButton.textContent = "처리 중...";
    // 로딩 메시지를 채팅창에 추가합니다.
    appendMessage("bot", "주문 의도를 분석하고 메뉴를 찾고 있습니다...");
    // 챗봇 API를 호출합니다.
    const response = await fetch("/api/chat", {
        // POST 방식으로 요청합니다.
        method: "POST",
        // JSON 요청 헤더를 설정하고, 로그인 상태이면 Authorization 헤더도 함께 보냅니다.
        headers: { "Content-Type": "application/json", ...authHeaders() },
        // 사용자 메시지와 추천 개수를 본문에 담습니다.
        body: JSON.stringify({ message, top_k: Number(topKSelect.value) }),
    });
    // 응답 JSON을 파싱합니다.
    const data = await response.json();
    // 분석 결과 UI를 갱신합니다.
    updateAnalysis(data.intent, data.confidence);
    // 추천 메뉴 UI를 갱신합니다.
    renderRecommendations(data.recommendations, data.temperature, data.quantity);
    // 장바구니 UI를 갱신합니다.
    renderCart(data.cart, data.total);
    // AI 답변을 채팅창에 추가합니다.
    appendMessage("bot", data.message);
    // 전송 버튼을 다시 활성화합니다.
    submitButton.disabled = false;
    // 전송 버튼 텍스트를 원래대로 변경합니다.
    submitButton.textContent = "☕ 전송";
}

// 입력 폼 제출 이벤트를 처리합니다.
chatForm.addEventListener("submit", async (event) => {
    // 폼의 기본 새로고침 동작을 막습니다.
    event.preventDefault();
    // 입력값 앞뒤 공백을 제거합니다.
    const message = messageInput.value.trim();
    // 입력값이 비어 있으면 함수 실행을 중단합니다.
    if (!message) return;
    // 사용자 메시지를 화면에 추가합니다.
    appendMessage("user", message);
    // 입력창을 비웁니다.
    messageInput.value = "";
    // 서버로 메시지를 전송합니다.
    await sendChat(message);
});

// 빠른 입력 버튼 전체를 순회합니다.
document.querySelectorAll(".chip").forEach((button) => {
    // 각 버튼에 클릭 이벤트를 등록합니다.
    button.addEventListener("click", () => {
        // 버튼에 저장된 예시 문장을 입력창에 넣습니다.
        messageInput.value = button.dataset.example;
        // 입력창에 포커스를 이동합니다.
        messageInput.focus();
    });
});

// 장바구니 비우기 버튼 클릭 이벤트를 등록합니다.
clearCartButton.addEventListener("click", async () => {
    // 장바구니 초기화 API를 호출합니다.
    const response = await fetch("/api/cart/clear", { method: "POST", headers: { ...authHeaders() } });
    // 응답 JSON을 파싱합니다.
    const data = await response.json();
    // 장바구니 UI를 갱신합니다.
    renderCart(data.cart, data.total);
    // 완료 메시지를 표시합니다.
    appendMessage("bot", "장바구니를 비웠습니다.");
});

// 결제 버튼 클릭 이벤트를 등록합니다.
checkoutButton.addEventListener("click", async () => {
    // 결제 API를 호출합니다.
    const response = await fetch("/api/checkout", {
        method: "POST",
        headers: { "Content-Type": "application/json", ...authHeaders() },
        body: JSON.stringify({ method: "demo" }),
    });
    // 응답 JSON을 파싱합니다.
    const data = await response.json();
    // 결제 안내 메시지를 채팅창에 표시합니다.
    appendMessage("bot", data.message + (data.ok ? `\n총 결제 예정 금액: ${formatWon(data.total)}` : ""));
});

// 서버 상태를 확인하는 함수입니다.
async function checkHealth() {
    // 서버 상태 API를 호출합니다.
    const response = await fetch("/api/health");
    // 응답 JSON을 파싱합니다.
    const data = await response.json();
    // OpenAI 설정 여부에 따라 상태 문구를 변경합니다.
    serverStatus.textContent = data.openai_ready ? "OpenAI 연결 준비됨" : "로컬 모드";
}

// 페이지가 열리면 서버 상태를 확인합니다.
checkHealth();
// 페이지가 열리면 로그인 상태 UI를 갱신합니다.
renderAuthState();
// 페이지가 열리면 (로그인 상태라면 회원 전용) 장바구니를 불러옵니다.
refreshCart();
