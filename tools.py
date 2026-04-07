from langchain_core.tools import tool

# ========================================================================
# MOCK DATA - Dữ liệu giả lập hệ thống du lịch
# Lưu ý: Giá cả có logic (VD: cuối tuần đắt hơn, hạng cao hơn đắt hơn)
# Sinh viên cần đọc hiểu data để debug test cases.
# ========================================================================

FLIGHTS_DB = {
    ("Hà Nội", "Đà Nẵng"): [
        {"airline": "Vietnam Airlines", "departure": "06:00", "arrival": "07:20", "price": 1_450_000, "class": "economy"},
        {"airline": "Vietnam Airlines", "departure": "14:00", "arrival": "15:20", "price": 2_800_000, "class": "business"},
        {"airline": "VietJet Air", "departure": "08:30", "arrival": "09:50", "price": 890_000, "class": "economy"},
        {"airline": "Bamboo Airways", "departure": "11:00", "arrival": "12:20", "price": 1_200_000, "class": "economy"},
    ],
    ("Hà Nội", "Phú Quốc"): [
        {"airline": "Vietnam Airlines", "departure": "07:00", "arrival": "09:15", "price": 2_100_000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "10:00", "arrival": "12:15", "price": 1_350_000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "16:00", "arrival": "18:15", "price": 1_100_000, "class": "economy"},
    ],
    ("Hà Nội", "Hồ Chí Minh"): [
        {"airline": "Vietnam Airlines", "departure": "06:00", "arrival": "08:10", "price": 1_600_000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "07:30", "arrival": "09:40", "price": 950_000, "class": "economy"},
        {"airline": "Bamboo Airways", "departure": "12:00", "arrival": "14:10", "price": 1_300_000, "class": "economy"},
        {"airline": "Vietnam Airlines", "departure": "18:00", "arrival": "20:10", "price": 3_200_000, "class": "business"},
    ],
    ("Hồ Chí Minh", "Đà Nẵng"): [
        {"airline": "Vietnam Airlines", "departure": "09:00", "arrival": "10:20", "price": 1_300_000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "13:00", "arrival": "14:20", "price": 780_000, "class": "economy"},
    ],
    ("Hồ Chí Minh", "Phú Quốc"): [
        {"airline": "Vietnam Airlines", "departure": "08:00", "arrival": "09:00", "price": 1_100_000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "15:00", "arrival": "16:00", "price": 650_000, "class": "economy"},
    ],
    # ===== TUYẾN THÊM MỚI =====
    ("Hà Nội", "Nha Trang"): [
        {"airline": "Vietnam Airlines", "departure": "05:30", "arrival": "07:10", "price": 1_650_000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "09:15", "arrival": "11:00", "price": 1_050_000, "class": "economy"},
        {"airline": "Bamboo Airways", "departure": "13:30", "arrival": "15:15", "price": 1_350_000, "class": "economy"},
    ],
    ("Hà Nội", "Hạ Long"): [
        {"airline": "Vietnam Airlines", "departure": "07:30", "arrival": "08:50", "price": 950_000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "10:45", "arrival": "12:05", "price": 750_000, "class": "economy"},
    ],
    ("Hồ Chí Minh", "Nha Trang"): [
        {"airline": "Vietnam Airlines", "departure": "08:30", "arrival": "09:50", "price": 1_200_000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "14:00", "arrival": "15:20", "price": 850_000, "class": "economy"},
        {"airline": "Bamboo Airways", "departure": "17:00", "arrival": "18:20", "price": 1_100_000, "class": "economy"},
    ],
    ("Hồ Chí Minh", "Hạ Long"): [
        {"airline": "Vietnam Airlines", "departure": "06:00", "arrival": "08:30", "price": 1_800_000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "11:30", "arrival": "14:00", "price": 1_400_000, "class": "economy"},
    ],
    ("Đà Nẵng", "Phú Quốc"): [
        {"airline": "VietJet Air", "departure": "10:30", "arrival": "12:15", "price": 950_000, "class": "economy"},
        {"airline": "Vietnam Airlines", "departure": "15:00", "arrival": "16:45", "price": 1_400_000, "class": "economy"},
    ],
    ("Đà Nẵng", "Nha Trang"): [
        {"airline": "VietJet Air", "departure": "12:00", "arrival": "13:30", "price": 680_000, "class": "economy"},
        {"airline": "Vietnam Airlines", "departure": "14:30", "arrival": "16:00", "price": 1_050_000, "class": "economy"},
    ],
    ("Nha Trang", "Phú Quốc"): [
        {"airline": "Vietnam Airlines", "departure": "09:00", "arrival": "10:15", "price": 1_250_000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "16:30", "arrival": "17:45", "price": 900_000, "class": "economy"},
    ],
    # ===== TUYẾN THÊM MỚI =====
    ("Hà Nội", "Cần Thơ"): [
        {"airline": "Vietnam Airlines", "departure": "06:30", "arrival": "09:30", "price": 1_850_000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "10:30", "arrival": "13:30", "price": 1_200_000, "class": "economy"},
        {"airline": "Bamboo Airways", "departure": "14:00", "arrival": "17:00", "price": 1_450_000, "class": "economy"},
    ],
    ("Hồ Chí Minh", "Cần Thơ"): [
        {"airline": "Vietnam Airlines", "departure": "08:00", "arrival": "10:00", "price": 1_100_000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "13:00", "arrival": "15:00", "price": 750_000, "class": "economy"},
    ],
    ("Hà Nội", "Quy Nhơn"): [
        {"airline": "Vietnam Airlines", "departure": "07:00", "arrival": "08:40", "price": 1_550_000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "11:30", "arrival": "13:10", "price": 1_000_000, "class": "economy"},
    ],
    ("Hồ Chí Minh", "Quy Nhơn"): [
        {"airline": "Vietnam Airlines", "departure": "09:30", "arrival": "11:10", "price": 1_250_000, "class": "economy"},
        {"airline": "Bamboo Airways", "departure": "15:00", "arrival": "16:40", "price": 1_050_000, "class": "economy"},
    ],
    ("Hà Nội", "Huế"): [
        {"airline": "Vietnam Airlines", "departure": "06:00", "arrival": "07:30", "price": 1_400_000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "10:00", "arrival": "11:30", "price": 900_000, "class": "economy"},
        {"airline": "Bamboo Airways", "departure": "13:30", "arrival": "15:00", "price": 1_250_000, "class": "economy"},
    ],
    ("Hồ Chí Minh", "Huế"): [
        {"airline": "Vietnam Airlines", "departure": "08:00", "arrival": "09:30", "price": 1_350_000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "14:30", "arrival": "16:00", "price": 950_000, "class": "economy"},
    ],
    ("Đà Nẵng", "Huế"): [
        {"airline": "VietJet Air", "departure": "11:00", "arrival": "12:00", "price": 480_000, "class": "economy"},
        {"airline": "Vietnam Airlines", "departure": "14:00", "arrival": "15:00", "price": 750_000, "class": "economy"},
    ],
    ("Quy Nhơn", "Nha Trang"): [
        {"airline": "VietJet Air", "departure": "10:30", "arrival": "11:50", "price": 580_000, "class": "economy"},
        {"airline": "Vietnam Airlines", "departure": "15:00", "arrival": "16:20", "price": 900_000, "class": "economy"},
    ],
    ("Cần Thơ", "Phú Quốc"): [
        {"airline": "Vietnam Airlines", "departure": "10:00", "arrival": "11:30", "price": 1_400_000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "16:00", "arrival": "17:30", "price": 1_100_000, "class": "economy"},
    ],
}

