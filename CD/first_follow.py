EPS = 'ε'

def first(CFG):
    FIRST = {nt: set() for nt in CFG}

    def f(x):
        if x not in CFG:
            return {x}
        res = set()
        for prod in CFG[x]:
            if not prod:
                res.add(EPS)
            else:
                for s in prod:
                    r = f(s)
                    res |= (r - {EPS})
                    if EPS not in r:
                        break
                else:
                    res.add(EPS)
        return res

    for nt in CFG:
        FIRST[nt] = f(nt)
    return FIRST


def follow(CFG, FIRST, start):
    FOLLOW = {nt: set() for nt in CFG}
    FOLLOW[start].add('$')

    for _ in range(5):
        for A in CFG:
            for prod in CFG[A]:
                for i, B in enumerate(prod):
                    if B in CFG:
                        beta = prod[i+1:]
                        if beta:
                            fb = set()
                            for s in beta:
                                r = FIRST[s] if s in FIRST else {s}
                                fb |= (r - {EPS})
                                if EPS not in r:
                                    break
                            FOLLOW[B] |= fb
                        else:
                            FOLLOW[B] |= FOLLOW[A]
    return FOLLOW

