# 🌍 TravelBuddy - AI Travel Planning Assistant

> **Trợ lý du lịch thông minh** powered by LangGraph + OpenAI GPT-4o-mini  
> Giúp bạn lên kế hoạch chuyến đi hoàn hảo với ngân sách, tìm chuyến bay, khách sạn và gợi ý du lịch.

![Status](https://img.shields.io/badge/status-active-brightgreen)
![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

---

## 📋 Table of Contents

- [Features](#features)
- [Architecture](#architecture)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage Examples](#usage-examples)
- [Project Structure](#project-structure)
- [Testing](#testing)
- [Configuration](#configuration)
- [Troubleshooting](#troubleshooting)

---

## ✨ Features

### 🎯 Core Capabilities

- **🔬 Smart Tool Chaining:** Tự động chuỗi nhiều công cụ (flights → budget → hotels)
- **💬 Natural Conversation:** Giao tiếp tiếng Việt tự nhiên, không máy móc
- **💰 Budget Management:** Tính toán ngân sách chi tiết, tracking chi phí realtime
- **✈️ Flight Search:** Tra cứu chuyến bay với giá, hãng, giờ bay
- **🏨 Hotel Recommendations:** Danh sách khách sạn sắp xếp theo rating
- **🛡️ Smart Guardrails:** Từ chối yêu cầu ngoài du lịch một cách lịch sự
- **📊 Comprehensive Reports:** Breakdown chi phí, ngân sách còn lại, gợi ý du lịch

### 🚀 Advanced Features

- **Multi-step planning:** Combine flights + budget + hotels dalam 1 request
- **Context Awareness:** Nhớ conversation history, maintain context
- **Slot Filling:** Thông minh hỏi thêm thông tin khi cần
- **Error Handling:** Graceful degradation khi không tìm thấy dữ liệu

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    USER INTERFACE                        │
│                  (Chat Loop - agent.py)                 │
└─────────────────┬───────────────────────────────────────┘
                  │
┌─────────────────▼───────────────────────────────────────┐
│              LANGGRAPH STATE MACHINE                      │
│  ┌──────────────────────────────────────────────────┐   │
│  │  Agent Node (LLM with Tool Binding)              │   │
│  │  • Receives user message                         │   │
│  │  • Decides which tool to use (or reply directly) │   │
│  │  • Binds tools using langchain_openai            │   │
│  └──────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────┐   │
│  │  Tool Node (Executes Tools)                      │   │
│  │  • search_flights()                              │   │
│  │  • calculate_budget()                            │   │
│  │  • search_hotels()                               │   │
│  └──────────────────────────────────────────────────┘   │
└─────────────────┬───────────────────────────────────────┘
                  │
┌─────────────────▼───────────────────────────────────────┐
│                  TOOLS LAYER (tools.py)                  │
│  ├─ search_flights(origin, destination)                 │
│  ├─ search_hotels(city, max_price_per_night)            │
│  └─ calculate_budget(total_budget, expenses)            │
└─────────────────┬───────────────────────────────────────┘
                  │
┌─────────────────▼───────────────────────────────────────┐
│                  DATA LAYER (Mock Data)                  │
│  ├─ FLIGHTS_DB (23 routes, 50+ flights)                 │
│  └─ HOTELS_DB (8 cities, 40+ hotels)                    │
└─────────────────────────────────────────────────────────┘
```

### Key Components

| Component | File | Purpose |
|-----------|------|---------|
| **Agent Logic** | `agent.py` | LangGraph state machine + chat loop |
| **Tools** | `tools.py` | Flight/hotel search + budget calculator |
| **System Prompt** | `system_prompt.txt` | Agent personality + instructions |
| **Mock Data** | `tools.py` | FLIGHTS_DB + HOTELS_DB |
| **Tests** | `test_runner.py` | 5 comprehensive test scenarios |

---

## 📦 Installation

### Prerequisites

- Python 3.8+
- pip or poetry
- OpenAI API key

### Step 1: Clone Repository

```bash
cd d:\gitHub\AI_20k\lab4_agent
```

### Step 2: Create Virtual Environment

```bash
python -m venv venv
.\venv\Scripts\Activate.ps1  # Windows
# or
source venv/bin/activate      # Linux/Mac
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

Or manually:
```bash
pip install langchain langchain-openai langgraph python-dotenv
```

### Step 4: Setup Environment Variables

Create `.env` file:

```env
OPENAI_API_KEY=sk-your-api-key-here
MODEL_NAME=gpt-4o-mini  # Default: gpt-4o-mini, can change to gpt-4 etc
```

### Step 5: Verify Installation

```bash
python test_api.py  # Should print a greeting
```

---

## 📁 Project Structure

```
lab4_agent/
├── agent.py                    # LangGraph state machine + chat loop
├── tools.py                    # Flight/hotel/budget tools + mock data
├── system_prompt.txt           # Agent personality + instructions
├── test_api.py                 # Simple API test
├── test_scenarios.py           # 5 test case definitions
├── test_runner.py              # Test suite runner
├── requirements.txt            # Python dependencies
├── .env                        # API keys (add this)
├── Readme.md                   # This file
├── README_TESTS.md             # Test documentation
├── test_results.md             # Test execution results
├── report_agent.md             # Agent evaluation report
└── venv/                       # Virtual environment
```

---

## 🧪 Testing

### Run All Tests

```bash
.\venv\Scripts\Activate.ps1
python test_runner.py
```

This will:
1. Execute 5 test scenarios
2. Generate `test_results.md` (raw outputs)
3. Generate `report_agent.md` (evaluation report)

### Test Coverage

| Test | Purpose | Expected | Status |
|------|---------|----------|--------|
| Test 1 | Direct Answer (no tools) | Agent asks clarifying questions | ✅ PASS |
| Test 2 | Single Tool Call | Calls search_flights with 4 results | ✅ PASS |
| Test 3 | Multi-Step Chaining | Chains 3 tools automatically | ✅ PASS |
| Test 4 | Missing Info | Asks for missing details gracefully | ✅ PASS |
| Test 5 | Guardrail/Refusal | Refuses out-of-scope requests politely | ✅ PASS |

**Current Status: 5/5 PASSING (100%)**

See [README_TESTS.md](README_TESTS.md) for detailed test documentation.

---

## ⚙️ Configuration

### Environment Variables

```env
# Required
OPENAI_API_KEY=sk-...  # Your OpenAI API key

# Optional
MODEL_NAME=gpt-4o-mini # Default model (can use gpt-4)
```

### System Prompt Customization

Edit `system_prompt.txt` to change:
- Agent personality (persona)
- Tool calling rules
- Response format
- Guardrails

Key sections:
- `<persona>` - Agent personality
- `<rules>` - Behavior rules
- `<quick_decision_tree>` - Tool calling logic
- `<response_format>` - Output structure
- `<constraints>` - Guardrails

### Mock Data Customization

Edit `tools.py`:
- `FLIGHTS_DB` - Add/remove flights
- `HOTELS_DB` - Add/remove hotels
- Prices, airlines, locations

---

## 🐛 Troubleshooting

### Issue: ModuleNotFoundError: No module named 'langgraph'

**Solution:**
```bash
.\venv\Scripts\Activate.ps1  # Make sure venv is activated
pip install -r requirements.txt
```

### Issue: OpenAI API Key Not Found

**Solution:**
1. Create `.env` file in project root
2. Add: `OPENAI_API_KEY=sk-your-key`
3. Restart agent

### Issue: Agent Not Calling Tools

**Possible causes:**
- User input doesn't match tool trigger patterns (see system_prompt.txt)
- LLM decided direct answer is better
- Model confusion - try test_runner.py to verify

**Debug:**
- Check console output for "↳ Gọi tool:" logs
- Review system_prompt.txt <quick_decision_tree>

### Issue: Slow Response Time

**Possible causes:**
- OpenAI API latency (~2-5s normal)
- Network issues
- Model overloaded

**Solution:**
- Switch to faster model: `MODEL_NAME=gpt-4o-mini` (already default)
- Check internet connection
- Wait during peak hours

---

## 📊 Performance Metrics

Based on test suite results:

| Metric | Result |
|--------|--------|
| Tool Calling Accuracy | **100%** ✅ |
| Tool Chaining Logic | **Perfect** ✅ |
| Average Response Time | **~3-5s** (API dependent) |
| Pass Rate (All Tests) | **100% (5/5)** ✅ |
| Vietnamese Quality | **Native-like** ✅ |

---

## 🎯 Roadmap

- [x] Core agent implementation
- [x] Tool chaining (flights + budget + hotels)
- [x] Mock data (23 flight routes, 40+ hotels)
- [x] System prompt with guardrails
- [x] Test suite (5 scenarios)
- [ ] Database integration (replace mock data)
- [ ] User authentication
- [ ] Booking integration
- [ ] Web UI (Streamlit/FastAPI)
- [ ] Multi-language support
- [ ] Analytics dashboard

---

## 📚 Resources

### Useful Links

- [LangGraph Documentation](https://python.langchain.com/docs/langgraph/)
- [OpenAI API Reference](https://platform.openai.com/docs/api-reference)
- [LangChain Documentation](https://python.langchain.com/docs/)

### Project Files

- [System Prompt](system_prompt.txt) - Agent instructions
- [Test Documentation](README_TESTS.md) - Testing guide
- [Test Results](test_results.md) - Latest test outputs
- [Agent Report](report_agent.md) - Evaluation metrics

---

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 👤 Author

**AI Lab 4 - University Project**

- Created: April 2026
- Language: Python 3.8+
- Framework: LangGraph + OpenAI

