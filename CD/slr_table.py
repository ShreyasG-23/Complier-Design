from collections import defaultdict

def closure(items, CFG):
    closure_set = set(items)

    while True:
        new_items = set()

        for (lhs, rhs, dot) in closure_set:
            if dot < len(rhs):
                B = rhs[dot]
                if B in CFG:
                    for prod in CFG[B]:
                        new_items.add((B, tuple(prod), 0))

        if new_items.issubset(closure_set):
            break

        closure_set |= new_items

    return closure_set


def goto(items, symbol, CFG):
    moved = set()

    for (lhs, rhs, dot) in items:
        if dot < len(rhs) and rhs[dot] == symbol:
            moved.add((lhs, rhs, dot+1))

    return closure(moved, CFG)


def items(CFG):
    start = list(CFG.keys())[0]
    I0 = closure({("S'", tuple([start]), 0)}, CFG)

    C = [I0]

    while True:
        new_sets = []

        for I in C:
            symbols = set()
            for (lhs, rhs, dot) in I:
                if dot < len(rhs):
                    symbols.add(rhs[dot])

            for X in symbols:
                g = goto(I, X, CFG)
                if g and g not in C and g not in new_sets:
                    new_sets.append(g)

        if not new_sets:
            break

        C.extend(new_sets)

    return C


def build_slr_table(CFG, FOLLOW):
    C = items(CFG)

    ACTION = {}
    GOTO = {}

    # find terminals
    terminals = set()
    for head in CFG:
        for prod in CFG[head]:
            for sym in prod:
                if sym not in CFG:
                    terminals.add(sym)

    for i, I in enumerate(C):
        for (lhs, rhs, dot) in I:

            # SHIFT or GOTO
            if dot < len(rhs):
                a = rhs[dot]
                j = goto(I, a, CFG)

                if j in C:
                    if a in terminals:
                        ACTION[(i, a)] = ('S', C.index(j))
                    else:
                        GOTO[(i, a)] = C.index(j)

            # REDUCE / ACCEPT
            else:
                if lhs == "S'":
                    ACTION[(i, '$')] = ('ACC', None)
                else:
                    for a in FOLLOW[lhs]:
                        if (i, a) not in ACTION:
                            ACTION[(i, a)] = ('R', (lhs, list(rhs)))

    return ACTION, GOTO, C

