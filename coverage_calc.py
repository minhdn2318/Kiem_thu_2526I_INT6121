# coverage_calc.py
nodes = set()   # tập tất cả node từ CFG
edges = set()   # tập tất cả edge từ CFG
all_paths = []  # danh sách path

# Đọc test path từ file
with open("test_paths.txt", encoding="utf-8") as f:
    for line in f:
        if line.startswith("Path"):
            # Path 1: start -> def place_buy_order -> Expr -> return
            _, path_str = line.split(":", 1)
            path_nodes = [n.strip() for n in path_str.strip().split("->")]
            all_paths.append(path_nodes)

# Lấy nodes và edges từ tất cả path
for path in all_paths:
    nodes.update(path)
    for i in range(len(path)-1):
        edges.add((path[i], path[i+1]))

# Tính coverage
executed_nodes = set()
executed_edges = set()
for path in all_paths:
    executed_nodes.update(path)
    for i in range(len(path)-1):
        executed_edges.add((path[i], path[i+1]))

statement_coverage = len(executed_nodes)/len(nodes)*100
branch_coverage = len(executed_edges)/len(edges)*100
path_coverage = len(all_paths)/len(all_paths)*100  # tất cả path đã liệt kê

print(f"Statement coverage: {statement_coverage:.2f}%")
print(f"Branch coverage: {branch_coverage:.2f}%")
print(f"Path coverage: {path_coverage:.2f}%")