HOTELS_DB = {
    "Đà Nẵng": [
        {"name": "Mường Thanh Luxury", "stars": 5, "price_per_night": 1_800_000, "area": "Mỹ Khê", "rating": 4.5},
        {"name": "Sala Danang Beach", "stars": 4, "price_per_night": 1_200_000, "area": "Mỹ Khê", "rating": 4.3},
        {"name": "Fivitel Danang", "stars": 3, "price_per_night": 650_000, "area": "Sơn Trà", "rating": 4.1},
        {"name": "Memory Hostel", "stars": 2, "price_per_night": 250_000, "area": "Hải Châu", "rating": 4.6},
        {"name": "Christina's Homestay", "stars": 2, "price_per_night": 350_000, "area": "An Thượng", "rating": 4.7},
        {"name": "Merperle Danang", "stars": 4, "price_per_night": 1_500_000, "area": "Mỹ Khê", "rating": 4.4},
        {"name": "Danang Golden Bay", "stars": 3, "price_per_night": 580_000, "area": "Bãi Mỹ Khê", "rating": 4.0},
    ],
    "Phú Quốc": [
        {"name": "Vinpearl Resort", "stars": 5, "price_per_night": 3_500_000, "area": "Bãi Dài", "rating": 4.4},
        {"name": "Sol by Meliá", "stars": 4, "price_per_night": 1_500_000, "area": "Bãi Trường", "rating": 4.2},
        {"name": "Lahana Resort", "stars": 3, "price_per_night": 800_000, "area": "Dương Đông", "rating": 4.0},
        {"name": "9Station Hostel", "stars": 2, "price_per_night": 200_000, "area": "Dương Đông", "rating": 4.5},
        {"name": "Mango Bay Resort", "stars": 4, "price_per_night": 1_800_000, "area": "Bãi Dài", "rating": 4.6},
        {"name": "Tropicana Resort", "stars": 3, "price_per_night": 950_000, "area": "Dương Đông", "rating": 4.2},
    ],
    "Hồ Chí Minh": [
        {"name": "Rex Hotel", "stars": 5, "price_per_night": 2_800_000, "area": "Quận 1", "rating": 4.3},
        {"name": "Liberty Central", "stars": 4, "price_per_night": 1_400_000, "area": "Quận 1", "rating": 4.1},
        {"name": "Cochin Zen Hotel", "stars": 3, "price_per_night": 550_000, "area": "Quận 3", "rating": 4.4},
        {"name": "The Common Room", "stars": 2, "price_per_night": 180_000, "area": "Quận 1", "rating": 4.6},
        {"name": "Park Hyatt Saigon", "stars": 5, "price_per_night": 3_500_000, "area": "Quận 1", "rating": 4.7},
        {"name": "Majestic Hotel", "stars": 4, "price_per_night": 1_600_000, "area": "Quận 1", "rating": 4.2},
    ],
    # ===== KHÁCH SẠN THÊM MỚI =====
    "Nha Trang": [
        {"name": "Vinpearl Nha Trang", "stars": 5, "price_per_night": 2_500_000, "area": "Bãi Nha Trang", "rating": 4.6},
        {"name": "Ninh Vân Bay", "stars": 5, "price_per_night": 3_200_000, "area": "Vịnh Ninh Vân", "rating": 4.8},
        {"name": "La Veranda Resort", "stars": 4, "price_per_night": 1_700_000, "area": "Đảo Hòn Tre", "rating": 4.5},
        {"name": "Amiana Resort", "stars": 4, "price_per_night": 1_400_000, "area": "Tân Lập", "rating": 4.3},
        {"name": "Cititel Premier", "stars": 3, "price_per_night": 680_000, "area": "Tây Bắc", "rating": 4.1},
        {"name": "Nha Trang Backpacker Hostel", "stars": 2, "price_per_night": 220_000, "area": "Tây Bắc", "rating": 4.4},
        {"name": "Blue Moon Hotel", "stars": 3, "price_per_night": 580_000, "area": "Tây Bắc", "rating": 4.0},
    ],
    "Hạ Long": [
        {"name": "Starlight Cruise", "stars": 4, "price_per_night": 1_600_000, "area": "Vịnh Hạ Long", "rating": 4.7},
        {"name": "Heritage Line Cruises", "stars": 4, "price_per_night": 1_450_000, "area": "Vịnh Hạ Long", "rating": 4.6},
        {"name": "Sunworld Ha Long", "stars": 5, "price_per_night": 2_100_000, "area": "Vịnh Hạ Long", "rating": 4.5},
        {"name": "Hoang Long Plaza", "stars": 3, "price_per_night": 750_000, "area": "Thành phố Hạ Long", "rating": 4.2},
        {"name": "Dragon Legend Cruise", "stars": 4, "price_per_night": 1_550_000, "area": "Vịnh Hạ Long", "rating": 4.4},
        {"name": "Ha Long City Hotel", "stars": 2, "price_per_night": 350_000, "area": "Thành phố Hạ Long", "rating": 4.1},
    ],
    # ===== KHÁCH SẠN THÊM MỚI =====
    "Cần Thơ": [
        {"name": "Victoria Can Tho Resort", "stars": 5, "price_per_night": 2_200_000, "area": "Sông Hậu", "rating": 4.6},
        {"name": "Azerai Can Tho", "stars": 4, "price_per_night": 1_600_000, "area": "Sông Hậu", "rating": 4.7},
        {"name": "Saigon Can Tho Hotel", "stars": 4, "price_per_night": 1_200_000, "area": "Quận Ninh Kiều", "rating": 4.3},
        {"name": "Mekong Riverside Lodge", "stars": 3, "price_per_night": 720_000, "area": "Quận Ninh Kiều", "rating": 4.2},
        {"name": "Nha Rieng Hotel", "stars": 3, "price_per_night": 650_000, "area": "Quận Cái Răng", "rating": 4.0},
        {"name": "Can Tho Backpackers", "stars": 2, "price_per_night": 280_000, "area": "Quận Ninh Kiều", "rating": 4.5},
    ],
    "Quy Nhơn": [
        {"name": "Avani Quy Nhon Resort", "stars": 5, "price_per_night": 2_600_000, "area": "Đồi Dừa", "rating": 4.7},
        {"name": "Life Resort Quy Nhon", "stars": 4, "price_per_night": 1_450_000, "area": "Nhân Hòa", "rating": 4.5},
        {"name": "Sunrise Beach Resort", "stars": 4, "price_per_night": 1_350_000, "area": "Bãi Vũng Tàu", "rating": 4.4},
        {"name": "Quy Nhon Seaside Inn", "stars": 3, "price_per_night": 750_000, "area": "Thành phố Quy Nhơn", "rating": 4.1},
        {"name": "Nha Trang Resort Quy Nhon", "stars": 3, "price_per_night": 680_000, "area": "Nhân Hòa", "rating": 4.0},
        {"name": "Quy Nhon Beach Hostel", "stars": 2, "price_per_night": 250_000, "area": "Thành phố Quy Nhơn", "rating": 4.6},
    ],
    "Huế": [
        {"name": "Saigon Morin", "stars": 5, "price_per_night": 2_300_000, "area": "Thành phố Huế", "rating": 4.6},
        {"name": "La Residence Hue", "stars": 5, "price_per_night": 2_700_000, "area": "Sông Hương", "rating": 4.8},
        {"name": "Hue Serene Shining Hotel", "stars": 4, "price_per_night": 1_400_000, "area": "Thành phố Huế", "rating": 4.3},
        {"name": "MerPerle Hue", "stars": 4, "price_per_night": 1_550_000, "area": "Sông Hương", "rating": 4.4},
        {"name": "Cititel Hue", "stars": 3, "price_per_night": 700_000, "area": "Thành phố Huế", "rating": 4.1},
        {"name": "Hue Eco Hostel", "stars": 2, "price_per_night": 240_000, "area": "Thành phố Huế", "rating": 4.5},
    ],
}

