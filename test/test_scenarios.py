# ========================================================================
# TEST SCENARIOS - 5 kịch bản test cho Agent
# ========================================================================

TEST_CASES = [
    {
        "test_id": "Test 1",
        "name": "Direct Answer (Không cần tool)",
        "user_input": "Xin chào! Tôi đang muốn đi du lịch nhưng chưa biết đi đâu.",
        "expected_behavior": "Agent chào hỏi, hỏi thêm về sở thích/ngân sách/thời gian. Không gọi tool nào.",
        "expected_tools": [],
        "success_criteria": [
            "✓ Không gọi bất kỳ tool nào",
            "✓ Trả lời thân thiện, lịch sự",
            "✓ Hỏi thêm thông tin về sở thích/ngân sách/thời gian"
        ]
    },
    {
        "test_id": "Test 2",
        "name": "Single Tool Call",
        "user_input": "Tìm giúp tôi chuyến bay từ Hà Nội đi Đà Nẵng",
        "expected_behavior": "Gọi search_flights('Hà Nội', 'Đà Nẵng'), liệt kê 4 chuyến bay (Vietnam Airlines 06:00, Vietnam Airlines 14:00 business, VietJet 08:30, Bamboo 11:00)",
        "expected_tools": ["search_flights"],
        "success_criteria": [
            "✓ Gọi search_flights với origin='Hà Nội', destination='Đà Nẵng'",
            "✓ Liệt kê đúng 4 chuyến bay",
            "✓ Hiển thị hãng, giờ bay, giá vé",
            "✓ Không gọi tools khác"
        ]
    },
    {
        "test_id": "Test 3",
        "name": "Multi-Step Tool Chaining",
        "user_input": "Tôi ở Hà Nội, muốn đi Phú Quốc 2 đêm, budget 5 triệu. Tư vấn giúp!",
        "expected_behavior": "Chuỗi 3 tools: search_flights('Hà Nội','Phú Quốc') → calculate_budget(5M, vé rẻ nhất) → search_hotels('Phú Quốc', max_price còn lại). Liệt kê tất cả khách sạn phù hợp budget.",
        "expected_tools": ["search_flights", "calculate_budget", "search_hotels"],
        "success_criteria": [
            "✓ Gọi search_flights để tìm vé rẻ nhất (1.100.000đ)",
            "✓ Gọi calculate_budget để tính ngân sách khách sạn còn lại",
            "✓ Gọi search_hotels với max_price phù hợp",
            "✓ Liệt kê tất cả khách sạn trong tầm giá (sắp xếp theo rating)",
            "✓ Breakdown ngân sách rõ ràng"
        ]
    },
    {
        "test_id": "Test 4",
        "name": "Missing Info / Clarification",
        "user_input": "Tôi muốn đặt khách sạn",
        "expected_behavior": "Hỏi lại thành phố nào? Bao nhiêu đêm? Ngân sách bao nhiêu? Không gọi tool vội.",
        "expected_tools": [],
        "success_criteria": [
            "✓ Không gọi bất kỳ tool nào",
            "✓ Hỏi thêm thông tin thiết yếu: thành phố, số đêm, ngân sách",
            "✓ Giọng điệu khéo léo, không áp đặt"
        ]
    },
    {
        "test_id": "Test 5",
        "name": "Guardrail / Refusal",
        "user_input": "Giải giúp tôi bài tập lập trình Python về linked list",
        "expected_behavior": "Từ chối lịch sự, nói rằng chỉ hỗ trợ du lịch.",
        "expected_tools": [],
        "success_criteria": [
            "✓ Từ chối yêu cầu về lập trình",
            "✓ Giải thích: chỉ hỗ trợ du lịch",
            "✓ Khéo léo lái về du lịch (không máy móc)",
            "✓ Không gọi tool nào"
        ]
    }
]
