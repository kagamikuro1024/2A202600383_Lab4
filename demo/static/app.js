/**
 * TravelBuddy - Web Demo App Logic
 * Streaming chat with tool call visualization
 */

// ====== DOM Elements ======
const chatArea = document.getElementById('chat-area');
const messagesContainer = document.getElementById('messages-container');
const welcomeScreen = document.getElementById('welcome-screen');
const messageInput = document.getElementById('message-input');
const btnSend = document.getElementById('btn-send');
const btnNewChat = document.getElementById('btn-new-chat');
const statusBadge = document.getElementById('status-badge');
const statusText = statusBadge.querySelector('.status-text');
const suggestionsGrid = document.getElementById('suggestions-grid');
const particlesContainer = document.getElementById('particles');

// ====== State ======
let isProcessing = false;
let sessionId = 'session_' + Date.now();

// ====== Init ======
document.addEventListener('DOMContentLoaded', () => {
    loadSuggestions();
    createParticles();
    autoResizeTextarea();
    messageInput.focus();
});

// ====== Particles ======
function createParticles() {
    const count = 15;
    for (let i = 0; i < count; i++) {
        const particle = document.createElement('div');
        particle.classList.add('particle');
        const size = Math.random() * 4 + 2;
        particle.style.width = `${size}px`;
        particle.style.height = `${size}px`;
        particle.style.left = `${Math.random() * 100}%`;
        particle.style.animationDuration = `${Math.random() * 15 + 10}s`;
        particle.style.animationDelay = `${Math.random() * 10}s`;
        particle.style.opacity = `${Math.random() * 0.3 + 0.1}`;
        particlesContainer.appendChild(particle);
    }
}

// ====== Suggestions ======
async function loadSuggestions() {
    try {
        const resp = await fetch('/api/suggestions');
        const suggestions = await resp.json();
        suggestionsGrid.innerHTML = '';
        suggestions.forEach(s => {
            const chip = document.createElement('div');
            chip.className = 'suggestion-chip';
            chip.innerHTML = `<span class="chip-icon">${s.icon}</span><span>${s.text}</span>`;
            chip.addEventListener('click', () => sendMessage(s.text));
            suggestionsGrid.appendChild(chip);
        });
    } catch (err) {
        console.error('Failed to load suggestions:', err);
    }
}

// ====== Textarea Auto-resize ======
function autoResizeTextarea() {
    messageInput.addEventListener('input', () => {
        messageInput.style.height = 'auto';
        messageInput.style.height = Math.min(messageInput.scrollHeight, 120) + 'px';
    });
}

// ====== Event Listeners ======
messageInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        if (!isProcessing) {
            sendMessage(messageInput.value);
        }
    }
});

btnSend.addEventListener('click', () => {
    if (!isProcessing) {
        sendMessage(messageInput.value);
    }
});

btnNewChat.addEventListener('click', async () => {
    // Xóa history trên server
    try {
        await fetch('/api/new-chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ session_id: sessionId })
        });
    } catch (e) { /* ignore */ }

    sessionId = 'session_' + Date.now();
    messagesContainer.innerHTML = '';
    messagesContainer.classList.remove('active');
    welcomeScreen.style.display = '';
    messageInput.value = '';
    messageInput.style.height = 'auto';
    messageInput.focus();
});

