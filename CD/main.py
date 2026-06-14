from tokenization import tokenize
from cfg import CFG
from first_follow import first, follow
from parser import Parser

with open("input.txt") as f:
    code = f.read()

tokens = tokenize(code)

print("\n===== TOKENS =====")

# Header
print(f"{'TYPE':<12} | {'VALUE':<30}")
print("-" * 45)

# Rows
for t in tokens:
    token_type = t[0]
    token_value = str(t[1])

    print(f"{token_type:<12} | {token_value:<30}")

# mapping
mapped = []
for t in tokens:
    if t[0] == 'KEYWORD':
        mapped.append(t[1])
    elif t[0] == 'ID':
        mapped.append("ID")
    elif t[0] == 'NUMBER':
        mapped.append("NUMBER")
    elif t[0] == 'STRING':
        mapped.append("STRING")
    elif t[0] == 'COLON':
        mapped.append("COLON")
    elif t[0] == 'ASSIGN':
        mapped.append("ASSIGN_OP")   
    elif t[0] == 'SEMICOL':
        mapped.append("SEMICOL")
    elif t[0] == 'LPAREN':
        mapped.append("LPAREN")
    elif t[0] == 'RPAREN':
        mapped.append("RPAREN")
    elif t[0] == 'EQUAL':
        mapped.append("EQUAL")
    else:
        mapped.append(t[1])

print("\n===== CFG =====")
for k in CFG:
    for p in CFG[k]:
        print(k, "->", p if p else "ε")

FIRST = first(CFG)
FOLLOW = follow(CFG, FIRST, "PROGRAM")

print("\n===== FIRST =====")

print(f"{'NON-TERMINAL':<15} | {'FIRST SET'}")
print("-" * 40)

for k in FIRST:
    values = ", ".join(sorted(FIRST[k]))
    print(f"{k:<15} | {{ {values} }}")

print("\n===== FOLLOW =====")

print(f"{'NON-TERMINAL':<15} | {'FOLLOW SET'}")
print("-" * 40)

for k in FOLLOW:
    values = ", ".join(sorted(FOLLOW[k]))
    print(f"{k:<15} | {{ {values} }}")

# ----------------------------
# ✅ PRODUCTION NUMBERING (ADDED)
# ----------------------------
productions = []
prod_map = {}

count = 1
for head in CFG:
    for prod in CFG[head]:
        productions.append((head, prod))
        prod_map[(head, tuple(prod))] = count
        count += 1

from slr_table import build_slr_table

ACTION, GOTO, STATES = build_slr_table(CFG, FOLLOW)

print("\n===== SLR STATES =====")

for i, state in enumerate(STATES):
    print(f"\nState {i}:")
    for (lhs, rhs, dot) in state:
        rhs = list(rhs)
        rhs.insert(dot, "•")
        print(f"{lhs} -> {' '.join(rhs)}")

print("\n===== PARSING TABLE =====")

# Collect symbols
terminals = sorted(set(sym for (_, sym) in ACTION.keys()))
non_terminals = sorted(set(sym for (_, sym) in GOTO.keys()))

headers = ["State"] + terminals + non_terminals

# Build full table
states = sorted(set(s for (s, _) in ACTION.keys()) | set(s for (s, _) in GOTO.keys()))
table = []

for state in states:
    row = [str(state)]

    # ACTION columns
    for t in terminals:
        val = ACTION.get((state, t), "")
        if val:
            if val[0] == 'S':
                val = f"S{val[1]}"
            elif val[0] == 'R':
                # ✅ FIXED REDUCE FORMAT
                head, body = val[1]
                val = f"R{prod_map[(head, tuple(body))]}"
            elif val[0] == 'ACC':
                val = "ACC"
        row.append(val)

    # GOTO columns
    for nt in non_terminals:
        val = GOTO.get((state, nt), "")
        row.append(str(val) if val != "" else "")

    table.append(row)

# Compute column widths
col_widths = [max(len(str(row[i])) for row in [headers] + table) + 2 for i in range(len(headers))]

# Print header
for i in range(len(headers)):
    print(headers[i].center(col_widths[i]), end="|")
print()

# Print separator
for w in col_widths:
    print("-" * w, end="+")
print()

# Print rows
for row in table:
    for i in range(len(row)):
        print(str(row[i]).center(col_widths[i]), end="|")
    print()
    
mapped.append('$')
print("\n===== MAPPED INPUT =====")
print(mapped)

parser = Parser(mapped, ACTION, GOTO, prod_map)
parser.parse()