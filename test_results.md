# 📊 Test Results

**Thời gian chạy:** 2026-04-07 15:19:23
**Tổng số tests:** 5

## Test 1 - Direct Answer (Không cần tool)

**User Input:**
```
Xin chào! Tôi đang muốn đi du lịch nhưng chưa biết đi đâu.
```

**Tools Called:** ❌ Không có

**Agent Response:**
```
Chào bạn! Thật tuyệt khi bạn muốn đi du lịch. Bạn có thể chia sẻ với mình một số sở thích của bạn không? Bạn thích biển, núi, hay khám phá văn hóa lịch sử? Hoặc nếu bạn đã có trong đầu một điểm đến nào đó, hãy cho mình biết để giúp bạn lên kế hoạch nhé!
```

⏱️ **Duration:** 1.6550681591033936s

---

## Test 2 - Single Tool Call

**User Input:**
```
Tìm giúp tôi chuyến bay từ Hà Nội đi Đà Nẵng
```

**Tools Called:** ['search_flights']

**Agent Response:**
```
✈️ **Các chuyến bay từ Hà Nội đến Đà Nẵng:**

1. **VietJet Air** (ECONOMY)  
   ⏰ 08:30 → 09:50  
   💰 890.000đ

2. **Bamboo Airways** (ECONOMY)  
   ⏰ 11:00 → 12:20  
   💰 1.200.000đ

3. **Vietnam Airlines** (ECONOMY)  
   ⏰ 06:00 → 07:20  
   💰 1.450.000đ

4. **Vietnam Airlines** (BUSINESS)  
   ⏰ 14:00 → 15:20  
   💰 2.800.000đ

Bạn có ngân sách cho chuyến đi này là bao nhiêu? Mình sẽ giúp bạn tính toán ngân sách còn lại sau khi đã trừ chi phí vé máy bay nhé!
```

⏱️ **Duration:** 7.03062891960144s

---

## Test 3 - Multi-Step Tool Chaining

**User Input:**
```
Tôi ở Hà Nội, muốn đi Phú Quốc 2 đêm, budget 5 triệu. Tư vấn giúp!
```

**Tools Called:** ['search_flights', 'calculate_budget', 'search_hotels']

**Agent Response:**
```
✈️ **Chuyến bay:** VietJet Air - 16:00 → 18:15 - 1.100.000đ

💰 **Ngân sách phân tích:**
   • Vé máy bay x1: 1.100.000đ
   • Ngân sách khách sạn (còn lại): 5.000.000đ - 1.100.000đ = 3.900.000đ
   • **Ngân sách/đêm tối đa:** 3.900.000đ ÷ 2 = 1.950.000đ

🏨 **Danh sách khách sạn phù hợp (sắp xếp theo rating):**
1. **Mango Bay Resort** - ⭐⭐⭐⭐ - 1.800.000đ/đêm (Rating: 4.6/5)
2. **Sol by Meliá** - ⭐⭐⭐⭐ - 1.500.000đ/đêm (Rating: 4.2/5)
3. **Tropicana Resort** - ⭐⭐⭐ - 950.000đ/đêm (Rating: 4.2/5)
4. **Lahana Resort** - ⭐⭐⭐ - 800.000đ/đêm (Rating: 4.0/5)
5. **9Station Hostel** - ⭐⭐ - 200.000đ/đêm (Rating: 4.5/5)

💡 **Gợi ý của TravelBuddy:** Phú Quốc nổi tiếng với các món hải sản tươi ngon và các bãi biển tuyệt đẹp. Hãy thử ghẹ xào bơ hoặc gỏi cá trích nhé!
```

⏱️ **Duration:** 9.416622638702393s

---

## Test 4 - Missing Info / Clarification

**User Input:**
```
Tôi muốn đặt khách sạn
```

**Tools Called:** ❌ Không có

**Agent Response:**
```
Bạn có thể cho tôi biết bạn định đến thành phố nào không? Đồng thời, nếu bạn có ngân sách cụ thể cho khách sạn, hãy cho tôi biết luôn nhé!
```

⏱️ **Duration:** 2.1409831047058105s

---

## Test 5 - Guardrail / Refusal

**User Input:**
```
Giải giúp tôi bài tập lập trình Python về linked list
```

**Tools Called:** ❌ Không có

**Agent Response:**
```
Mình rất vui vì bạn quan tâm đến lập trình, nhưng mình chuyên về du lịch và không thể giúp bạn giải bài tập lập trình. Nếu bạn có bất kỳ câu hỏi nào về việc lên kế hoạch cho chuyến đi hoặc tìm kiếm các dịch vụ du lịch, hãy cho mình biết nhé! 🌍✈️
```

⏱️ **Duration:** 2.002479076385498s

---

