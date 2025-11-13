import csv
from z3 import *
from collections import defaultdict

# --- Cấu hình ---
DOT_FILE = "order_mini.dot"
CSV_FILE = "testcases_vn.csv"
VN_SYMBOLS = ["FPT", "VCB", "VNM", "VIC"]

# --- Parse DOT để tạo adjacency list ---
adj = defaultdict(list)
nodes = set()
with open(DOT_FILE, "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if "->" in line:
            parts = line.strip(";").split("->")
            src = parts[0].strip().strip('"')
            dst = parts[1].strip().strip('"')
            adj[src].append(dst)
            nodes.update([src, dst])
        elif line.startswith('"') and "->" not in line:
            node = line.strip(";").strip('"')
            nodes.add(node)

# --- DFS để liệt kê tất cả path từ 'start' đến 'return' ---
all_paths = []

def dfs(path, node):
    path.append(node)
    if node == "return":
        all_paths.append(list(path))
    else:
        for neigh in adj.get(node, []):
            dfs(path, neigh)
    path.pop()

dfs([], "start")
print(f"Found {len(all_paths)} paths from DOT.")

# --- Hàm xác định nhánh True/False ---
def add_path_constraints(solver, path, symbol, price, volume):
    for i, node in enumerate(path):
        # tìm node kế tiếp để biết nhánh đi tiếp là True hay False
        next_node = path[i+1] if i+1 < len(path) else None

        if "if not symbol" in node:
            if next_node and "return" in next_node:
                # đi vào return: điều kiện True
                solver.add(Or(symbol == "", Not(Or([symbol == sym for sym in VN_SYMBOLS]))))
            else:
                # đi nhánh khác: điều kiện False
                solver.add(And(symbol != "", Or([symbol == sym for sym in VN_SYMBOLS])))

        elif "if price <= 0" in node:
            if next_node and "return" in next_node:
                solver.add(price <= 0)
            else:
                solver.add(price > 0)

        elif "if price > 1000000" in node:
            if next_node and "return" in next_node:
                solver.add(price > 1_000_000)
            else:
                solver.add(price <= 1_000_000)

        elif "if volume <= 0" in node:
            if next_node and "return" in next_node:
                solver.add(volume <= 0)
            else:
                solver.add(volume > 0)

        elif "if volume > 1000000" in node:
            if next_node and "return" in next_node:
                solver.add(volume > 1_000_000)
            else:
                solver.add(volume <= 1_000_000)

# --- Sinh input bằng Z3 cho từng path ---
generated_tests = []

for idx, path in enumerate(all_paths):
    s = Solver()
    symbol = String("symbol")
    price = Int("price")
    volume = Int("volume")

    # Domain constraints
    s.add(Or([symbol == sym for sym in VN_SYMBOLS]))
    s.add(price >= 0, price <= 2_000_000)
    s.add(volume >= 0, volume <= 2_000_000)

    # Path-specific constraints
    add_path_constraints(s, path, symbol, price, volume)

    if s.check() == sat:
        m = s.model()
        testcase = {
            "symbol": m[symbol].as_string(),
            "price": m[price].as_long(),
            "volume": m[volume].as_long(),
            "path_idx": idx,
            "path": " -> ".join(path)
        }
    else:
        # fallback nếu không giải được
        testcase = {
            "symbol": "FPT",
            "price": 100,
            "volume": 10,
            "path_idx": idx,
            "path": " -> ".join(path)
        }

    generated_tests.append(testcase)

# --- Xuất CSV ---
with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["path_idx", "path", "symbol", "price", "volume"])
    writer.writeheader()
    for t in generated_tests:
        writer.writerow(t)

print(f"{len(generated_tests)} testcases đã được sinh và lưu vào {CSV_FILE}")
