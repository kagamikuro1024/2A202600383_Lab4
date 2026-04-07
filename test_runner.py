#!/usr/bin/env python
# ========================================================================
# TEST RUNNER - Chạy agent với 5 test cases và ghi kết quả
# ========================================================================

import sys
import time
from io import StringIO
from datetime import datetime
from agent import graph
from test_scenarios import TEST_CASES

def run_test_case(test: dict) -> dict:
    """
    Chạy 1 test case với agent và capture output
    
    Args:
        test: dict chứa test_id, user_input, expected_behavior, etc.
    
    Returns:
        dict chứa kết quả test
    """
    result = {
        "test_id": test["test_id"],
        "name": test["name"],
        "user_input": test["user_input"],
        "timestamp": datetime.now().isoformat(),
        "tools_called": [],
        "response": "",
        "error": None
    }
    
    # Redirect stdout để capture output
    old_stdout = sys.stdout
    sys.stdout = captured_output = StringIO()
    
    try:
        print(f"\n{'='*60}")
        print(f"🧪 {test['test_id']} - {test['name']}")
        print(f"{'='*60}")
        print(f"📝 User: {test['user_input']}\n")
        print("⏳ Agent đang suy nghĩ...\n")
        
        # Invoke agent
        start_time = time.time()
        agent_result = graph.invoke(
            {"messages": [("human", test["user_input"])]},
            config={"configurable": {"thread_id": "test"}}
        )
        elapsed_time = time.time() - start_time
        
        # Extract tools called từ messages
        tools_logged = []
        for msg in agent_result["messages"]:
            if hasattr(msg, 'tool_calls') and msg.tool_calls:
                for tc in msg.tool_calls:
                    tools_logged.append(tc['name'])
                    print(f"  ↳ Gọi tool: {tc['name']}({tc['args']})")
        
        # Extract final response
        final_msg = agent_result["messages"][-1]
        if hasattr(final_msg, 'content'):
            response_text = final_msg.content
        else:
            response_text = str(final_msg)
        
        print(f"\n🤖 Agent: {response_text}")
        print(f"\n⏱️  Thời gian: {elapsed_time:.2f}s")
        
        # Save results
        result["tools_called"] = tools_logged
        result["response"] = response_text
        result["duration"] = elapsed_time
        
    except Exception as e:
        result["error"] = str(e)
        print(f"\n❌ LỖI: {str(e)}")
    
    finally:
        # Restore stdout
        sys.stdout = old_stdout
        captured = captured_output.getvalue()
    
    return {
        **result,
        "captured_output": captured
    }

def generate_test_results_md(results: list) -> str:
    """Generate test_results.md"""
    md = "# 📊 Test Results\n\n"
    md += f"**Thời gian chạy:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    md += f"**Tổng số tests:** {len(results)}\n\n"
    
    for result in results:
        md += f"## {result['test_id']} - {result['name']}\n\n"
        md += f"**User Input:**\n```\n{result['user_input']}\n```\n\n"
        md += f"**Tools Called:** {result['tools_called'] if result['tools_called'] else '❌ Không có'}\n\n"
        md += f"**Agent Response:**\n```\n{result['response']}\n```\n\n"
        md += f"⏱️ **Duration:** {result.get('duration', 'N/A')}s\n\n"
        
        if result['error']:
            md += f"**❌ Error:** {result['error']}\n\n"
        
        md += "---\n\n"
    
    return md

def generate_report_md(results: list) -> str:
    """Generate report_agent.md với so sánh expected vs actual"""
    md = "# 📋 Agent Evaluation Report\n\n"
    md += f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    
    # Summary
    passed = 0
    failed = 0
    
    for result in results:
        test_case = next((t for t in TEST_CASES if t['test_id'] == result['test_id']), None)
        if not test_case:
            continue
        
        # Check if tools match expected
        expected_tools = set(test_case['expected_tools'])
        actual_tools = set(result['tools_called'])
        tools_match = expected_tools == actual_tools
        
        if tools_match and not result['error']:
            passed += 1
        else:
            failed += 1
    
    md += f"## Summary\n\n"
    md += f"✅ **Passed:** {passed}/{len(results)}\n"
    md += f"❌ **Failed:** {failed}/{len(results)}\n"
    md += f"📈 **Pass Rate:** {passed/len(results)*100:.1f}%\n\n"
    
    # Detailed results
    md += f"## Detailed Results\n\n"
    
    for result in results:
        test_case = next((t for t in TEST_CASES if t['test_id'] == result['test_id']), None)
        if not test_case:
            continue
        
        expected_tools = set(test_case['expected_tools'])
        actual_tools = set(result['tools_called'])
        tools_match = expected_tools == actual_tools
        
        md += f"### {result['test_id']} - {result['name']}\n\n"
        md += f"**Expected Behavior:**\n```\n{test_case['expected_behavior']}\n```\n\n"
        
        md += f"**Expected Tools:** {test_case['expected_tools'] if test_case['expected_tools'] else 'Không có'}\n"
        md += f"**Actual Tools:** {result['tools_called'] if result['tools_called'] else 'Không có'}\n"
        md += f"**Match:** {'✅ YES' if tools_match else '❌ NO'}\n\n"
        
        md += f"**Success Criteria:**\n"
        for criterion in test_case['success_criteria']:
            # Simplified check - user sẽ review manually
            md += f"- [ ] {criterion}\n"
        md += "\n"
        
        md += f"**Agent Response Preview:**\n```\n{result['response'][:300]}...\n```\n\n"
        
        if result['error']:
            md += f"**⚠️ Error:** {result['error']}\n\n"
        
        md += "---\n\n"
    
    # Recommendations
    md += f"## 💡 Recommendations\n\n"
    md += "1. **Test 1 (Direct Answer):** Review if agent asks clarifying questions instead of calling tools\n"
    md += "2. **Test 2 (Single Tool):** Verify all 4 flights are listed correctly\n"
    md += "3. **Test 3 (Multi-Step):** Check tool chaining order and hotel list format\n"
    md += "4. **Test 4 (Clarification):** Ensure agent asks for missing info gracefully\n"
    md += "5. **Test 5 (Guardrail):** Verify agent refuses non-travel requests politely\n\n"
    
    return md

if __name__ == "__main__":
    print("\n" + "="*60)
    print("🚀 STARTING TEST SUITE - 5 Test Cases")
    print("="*60 + "\n")
    
    # Run all tests
    results = []
    for test in TEST_CASES:
        result = run_test_case(test)
        results.append(result)
        time.sleep(1)  # Wait between tests to avoid rate limiting
    
    # Generate reports
    test_results_md = generate_test_results_md(results)
    report_md = generate_report_md(results)
    
    # Save to files
    with open("test_results.md", "w", encoding="utf-8") as f:
        f.write(test_results_md)
    
    with open("report_agent.md", "w", encoding="utf-8") as f:
        f.write(report_md)
    
    print("\n" + "="*60)
    print("✅ TEST SUITE COMPLETED")
    print("="*60)
    print("\n📁 Results saved to:")
    print("   • test_results.md - Detailed test outputs")
    print("   • report_agent.md - Evaluation report with comparison\n")
