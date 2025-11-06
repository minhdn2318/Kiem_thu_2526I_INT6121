# order.py
def place_buy_order(symbol, price, volume):
    """Đặt lệnh MUA cổ phiếu"""
    if not symbol or not isinstance(symbol, str):
        return {"status": "error", "msg": "Mã cổ phiếu không hợp lệ"}
    if price <= 0:
        return {"status": "error", "msg": "Giá phải > 0"}
    if volume <= 0:
        return {"status": "error", "msg": "Khối lượng phải > 0"}

    # Giới hạn biên có thể mở rộng
    if price > 1_000_000:
        return {"status": "error", "msg": "Giá vượt giới hạn tối đa"}
    if volume > 1_000_000:
        return {"status": "error", "msg": "Khối lượng vượt giới hạn tối đa"}

    return {
        "status": "success",
        "msg": f"Đặt lệnh MUA thành công: {volume} CP {symbol} giá {price}"
    }


def place_sell_order(symbol, price, volume):
    """Đặt lệnh BÁN cổ phiếu"""
    if not symbol or not isinstance(symbol, str):
        return {"status": "error", "msg": "Mã cổ phiếu không hợp lệ"}
    if price <= 0:
        return {"status": "error", "msg": "Giá phải > 0"}
    if volume <= 0:
        return {"status": "error", "msg": "Khối lượng phải > 0"}

    # Giới hạn biên có thể mở rộng
    if price > 1_000_000:
        return {"status": "error", "msg": "Giá vượt giới hạn tối đa"}
    if volume > 1_000_000:
        return {"status": "error", "msg": "Khối lượng vượt giới hạn tối đa"}

    return {
        "status": "success",
        "msg": f"Đặt lệnh BÁN thành công: {volume} CP {symbol} giá {price}"
    }
