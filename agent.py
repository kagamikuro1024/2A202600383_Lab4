from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, AIMessage, BaseMessage
from tools import search_flights, search_hotels, calculate_budget
from dotenv import load_dotenv
import os
import sys

load_dotenv()

# 1. Đọc System Prompt (có error handling)
try:
    with open("system_prompt.txt", "r", encoding="utf-8") as f:
        SYSTEM_PROMPT = f.read()
except FileNotFoundError:
    print("Lỗi: Không tìm thấy file 'system_prompt.txt'")
    sys.exit(1)
except Exception as e:
    print(f"Lỗi khi đọc system_prompt.txt: {e}")
    sys.exit(1)

# 1.1 Config
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")
MAX_ITERATIONS = 10  # Tránh infinite loop

# 2. Khai báo State
class AgentState(TypedDict):
    messages: Annotated[list, add_messages]

# 3. Khởi tạo LLM và Tools
tools_list = [search_flights, search_hotels, calculate_budget]
llm = ChatOpenAI(model=MODEL_NAME)
llm_with_tools = llm.bind_tools(tools_list, tool_choice="auto")

# 4. Agent Node (cải tiến)
def agent_node(state: AgentState):
    messages = state["messages"]
    
    # Cải tiến 1: Check empty messages trước
    if not messages:
        return {"messages": []}
    
    # Cải tiến 2: Tránh thêm SystemMessage lặp lại (chỉ thêm lần đầu)
    if not any(isinstance(m, SystemMessage) for m in messages):
        messages = [SystemMessage(content=SYSTEM_PROMPT)] + messages

    try:
        response = llm_with_tools.invoke(messages)
    except Exception as e:
        # Cải tiến 3: Xử lý lỗi API
        error_msg = f"Lỗi LLM: {str(e)}"
        print(error_msg)
        return {"messages": [AIMessage(content=error_msg)]}

    # Cải tiến 4: Enhanced logging
    if response.tool_calls:
        for tc in response.tool_calls:
            print(f"  ↳ Gọi tool: {tc['name']}({tc['args']})")
    else:
        print(f"  ↳ Trả lời trực tiếp (không cần tool)")

    return {"messages": [response]}

# 5. Xây dựng Graph
builder = StateGraph(AgentState)
builder.add_node("agent", agent_node)

tool_node = ToolNode(tools_list)
builder.add_node("tools", tool_node)

# Khai báo edges
builder.add_edge(START, "agent")
builder.add_conditional_edges("agent", tools_condition)
builder.add_edge("tools", "agent")

graph = builder.compile()

# Helper function: Lấy content từ message (BaseMessage hoặc dict)
def get_message_content(message) -> str:
    """Extract content from BaseMessage or dict safely, always returns str"""
    if isinstance(message, BaseMessage):
        content = message.content
        # Handle multimodal content (list of blocks)
        if isinstance(content, list):
            return "".join(str(item) for item in content)
        return str(content) if content else ""
    elif isinstance(message, dict):
        content = message.get("content", "")
        if isinstance(content, list):
            return "".join(str(item) for item in content)
        return str(content) if content else ""
    return str(message)
if __name__ == "__main__":
    print("=" * 60)
    print("🌍 TravelBuddy – Trợ lý Du lịch Thông minh")
    print("   Mô tả chuyến du lịch hoặc đặt câu hỏi về du lịch")
    print("   Gõ 'quit'/'exit'/'q' để thoát")
    print("=" * 60)

    iteration_count = 0
    conversation_history = []

    while True:
        try:
            user_input = input("\n👤 Bạn: ").strip()
            
            # Cải tiến 5: Check empty input
            if not user_input:
                print("   (Vui lòng nhập gì đó)")
                continue
            
            if user_input.lower() in ("quit", "exit", "q"):
                print("\n👋 Tạm biệt! Chúc bạn có chuyến đi tuyệt vời!")
                break

            print("\n⏳ TravelBuddy đang suy nghĩ...")
            iteration_count = 0
            
            # Cải tiến 6: Invoke graph với message input
            result = graph.invoke(
                {"messages": [("human", user_input)]},
                config={"configurable": {"thread_id": "default"}}
            )
            
            # Cải tiến 7: Display final response + tool calls info
            final = result["messages"][-1]
            
            # Hiển thị tool calls (nếu có)
            if hasattr(final, 'tool_calls') and final.tool_calls:
                print(f"\n🔧 Công cụ được sử dụng:")
                for tc in final.tool_calls:
                    print(f"   • {tc['name']}: {tc['args']}")
            
            # Hiển thị response chính (safe extraction)
            content = get_message_content(final)
            if content:
                print(f"\n🤖 TravelBuddy: {content}")
            
            conversation_history.append({
                "user": user_input,
                "assistant": content
            })
            
        except KeyboardInterrupt:
            print("\n\n👋 Tạm biệt!")
            break
        except Exception as e:
            print(f"\n❌ Lỗi không mong muốn: {str(e)}")
            print("   Vui lòng thử lại.")