@tool
def search_flights(origin: str, destination: str) -> str:
    """
    Tìm kiếm các chuyến bay giữa hai thành phố.
    Tham số:
    - origin: thành phố khởi hành (VD: 'Hà Nội', 'Hồ Chí Minh')
    - destination: thành phố đến (VD: 'Đà Nẵng', 'Phú Quốc')
    Trả về danh sách chuyến bay với hãng, giờ bay, giá vé.
    Nếu không tìm thấy tuyến bay, trả về thông báo không có chuyến.
    """
    # Chuẩn hóa tên thành phố (loại bỏ khoảng trắng thừa)
    origin = origin.strip()
    destination = destination.strip()

    # Tra cứu FLIGHTS_DB theo tuyến (origin -> destination)
    flights = None
    if (origin, destination) in FLIGHTS_DB:
        flights = FLIGHTS_DB[(origin, destination)]
    # Nếu không tìm được, thử tra ngược (destination -> origin)
    elif (destination, origin) in FLIGHTS_DB:
        flights = FLIGHTS_DB[(destination, origin)]

    # Xử lý trường hợp không tìm thấy chuyến bay
    if not flights:
        return f"❌ Không tìm thấy chuyến bay từ {origin} đến {destination}. Vui lòng thử các điểm đến khác hoặc kiểm tra lại tên thành phố."

    # Format danh sách chuyến bay dễ đọc
    result = f"✈️ **Các chuyến bay từ {origin} đến {destination}:**\n\n"

    for i, flight in enumerate(flights, 1):
        # Format giá tiền với dấu chấm phân cách (1.450.000đ)
        formatted_price = f"{flight['price']:,}đ".replace(",", ".")

        result += (
            f"{i}. **{flight['airline']}** ({flight['class'].upper()})\n"
            f"   ⏰ {flight['departure']} → {flight['arrival']}\n"
            f"   💰 {formatted_price}\n\n"
        )

    return result

