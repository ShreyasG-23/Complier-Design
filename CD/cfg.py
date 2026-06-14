CFG = {
    "PROGRAM": [["DECL", "PROC"]],
    
    "DECL": [["ID", "COLON", "integer", "SEMICOL"]],
    
    "PROC": [["procedure", "ID", "LPAREN", "PARAM", "RPAREN",
              "BODY", "end", "ID"]],
    
    "PARAM": [["ID", "COLON", "integer"]],
    
    "BODY": [["ASSIGN", "IFSTMT"]],
    
    "ASSIGN": [['ID', 'ASSIGN_OP', 'NUMBER', 'SEMICOL']],
    
    "IFSTMT": [["if", "COND", "then", "PRINTF",
                "ELSEIF", "ELSE", "end", "if", "SEMICOL"]],
    
    "ELSEIF": [["elseif", "COND", "then", "PRINTF"], []],
    
    "ELSE": [["else", "PRINTF"], []],
    
    "COND": [["ID", "EQUAL", "NUMBER", "and", "ID", "EQUAL", "NUMBER"]],
    
    "PRINTF": [["printf", "LPAREN", "STRING", "RPAREN", "SEMICOL"]],
}

