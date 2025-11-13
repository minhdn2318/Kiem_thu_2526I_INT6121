# dfs_from_dot.py
from collections import defaultdict

dot_file = "order_mini.dot"
output_file = "test_paths.txt"  # file lưu kết quả

nodes = set()
edges = []

# đọc DOT file
with open(dot_file, encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if "->" in line:
            parts = line.replace(";", "").split("->")
            src = parts[0].strip().strip('"')
            dst = parts[1].strip().strip('"')
            nodes.add(src)
            nodes.add(dst)
            edges.append((src, dst))
        elif line.endswith(";") and "->" not in line and line != "digraph CFG {":
            n = line.replace(";", "").strip().strip('"')
            nodes.add(n)

# tạo adjacency dict
graph = defaultdict(list)
for src, dst in edges:
    graph[src].append(dst)

# DFS liệt kê tất cả path từ start -> return
all_paths = []

def dfs(node, path):
    path.append(node)
    if node == "return":
        all_paths.append(list(path))
    else:
        for child in graph.get(node, []):
            dfs(child, path)
    path.pop()

dfs("start", [])

# lưu kết quả ra file
with open(output_file, "w", encoding="utf-8") as f:
    for i, path in enumerate(all_paths, 1):
        f.write(f"Path {i}: {' -> '.join(path)}\n")

print(f"Đã lưu {len(all_paths)} path vào file {output_file}")
