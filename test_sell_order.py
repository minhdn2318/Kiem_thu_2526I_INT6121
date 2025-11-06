import pytest
from order import place_sell_order

# ==============================
# Test cho hàm place_sell_order()
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
])
def test_place_sell_order(symbol, price, volume, expected):
    """Kiểm thử các trường hợp ĐẶT LỆNH BÁN"""
    result = place_sell_order(symbol, price, volume)
    assert result["status"] == expected["status"]
    if result["status"] == "error":
        assert result["msg"] == expected["msg"]