// ====== Send Message ======
async function sendMessage(text) {
    text = text.trim();
    if (!text || isProcessing) return;

    isProcessing = true;
    setStatus('thinking');
    btnSend.classList.add('loading');
    btnSend.disabled = true;

    // Hide welcome, show messages
    welcomeScreen.style.display = 'none';
    messagesContainer.classList.add('active');

    // Add user message
    addMessage('user', text);
    messageInput.value = '';
    messageInput.style.height = 'auto';

    // Add thinking indicator
    const thinkingEl = addThinkingIndicator();

    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: text, session_id: sessionId })
        });

        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        let assistantBubble = null;
        let assistantContent = '';
        let toolsContainer = null;

        while (true) {
            const { done, value } = await reader.read();
            if (done) break;

            const chunk = decoder.decode(value, { stream: true });
            const lines = chunk.split('\n');

            for (const line of lines) {
                if (!line.startsWith('data: ')) continue;
                const jsonStr = line.slice(6);
                
                let data;
                try {
                    data = JSON.parse(jsonStr);
                } catch { continue; }

                if (data.type === 'thinking') {
                    // Already showing thinking indicator
                    continue;
                }

                if (data.type === 'tools') {
                    // Remove thinking, show tool calls
                    thinkingEl.remove();

                    // Create assistant message with tool calls
                    const msgEl = createAssistantMessageElement();
                    toolsContainer = document.createElement('div');
                    toolsContainer.className = 'tool-calls-container';

                    data.content.forEach(tc => {
                        const badge = document.createElement('div');
                        badge.className = 'tool-call-badge';
                        const argsStr = formatToolArgs(tc.args);
                        badge.innerHTML = `
                            <span class="tool-icon">🔧</span>
                            <span class="tool-name">${tc.name}</span>
                            <span class="tool-args">${argsStr}</span>
                        `;
                        toolsContainer.appendChild(badge);
                    });

                    const bubble = msgEl.querySelector('.message-bubble');
                    bubble.insertBefore(toolsContainer, bubble.firstChild);
                    assistantBubble = bubble;
                    messagesContainer.appendChild(msgEl);
                    scrollToBottom();
                    continue;
                }

                if (data.type === 'tool_results') {
                    // Hiển thị kết quả trả về từ các tools (flights, hotels, budget)
                    if (thinkingEl.parentNode) thinkingEl.remove();

                    if (!assistantBubble) {
                        const msgEl = createAssistantMessageElement();
                        assistantBubble = msgEl.querySelector('.message-bubble');
                        messagesContainer.appendChild(msgEl);
                    }

                    const resultsContainer = document.createElement('div');
                    resultsContainer.className = 'tool-results-container';

                    data.content.forEach(tr => {
                        const resultCard = document.createElement('details');
                        resultCard.className = 'tool-result-card';
                        resultCard.open = true; // Mặc định mở

                        const toolLabel = getToolLabel(tr.name);
                        resultCard.innerHTML = `
                            <summary class="tool-result-header">
                                <span class="tool-result-icon">${toolLabel.icon}</span>
                                <span class="tool-result-title">${toolLabel.title}</span>
                                <svg class="chevron" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg>
                            </summary>
                            <div class="tool-result-body">${formatMarkdown(tr.content)}</div>
                        `;
                        resultsContainer.appendChild(resultCard);
                    });

                    assistantBubble.appendChild(resultsContainer);
                    scrollToBottom();
                    continue;
                }

                if (data.type === 'content') {
                    // Remove thinking if still present
                    if (thinkingEl.parentNode) thinkingEl.remove();

                    if (!assistantBubble) {
                        const msgEl = createAssistantMessageElement();
                        assistantBubble = msgEl.querySelector('.message-bubble');
                        messagesContainer.appendChild(msgEl);
                    }

                    assistantContent += data.content;
                    // Find or create the text container (after tool calls if they exist)
                    let textEl = assistantBubble.querySelector('.message-text');
                    if (!textEl) {
                        textEl = document.createElement('div');
                        textEl.className = 'message-text';
                        assistantBubble.appendChild(textEl);
                    }
                    textEl.innerHTML = formatMarkdown(assistantContent);
                    scrollToBottom();
                    continue;
                }

                if (data.type === 'error') {
                    thinkingEl.remove();
                    addMessage('assistant', `❌ Lỗi: ${data.content}`);
                    continue;
                }

                if (data.type === 'done') {
                    // Add timestamp to the last assistant message
                    if (assistantBubble) {
                        const msgEl = assistantBubble.closest('.message');
                        const timeEl = document.createElement('div');
                        timeEl.className = 'message-time';
                        timeEl.textContent = getCurrentTime();
                        msgEl.querySelector('.message-content').appendChild(timeEl);
                    }
                }
            }
        }

    } catch (err) {
        if (thinkingEl.parentNode) thinkingEl.remove();
        addMessage('assistant', `❌ Không thể kết nối đến server: ${err.message}`);
    } finally {
        isProcessing = false;
        setStatus('ready');
        btnSend.classList.remove('loading');
        btnSend.disabled = false;
        messageInput.focus();
    }
}