@tool
def search_hotels(city: str, max_price_per_night: int = 99999999) -> str:
    """
    Tìm kiếm khách sạn tại một thành phố, có thể lọc theo giá tối đa mỗi đêm.
    Tham số:
    - city: tên thành phố (VD: 'Đà Nẵng', 'Phú Quốc', 'Hồ Chí Minh')
    - max_price_per_night: giá tối đa mỗi đêm (VNĐ), mặc định không giới hạn
    Trả về danh sách khách sạn phù hợp với tên, số sao, giá, khu vực, rating.
    """
    # Chuẩn hóa tên thành phố
    city = city.strip()

    # Tra cứu HOTELS_DB
    if city not in HOTELS_DB:
        return f"❌ Không tìm thấy khách sạn tại {city}. Thành phố này hiện chưa có dữ liệu. Vui lòng chọn một địa điểm khác."

    hotels = HOTELS_DB[city]

    # Lọc theo max_price_per_night
    filtered_hotels = [
        hotel for hotel in hotels
        if hotel['price_per_night'] <= max_price_per_night
    ]

    # Nếu không có kết quả phù hợp
    if not filtered_hotels:
        formatted_budget = f"{max_price_per_night:,}đ".replace(",", ".")
        return f"❌ Không tìm thấy khách sạn tại {city} với giá dưới {formatted_budget}/đêm. Hãy thử tăng ngân sách hoặc chọn khu vực khác."

    # Sắp xếp theo rating giảm dần (khách sạn tốt nhất lên trên)
    filtered_hotels.sort(key=lambda x: x['rating'], reverse=True)

    # Format danh sách khách sạn dễ đọc
    result = f"🏨 **Khách sạn tại {city} (sắp xếp theo đánh giá):**\n\n"

    for i, hotel in enumerate(filtered_hotels, 1):
        # Format giá tiền
        formatted_price = f"{hotel['price_per_night']:,}đ".replace(",", ".")

        # Hiển thị số sao
        stars = "⭐" * hotel['stars']

        result += (
            f"{i}. **{hotel['name']}** {stars}\n"
            f"   📍 {hotel['area']}\n"
            f"   💰 {formatted_price}/đêm\n"
            f"   ⭐ Đánh giá: {hotel['rating']}/5\n\n"
        )

    return result

