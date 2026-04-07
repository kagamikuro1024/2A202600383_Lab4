"""
TravelBuddy Web Demo - Giao diện web hiện đại cho Agent Du lịch
Chạy tại: http://localhost:3636
"""

import sys
import os
import json
import time

# Thêm thư mục cha vào sys.path để import agent.py, tools.py
PARENT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, PARENT_DIR)
os.chdir(PARENT_DIR)  # Để agent.py tìm được system_prompt.txt

from flask import Flask, request, jsonify, Response, send_from_directory
from langchain_core.messages import SystemMessage, AIMessage, HumanMessage, BaseMessage
from agent import graph, SYSTEM_PROMPT, get_message_content

DEMO_DIR = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__, static_folder=os.path.join(DEMO_DIR, "static"))

# Lưu conversation history cho mỗi session
conversations = {}

# Danh sách tên thành phố trong database
_CITIES = [
    "Hà Nội", "Ha Noi", "Đà Nẵng", "Da Nang", "Phú Quốc", "Phu Quoc",
    "Hồ Chí Minh", "Ho Chi Minh", "Nha Trang", "Hạ Long", "Ha Long",
    "Cần Thơ", "Can Tho", "Quy Nhơn", "Quy Nhon", "Huế", "Hue"
]

def _is_new_trip_request(message: str) -> bool:
    """
    Phát hiện xem tin nhắn có phải là yêu cầu chuyến đi MỚI hoàn toàn không.
    Dấu hiệu: chứa cả điểm đi + điểm đến + keywords du lịch trong 1 câu.
    """
    msg_lower = message.lower()
    
    # Keywords cho yêu cầu tư vấn mới (chứa đủ thông tin)
    trip_keywords = ["muốn đi", "muon di", "tư vấn", "tu van", "gợi ý", "goi y",
                     "lập kế hoạch", "budget", "ngân sách", "ngan sach", "kinh phí",
                     "tìm chuyến bay", "tim chuyen bay", "đặt vé", "dat ve"]
    
    has_trip_keyword = any(kw in msg_lower for kw in trip_keywords)
    
    # Đếm số thành phố xuất hiện trong tin nhắn
    cities_found = [c for c in _CITIES if c.lower() in msg_lower]
    
    # Nếu có keyword du lịch + ít nhất 1 thành phố → nhiều khả năng là yêu cầu mới
    return has_trip_keyword and len(cities_found) >= 1

@app.route("/")
def index():
    return send_from_directory("static", "index.html")

@app.route("/static/<path:path>")
def serve_static(path):
    return send_from_directory("static", path)

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("message", "").strip()
    session_id = data.get("session_id", "default")

    if not user_message:
        return jsonify({"error": "Tin nhắn không được để trống"}), 400

    # Khởi tạo history cho session nếu chưa có
    if session_id not in conversations:
        conversations[session_id] = []

    # Smart detect: Nếu user đang hỏi chuyến đi mới hoàn toàn → tự xóa history cũ
    # để tránh LLM bị nhầm lẫn do context cũ
    if conversations[session_id] and _is_new_trip_request(user_message):
        print(f"  ↳ Phát hiện yêu cầu chuyến đi mới, xóa history cũ cho session {session_id}")
        conversations[session_id] = []

    def generate():
        try:
            # Gửi signal bắt đầu xử lý
            yield f"data: {json.dumps({'type': 'thinking', 'content': 'Đang suy nghĩ...'})}\n\n"

            # Thêm tin nhắn mới của user vào lịch sử
            all_messages = conversations[session_id] + [HumanMessage(content=user_message)]

            # Invoke the graph với TOÀN BỘ lịch sử hội thoại
            result = graph.invoke(
                {"messages": all_messages},
                config={"configurable": {"thread_id": session_id}}
            )

            # Lưu toàn bộ messages từ graph result
            conversations[session_id] = result["messages"]

            # Thu thập tool calls VÀ tool results
            tool_calls_info = []
            tool_results_info = []
            
            for msg in result["messages"]:
                # Tool calls (AIMessage có tool_calls)
                if hasattr(msg, 'tool_calls') and msg.tool_calls:
                    for tc in msg.tool_calls:
                        tool_calls_info.append({
                            "name": tc['name'],
                            "args": tc['args']
                        })
                
                # Tool results (ToolMessage chứa kết quả trả về)
                if msg.__class__.__name__ == 'ToolMessage':
                    tool_results_info.append({
                        "name": getattr(msg, 'name', 'unknown'),
                        "content": get_message_content(msg)
                    })

            # Gửi tool calls info
            if tool_calls_info:
                yield f"data: {json.dumps({'type': 'tools', 'content': tool_calls_info}, ensure_ascii=False)}\n\n"
                time.sleep(0.3)

            # Gửi tool results (kết quả từ search_flights, search_hotels, calculate_budget)
            if tool_results_info:
                yield f"data: {json.dumps({'type': 'tool_results', 'content': tool_results_info}, ensure_ascii=False)}\n\n"
                time.sleep(0.2)

            # Lấy response cuối cùng
            final = result["messages"][-1]
            content = get_message_content(final)

            if content:
                # Stream từng đoạn nhỏ để tạo hiệu ứng typing
                chunk_size = 8
                for i in range(0, len(content), chunk_size):
                    chunk = content[i:i+chunk_size]
                    yield f"data: {json.dumps({'type': 'content', 'content': chunk}, ensure_ascii=False)}\n\n"
                    time.sleep(0.02)

            yield f"data: {json.dumps({'type': 'done'})}\n\n"

        except Exception as e:
            yield f"data: {json.dumps({'type': 'error', 'content': str(e)}, ensure_ascii=False)}\n\n"

    return Response(generate(), mimetype="text/event-stream")

@app.route("/api/new-chat", methods=["POST"])
def new_chat():
    """Xóa lịch sử hội thoại của session"""
    data = request.json or {}
    session_id = data.get("session_id", "default")
    if session_id in conversations:
        del conversations[session_id]
    return jsonify({"status": "ok"})

@app.route("/api/suggestions", methods=["GET"])
def suggestions():
    """Trả về gợi ý câu hỏi mẫu"""
    sample_questions = [
        {"icon": "✈️", "text": "Tìm chuyến bay từ Hà Nội đến Đà Nẵng"},
        {"icon": "🏖️", "text": "Tôi muốn đi Phú Quốc từ Hồ Chí Minh, ngân sách 10 triệu cho 3 đêm"},
        {"icon": "🏨", "text": "Tìm khách sạn ở Nha Trang giá dưới 1 triệu/đêm"},
        {"icon": "💰", "text": "Tính ngân sách cho chuyến đi Đà Nẵng: vé bay 1.2 triệu, khách sạn 2 triệu"},
        {"icon": "🌴", "text": "Gợi ý chuyến đi từ Hà Nội đến Hạ Long"},
        {"icon": "🏛️", "text": "Tìm chuyến bay từ Hồ Chí Minh đến Huế"},
    ]
    return jsonify(sample_questions)


if __name__ == "__main__":
    print("=" * 60)
    print("🌍 TravelBuddy Web Demo")
    print("   Truy cập: http://localhost:3636")
    print("=" * 60)
    app.run(host="0.0.0.0", port=3636, debug=True)
