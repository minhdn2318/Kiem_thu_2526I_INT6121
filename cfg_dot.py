# mini_cfg_dot.py
import ast

class Node:
    def __init__(self, name):
        self.name = name
        self.children = []

nodes = []
edges = []

def new_node(name):
    n = Node(name)
    nodes.append(n)
    return n

# Parse code order.py
with open("order.py", encoding="utf-8") as f:
    tree = ast.parse(f.read())

start = new_node("start")
last_nodes = [start]

def parse_stmt(stmt, prev_nodes):
    if isinstance(stmt, ast.If):
        cond = ast.unparse(stmt.test)
        n = new_node(f"if {cond}")
        for pn in prev_nodes:
            edges.append((pn.name, n.name))
        body_last = parse_block(stmt.body, [n])
        orelse_last = parse_block(stmt.orelse, [n])
        return body_last + orelse_last
    elif isinstance(stmt, ast.Return):
        n = new_node("return")
        for pn in prev_nodes:
            edges.append((pn.name, n.name))
        return [n]
    else:
        n = new_node(type(stmt).__name__)
        for pn in prev_nodes:
            edges.append((pn.name, n.name))
        return [n]

def parse_block(stmts, prev_nodes):
    last = prev_nodes
    for s in stmts:
        last = parse_stmt(s, last)
    return last

# parse each function in module
for node in tree.body:
    if isinstance(node, ast.FunctionDef):
        func_node = new_node(f"def {node.name}")
        for ln in last_nodes:
            edges.append((ln.name, func_node.name))
        last_nodes = parse_block(node.body, [func_node])

# Xuất DOT
dot_file = "order_mini.dot"
with open(dot_file, "w") as f:
    f.write("digraph CFG {\n")
    for n in nodes:
        f.write(f'  "{n.name}";\n')
    for e in edges:
        f.write(f'  "{e[0]}" -> "{e[1]}";\n')
    f.write("}\n")

print(f"Đã xuất DOT: {dot_file}")
