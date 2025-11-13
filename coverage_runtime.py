# coverage_runtime.py
from collections import defaultdict

# --- định nghĩa hàm theo dõi node ---
executed_nodes = set()
executed_edges = set()
current_path = []

def visit(node):
    current_path.append(node)
    executed_nodes.add(node)

def leave(node):
    current_path.pop()

def edge(src, dst):
    executed_edges.add((src, dst))

# --- hàm gốc có instrumented --- 
def place_buy_order(symbol, price, volume):
    visit("start")
    visit("def place_buy_order")
    visit("Expr")

    if not symbol or not isinstance(symbol, str):
        edge("Expr", "return")
        visit("return")
        leave("return")
        leave("Expr")
        leave("def place_buy_order")
        leave("start")
        return {"status": "error", "msg": "Mã cổ phiếu không hợp lệ"}
    edge("Expr", "if price <= 0")

    if price <= 0:
        edge("if price <= 0", "return")
        visit("return")
        leave("return")
        leave("def place_buy_order")
        leave("start")
        return {"status": "error", "msg": "Giá phải > 0"}
    edge("if price <= 0", "if volume <= 0")

    if volume <= 0:
        edge("if volume <= 0", "return")
        visit("return")
        leave("return")
        leave("def place_buy_order")
        leave("start")
        return {"status": "error", "msg": "Khối lượng phải > 0"}
    edge("if volume <= 0", "if price > 1000000")

    if price > 1_000_000:
        edge("if price > 1000000", "return")
        visit("return")
        leave("return")
        leave("def place_buy_order")
        leave("start")
        return {"status": "error", "msg": "Giá vượt giới hạn tối đa"}
    edge("if price > 1000000", "if volume > 1000000")

    if volume > 1_000_000:
        edge("if volume > 1000000", "return")
        visit("return")
        leave("return")
        leave("def place_buy_order")
        leave("start")
        return {"status": "error", "msg": "Khối lượng vượt giới hạn tối đa"}
    edge("if volume > 1000000", "return")

    visit("return")
    leave("return")
    leave("def place_buy_order")
    leave("start")
    return {"status": "success", "msg": f"Đặt lệnh MUA thành công: {volume} CP {symbol} giá {price}"}

# --- tương tự instrument place_sell_order --- 
# ...

# --- danh sách test input ---
tests = [
    ("VCB", 100, 10),       # lệnh hợp lệ
    ("", 100, 10),          # symbol rỗng → lỗi
    ("VNM", -50, 5),        # price <= 0 → lỗi
    ("FPT", 100, -1),       # volume <= 0 → lỗi
    ("HPG", 2_000_000, 10)  # price vượt giới hạn → lỗi
]


# chạy test và theo dõi coverage
for symbol, price, volume in tests:
    place_buy_order(symbol, price, volume)

# tính coverage
all_nodes = {"start", "def place_buy_order", "Expr", "if not symbol or not isinstance(symbol, str)",
             "if price <= 0", "if volume <= 0", "if price > 1000000", "if volume > 1000000", "return"}
all_edges = {("Expr", "if not symbol or not isinstance(symbol, str)"),
             ("Expr", "if price <= 0"),
             ("if not symbol or not isinstance(symbol, str)", "return"),
             ("if price <= 0", "return"),
             ("if volume <= 0", "return"),
             ("if price > 1000000", "return"),
             ("if volume > 1000000", "return"),
             ("if price <= 0", "if volume <= 0"),
             ("if price > 1000000", "if volume > 1000000")}

statement_coverage = len(executed_nodes)/len(all_nodes)*100
branch_coverage = len(executed_edges)/len(all_edges)*100

print(f"Statement coverage: {statement_coverage:.2f}%")
print(f"Branch coverage: {branch_coverage:.2f}%")