// ====== UI Helpers ======
function addMessage(role, content) {
    const msgEl = document.createElement('div');
    msgEl.className = `message ${role}`;

    const avatar = role === 'user' ? '👤' : '🤖';

    msgEl.innerHTML = `
        <div class="message-avatar">${avatar}</div>
        <div class="message-content">
            <div class="message-bubble">
                <div class="message-text">${role === 'user' ? escapeHtml(content) : formatMarkdown(content)}</div>
            </div>
            <div class="message-time">${getCurrentTime()}</div>
        </div>
    `;

    messagesContainer.appendChild(msgEl);
    scrollToBottom();
    return msgEl;
}

function createAssistantMessageElement() {
    const msgEl = document.createElement('div');
    msgEl.className = 'message assistant';
    msgEl.innerHTML = `
        <div class="message-avatar">🤖</div>
        <div class="message-content">
            <div class="message-bubble"></div>
        </div>
    `;
    return msgEl;
}

function addThinkingIndicator() {
    const el = document.createElement('div');
    el.className = 'thinking-indicator';
    el.innerHTML = `
        <div class="message-avatar" style="background: var(--accent-gradient); box-shadow: 0 2px 8px var(--accent-glow);">🤖</div>
        <div class="thinking-bubble">
            <div class="thinking-dots">
                <span></span><span></span><span></span>
            </div>
            <span>TravelBuddy đang suy nghĩ...</span>
        </div>
    `;
    messagesContainer.appendChild(el);
    scrollToBottom();
    return el;
}

function setStatus(status) {
    if (status === 'thinking') {
        statusBadge.classList.add('thinking');
        statusText.textContent = 'Đang xử lý...';
    } else {
        statusBadge.classList.remove('thinking');
        statusText.textContent = 'Sẵn sàng';
    }
}

function scrollToBottom() {
    requestAnimationFrame(() => {
        chatArea.scrollTop = chatArea.scrollHeight;
    });
}

function getCurrentTime() {
    const now = new Date();
    return now.toLocaleTimeString('vi-VN', { hour: '2-digit', minute: '2-digit' });
}

// ====== Formatting ======
function escapeHtml(str) {
    const div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
}

function formatMarkdown(text) {
    if (!text) return '';

    // Escape HTML first
    let html = escapeHtml(text);

    // Bold: **text**
    html = html.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');

    // Italic: *text*
    html = html.replace(/(?<!\*)\*(?!\*)(.*?)(?<!\*)\*(?!\*)/g, '<em>$1</em>');

    // Line breaks
    html = html.replace(/\n/g, '<br>');

    // Horizontal rules
    html = html.replace(/(^|<br>)-{3,}(<br>|$)/g, '$1<hr style="border:none;border-top:1px solid var(--border-color);margin:12px 0;">$2');

    return html;
}

function formatToolArgs(args) {
    if (!args) return '';
    const parts = [];
    for (const [key, value] of Object.entries(args)) {
        if (typeof value === 'number') {
            parts.push(`${key}: ${value.toLocaleString('vi-VN')}`);
        } else {
            parts.push(`${key}: ${value}`);
        }
    }
    return `(${parts.join(', ')})`;
}

function getToolLabel(toolName) {
    const labels = {
        'search_flights': { icon: '✈️', title: 'Kết quả tìm chuyến bay' },
        'search_hotels': { icon: '🏨', title: 'Kết quả tìm khách sạn' },
        'calculate_budget': { icon: '💰', title: 'Kết quả tính ngân sách' }
    };
    return labels[toolName] || { icon: '📋', title: toolName };
}