@tool
def calculate_budget(total_budget: int, expenses: str) -> str:
    """
        Tính toán ngân sách còn lại sau khi trừ các khoản chi phí.
        Tham số:
        - total_budget: tổng ngân sách ban đầu (VNĐ)
        - expenses: chuỗi mô tả các khoản chi, mỗi khoản cách nhau bởi dấu phẩy,
        - định dạng 'tên_khoản:số_tiền' (VD: 'vé_máy_bay:890000,khách_sạn:650000')
        Trả về bảng chi tiết các khoản chi và số tiền còn lại.
        Nếu vượt ngân sách, cảnh báo rõ ràng số tiền thiếu.
    """
    try:
        # Parse chuỗi expenses thành dict {tên: số_tiền}
        expense_items = expenses.split(",")  # Tách các khoản chi theo dấu phẩy

        expenses_dict = {}
        total_expense = 0

        for item in expense_items:
            item = item.strip()  # Loại bỏ khoảng trắng

            # Tách tên khoản và số tiền theo dấu ":"
            if ":" not in item:
                return f"❌ Lỗi định dạng: '{item}' không đúng. Vui lòng sử dụng định dạng 'tên_khoản:số_tiền'."

            parts = item.split(":")
            if len(parts) != 2:
                return f"❌ Lỗi định dạng: '{item}' không đúng. Mỗi khoản phải có tên và số tiền cách nhau bởi dấu ':'."

            expense_name = parts[0].strip()
            try:
                expense_amount = int(parts[1].strip())
                if expense_amount < 0:
                    return f"❌ Lỗi: Số tiền '{expense_amount}' không hợp lệ (phải >= 0)."
            except ValueError:
                return f"❌ Lỗi: Không thể chuyển đổi '{parts[1]}' thành số tiền."

            expenses_dict[expense_name] = expense_amount
            total_expense += expense_amount

        # Tính số tiền còn lại
        remaining_budget = total_budget - total_expense

        # Format bảng chi tiết với dấu chấm phân cách
        result = "💰 **BÁO CÁO NGÂN SÁCH CHI TIẾT:**\n\n"
        result += "**Bảng chi phí:**\n"

        for name, amount in expenses_dict.items():
            formatted_amount = f"{amount:,}đ".replace(",", ".")
            result += f"  • {name}: {formatted_amount}\n"

        result += "\n" + "-" * 40 + "\n"

        # Format tổng chi phí
        formatted_total_expense = f"{total_expense:,}đ".replace(",", ".")
        formatted_total_budget = f"{total_budget:,}đ".replace(",", ".")

        result += f"**Tổng chi:** {formatted_total_expense}\n"
        result += f"**Ngân sách:** {formatted_total_budget}\n"

        # Hiển thị số tiền còn lại hoặc cảnh báo vượt ngân sách
        if remaining_budget >= 0:
            formatted_remaining = f"{remaining_budget:,}đ".replace(",", ".")
            result += f"**Còn lại:** {formatted_remaining} ✅\n"
        else:
            # Nếu âm -> cảnh báo rõ ràng
            shortage = abs(remaining_budget)
            formatted_shortage = f"{shortage:,}đ".replace(",", ".")
            result += f"\n⚠️ **VẬT NGÂN SÁCH {formatted_shortage}!** 🚨\n"
            result += f"Cần điều chỉnh kế hoạch hoặc tăng ngân sách.\n"

        return result

    except Exception as e:
        return f"❌ Lỗi không mong muốn: {str(e)}"
    
    