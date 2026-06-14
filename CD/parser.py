class Parser:
    def __init__(self, tokens, ACTION, GOTO, prod_map):
        self.tokens = tokens 
        self.ACTION = ACTION
        self.GOTO = GOTO
        self.prod_map = prod_map
        self.stack = [0]
        self.index = 0

    def parse(self):
        print("\n===== PARSING TRACE =====")

        rows = []
        step = 1   # 🔥 STEP COUNTER (STATE)

        while True:
            state = self.stack[-1]

            if self.index >= len(self.tokens):
                rows.append([
                    str(step),
                    self.format_stack(),
                    "",
                    "ERROR"
                ])
                print("\nINVALID STRING")
                break

            token = self.tokens[self.index].strip()
            print(f"DEBUG → State: {state}, Token: '{token}'")

            action = self.ACTION.get((state, token))
            input_str = " ".join(self.tokens[self.index:])

            # ERROR
            if action is None:
                rows.append([
                    str(step),
                    self.format_stack(),
                    input_str,
                    "ERROR"
                ])
                print("\nINVALID STRING")
                break   

            # SHIFT
            if action[0] == 'S':
                rows.append([
                    str(step),
                    self.format_stack(),
                    input_str,
                    f"S{action[1]}"
                ])
                step += 1

                self.stack.append(token)
                self.stack.append(action[1])
                self.index += 1

            # REDUCE
            elif action[0] == 'R':
                head, body = action[1]
                rule_no = self.prod_map[(head, tuple(body))]

                rows.append([
                    str(step),
                    self.format_stack(),
                    input_str,
                    f"R{rule_no}"
                ])
                step += 1

                if body != []:
                    for _ in range(len(body) * 2):
                        self.stack.pop()

                state = self.stack[-1]
                self.stack.append(head)
                self.stack.append(self.GOTO[(state, head)])

            # ACCEPT
            elif action[0] == 'ACC':
                rows.append([
                    str(step),
                    self.format_stack(),
                    input_str,
                    "ACCEPT"
                ])
                print("\nVALID STRING")
                break

        # PRINT TABLE
        self.print_table(rows)

    # 🔹 stack formatter
    def format_stack(self):
        return "[" + " ".join(map(str, self.stack)) + "]"

    # 🔹 aligned table
    def print_table(self, rows):
        headers = ["STATE", "STACK", "INPUT", "ACTION"]

        MAX_STACK_WIDTH = 50
        MAX_INPUT_WIDTH = 60

        formatted_rows = []

        for row in rows:
            st, stack, inp, act = row

            if len(stack) > MAX_STACK_WIDTH:
                stack = "..." + stack[-(MAX_STACK_WIDTH - 3):]

            if len(inp) > MAX_INPUT_WIDTH:
                inp = inp[:MAX_INPUT_WIDTH - 3] + "..."

            formatted_rows.append([st, stack, inp, act])

        col_widths = [
            max(len(r[i]) for r in formatted_rows + [headers]) + 2
            for i in range(4)
        ]

        print()
        for i in range(4):
            print(headers[i].ljust(col_widths[i]), end="| ")
        print()

        for w in col_widths:
            print("-" * w, end="+-")
        print()

        for row in formatted_rows:
            for i in range(4):
                print(row[i].ljust(col_widths[i]), end="| ")
            print()

            