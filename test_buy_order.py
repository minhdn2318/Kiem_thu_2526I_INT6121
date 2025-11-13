# test_buy_order.py
import pytest
from order import place_buy_order

# ==============================
# Test cho hàm place_buy_order()
# ==============================

@pytest.mark.parametrize("symbol, price, volume, expected", [
    # --- EP: Valid Partition ---
    ("FPT", 95000, 10, {"status": "success"}),

    # --- EP: Invalid Partition ---
    ("", 95000, 10, {"status": "error", "msg": "Mã cổ phiếu không hợp lệ"}),
    ("FPT", -95000, 10, {"status": "error", "msg": "Giá phải > 0"}),
    ("FPT", 95000, 0, {"status": "error", "msg": "Khối lượng phải > 0"}),

    # --- BVA: Boundary Test ---
    ("FPT", 1, 1, {"status": "success"}),
    ("FPT", 1_000_000, 1_000_000, {"status": "success"}),
    ("FPT", 0, 100, {"status": "error", "msg": "Giá phải > 0"}),
    ("FPT", 50000, -1, {"status": "error", "msg": "Khối lượng phải > 0"}),
    ("FPT", 1_000_001, 10, {"status": "error", "msg": "Giá vượt giới hạn tối đa"}),
    ("FPT", 10, 1_000_001, {"status": "error", "msg": "Khối lượng vượt giới hạn tối đa"}),
])
def test_place_buy_order(symbol, price, volume, expected):
    """Kiểm thử các trường hợp ĐẶT LỆNH MUA"""
    result = place_buy_order(symbol, price, volume)
    assert result["status"] == expected["status"]
    if result["status"] == "error":
        assert result["msg"] == expected["msg"]
