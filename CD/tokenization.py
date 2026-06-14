import re

TOKEN_SPEC = [
    ('NUMBER', r'\d+'),
    ('STRING', r'"[^"]*"'),
    ('ASSIGN', r':='),
    ('COLON', r':'),
    ('SEMICOL', r';'),
    ('LPAREN', r'\('),
    ('RPAREN', r'\)'),
    ('EQUAL', r'='),
    ('KEYWORD', r'\b(if|then|elseif|else|end|procedure|printf|and|integer)\b'),
    ('ID', r'[A-Za-z_][A-Za-z0-9_]*'),
    ('SKIP', r'[ \n\t]+'),
]

tok_regex = '|'.join(f'(?P<{n}>{p})' for n, p in TOKEN_SPEC)

def tokenize(code):
    tokens = []
    for m in re.finditer(tok_regex, code, re.IGNORECASE):
        kind = m.lastgroup
        value = m.group()

        if kind == 'KEYWORD':
            tokens.append(('KEYWORD', value.lower()))
        elif kind == 'NUMBER':
            tokens.append(('NUMBER', value))
        elif kind == 'STRING':
            tokens.append(('STRING', value))
        elif kind != 'SKIP':
            tokens.append((kind, value))
    return tokens



