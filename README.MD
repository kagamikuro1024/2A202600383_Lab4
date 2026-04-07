# 🌍 TravelBuddy — Trợ lý Du lịch AI

> Agent du lịch thông minh sử dụng **LangGraph + OpenAI GPT-4o-mini**, hỗ trợ tìm chuyến bay, đặt khách sạn và quản lý ngân sách du lịch Việt Nam.

---

## ✨ Tính năng

- **Tool Chaining tự động:** `search_flights → calculate_budget → search_hotels`
- **Giao tiếp tiếng Việt** tự nhiên, slot filling thông minh
- **23 tuyến bay**, **40+ khách sạn** tại 8 thành phố (mock data)
- **Guardrails:** Từ chối yêu cầu ngoài phạm vi du lịch
- **Web Demo** hiện đại với streaming response + tool visualization

---

## 🏗️ Kiến trúc

```
User Input → [Agent Node (LLM)] → quyết định gọi tool hay trả lời trực tiếp
                    ↓
             [Tool Node] → search_flights / search_hotels / calculate_budget
                    ↓
             [Agent Node] → format response → User
```

---

## 📁 Cấu trúc Project

```
lab4_agent/
├── agent.py              # LangGraph state machine + ReAct loop
├── tools.py              # 3 tools + FLIGHTS_DB & HOTELS_DB
├── system_prompt.txt     # Persona, rules, response format, guardrails
├── .env                  # OPENAI_API_KEY
├── demo/
│   ├── web_demo.py       # Flask server (port 3636)
│   └── static/           # HTML/CSS/JS frontend
├── test/
│   ├── test_api.py       # Kiểm tra API key
│   ├── test_scenarios.py # 5 test cases
│   └── test_runner.py    # Chạy test + xuất report
├── test_results.md       # Kết quả test
└── report_agent.md       # Báo cáo đánh giá agent
```

---

## 🚀 Cài đặt & Chạy

```bash
# 1. Tạo virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1        # Windows
# source venv/bin/activate         # Linux/Mac

# 2. Cài dependencies
pip install langchain langchain-openai langgraph python-dotenv flask

# 3. Tạo file .env
echo OPENAI_API_KEY=sk-your-key > .env

# 4. Chạy agent (CLI)
python agent.py

# 5. Chạy Web Demo
cd demo
python web_demo.py
# → Truy cập http://localhost:3636
```

---

## 🧪 Testing

```bash
cd test
python test_runner.py
```

| # | Test Case | Mục đích | Kết quả |
|---|-----------|----------|---------|
| 1 | Direct Answer | Trả lời không cần tool | ✅ |
| 2 | Single Tool | Gọi `search_flights` | ✅ |
| 3 | Multi-Step Chain | Chain 3 tools tự động | ✅ |
| 4 | Slot Filling | Hỏi thêm thông tin thiếu | ✅ |
| 5 | Guardrail | Từ chối câu hỏi ngoài scope | ✅ |

**Kết quả: 5/5 PASS (100%)**

---

## 🔧 3 Tools

| Tool | Tham số | Mô tả |
|------|---------|-------|
| `search_flights` | `origin`, `destination` | Tìm chuyến bay giữa 2 thành phố |
| `search_hotels` | `city`, `max_price_per_night` | Tìm khách sạn theo budget |
| `calculate_budget` | `total_budget`, `expenses` | Tính chi phí còn lại |

---

## 👤 Thông tin

- **Môn học:** AI Lab 4 — Agent & Tool Calling
- **Framework:** LangGraph + LangChain + OpenAI
- **Ngày tạo:** Tháng 4/2026
