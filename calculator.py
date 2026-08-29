"""Scientific calculator with a dark, clickable GUI.

Run:
    python3 calculator.py
"""

from __future__ import annotations

import ast
import math
import tkinter as tk
from tkinter import font as tkfont


class SafeEvaluator(ast.NodeVisitor):
    """Evaluate a math expression using only allowed operators and functions."""

    def __init__(self, angle_mode: str = "DEG", ans: float = 0.0):
        self.angle_mode = angle_mode
        self.ans = ans

    def _wrap_trig(self, func):
        def inner(x):
            angle = math.radians(x) if self.angle_mode == "DEG" else x
            return func(angle)

        return inner

    def _wrap_inv_trig(self, func):
        def inner(x):
            value = func(x)
            return math.degrees(value) if self.angle_mode == "DEG" else value

        return inner

    def _namespace(self):
        return {
            "sin": self._wrap_trig(math.sin),
            "cos": self._wrap_trig(math.cos),
            "tan": self._wrap_trig(math.tan),
            "asin": self._wrap_inv_trig(math.asin),
            "acos": self._wrap_inv_trig(math.acos),
            "atan": self._wrap_inv_trig(math.atan),
            "sinh": math.sinh,
            "cosh": math.cosh,
            "tanh": math.tanh,
            "asinh": math.asinh,
            "acosh": math.acosh,
            "atanh": math.atanh,
            "sqrt": math.sqrt,
            "cbrt": math.cbrt if hasattr(math, "cbrt") else (lambda x: math.copysign(abs(x) ** (1 / 3), x)),
            "log": math.log10,
            "ln": math.log,
            "log2": math.log2,
            "exp": math.exp,
            "pow10": lambda x: 10 ** x,
            "abs": abs,
            "floor": math.floor,
            "ceil": math.ceil,
            "round": round,
            "fact": self._whole(math.factorial),
            "factorial": self._whole(math.factorial),
            "comb": self._whole(math.comb),
            "perm": self._whole(math.perm),
            "gcd": self._whole(math.gcd),
            "lcm": self._whole(math.lcm),
            "pi": math.pi,
            "e": math.e,
            "tau": math.tau,
            "ans": self.ans,
        }

    @staticmethod
    def _whole(func):
        def inner(*args):
            ints = []
            for value in args:
                if abs(value - round(value)) > 1e-9:
                    raise ValueError("this function needs whole numbers")
                ints.append(int(round(value)))
            return func(*ints)

        return inner

    def evaluate(self, expression: str):
        expression = expression.strip().replace("^", "**")
        if not expression:
            raise ValueError("empty expression")
        tree = ast.parse(expression, mode="eval")
        return self.visit(tree.body)

    def visit_Expression(self, node):
        return self.visit(node.body)

    def visit_Constant(self, node):
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError("only numbers are allowed")

    def visit_UnaryOp(self, node):
        value = self.visit(node.operand)
        if isinstance(node.op, ast.UAdd):
            return +value
        if isinstance(node.op, ast.USub):
            return -value
        raise ValueError("operator not allowed")

    def visit_BinOp(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        ops = {
            ast.Add: lambda a, b: a + b,
            ast.Sub: lambda a, b: a - b,
            ast.Mult: lambda a, b: a * b,
            ast.Div: lambda a, b: a / b,
            ast.FloorDiv: lambda a, b: a // b,
            ast.Mod: lambda a, b: a % b,
            ast.Pow: lambda a, b: a ** b,
        }
        for op_type, func in ops.items():
            if isinstance(node.op, op_type):
                return func(left, right)
        raise ValueError("operator not allowed")

    def visit_Call(self, node):
        if not isinstance(node.func, ast.Name):
            raise ValueError("invalid function")
        name = node.func.id
        func = self._namespace().get(name)
        if func is None or not callable(func):
            raise ValueError(f"unknown function: {name}")
        args = [self.visit(arg) for arg in node.args]
        if node.keywords:
            raise ValueError("keyword arguments are not allowed")
        return func(*args)

    def visit_Name(self, node):
        value = self._namespace().get(node.id)
        if value is None or callable(value):
            raise ValueError(f"unknown name: {node.id}")
        return value

    def generic_visit(self, node):
        raise ValueError("that expression is not allowed")


def format_result(value) -> str:
    if isinstance(value, bool) or value is None:
        raise ValueError("invalid result")
    if isinstance(value, complex):
        raise ValueError("complex results are not supported")
    if isinstance(value, int) or (isinstance(value, float) and value.is_integer() and abs(value) < 1e15):
        return str(int(value))
    text = f"{value:.12g}"
    return text


# --- colors (light keycaps so labels stay readable on macOS Tk) ---
BG = "#1c2128"
PANEL = "#252b34"
DISPLAY = "#11161c"
NUM = "#eef1f5"
NUM_HOVER = "#d5dbe3"
NUM_FG = "#111827"
FN = "#c6efe8"
FN_HOVER = "#9fdfd4"
FN_FG = "#0b3d38"
OP = "#ffd89a"
OP_HOVER = "#f5c56d"
OP_FG = "#3f2a08"
EQ = "#ff8a3d"
EQ_HOVER = "#ff9f5c"
EQ_FG = "#1a0d00"
DANGER = "#ff7b87"
DANGER_HOVER = "#ff96a0"
DANGER_FG = "#3b0a10"
ACCENT = "#3ee0c2"
TEXT = "#f3f6fb"
MUTED = "#c5ced8"
LINE = "#6b7380"
KEY_EDGE = "#4b5563"
ACTIVE_FG = "#c2410c"


class HoverButton(tk.Label):
    """Raised keycap. Labels honor background color on macOS; Button often does not."""

    def __init__(self, master, hover, command=None, **kwargs):
        self._bg = kwargs.get("bg")
        self._hover = hover
        self._command = command
        kwargs.setdefault("fg", NUM_FG)
        kwargs.setdefault("relief", "raised")
        kwargs.setdefault("bd", 2)
        kwargs.setdefault("padx", 4)
        kwargs.setdefault("pady", 6)
        kwargs.setdefault("cursor", "hand2")
        kwargs.setdefault("highlightthickness", 1)
        kwargs.setdefault("highlightbackground", KEY_EDGE)
        super().__init__(master, **kwargs)
        self.bind("<Enter>", lambda _e: self.configure(bg=self._hover))
        self.bind("<Leave>", lambda _e: self.configure(bg=self._bg, relief="raised"))
        self.bind("<Button-1>", lambda _e: self.configure(relief="sunken"))
        self.bind("<ButtonRelease-1>", self._release)

    def _release(self, _event=None):
        self.configure(relief="raised", bg=self._hover)
        if self._command:
            self._command()


class CalculatorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Yash's Calculator")
        self.configure(bg=BG)
        self.minsize(860, 620)
        self.geometry("920x680")
        self.angle_mode = "DEG"
        self.second = False
        self.hyp = False
        self.ans = 0.0
        self.expression = ""
        self.just_evaluated = False
        self.history: list[tuple[str, str]] = []

        self._fonts()
        self._build()
        self._bind_keys()
        self._refresh_fn_labels()

    def _fonts(self):
        available = set(tkfont.families())
        for name in ("Lucida Grande", "Arial", "Helvetica", "Menlo"):
            if name in available:
                family = name
                break
        else:
            family = "TkDefaultFont"
        self.font_title = (family, 11, "bold")
        self.font_muted = (family, 9)
        self.font_expr = (family, 11)
        self.font_result = (family, 18, "bold")
        self.font_btn = (family, 10, "bold")
        self.font_small = (family, 9)

    def _build(self):
        shell = tk.Frame(self, bg=BG, padx=18, pady=16)
        shell.pack(fill="both", expand=True)
        shell.columnconfigure(0, weight=1, minsize=220)
        shell.columnconfigure(1, weight=4)
        shell.rowconfigure(0, weight=1)

        self._build_history(shell)
        self._build_main(shell)

    def _build_history(self, parent):
        card = tk.Frame(parent, bg=PANEL, highlightbackground=LINE, highlightthickness=1)
        card.grid(row=0, column=0, sticky="nsew", padx=(0, 14))
        card.rowconfigure(2, weight=1)
        card.columnconfigure(0, weight=1)

        tk.Label(card, text="History", bg=PANEL, fg=ACCENT, font=self.font_title, anchor="w").grid(
            row=0, column=0, sticky="ew", padx=16, pady=(16, 4)
        )
        tk.Label(
            card,
            text="Click a line to reuse it",
            bg=PANEL,
            fg=MUTED,
            font=self.font_small,
            anchor="w",
        ).grid(row=1, column=0, sticky="ew", padx=16, pady=(0, 8))

        self.history_list = tk.Listbox(
            card,
            bg=DISPLAY,
            fg=TEXT,
            selectbackground="#9fdfd4",
            selectforeground=NUM_FG,
            activestyle="none",
            highlightthickness=0,
            bd=0,
            font=self.font_small,
        )
        self.history_list.grid(row=2, column=0, sticky="nsew", padx=12, pady=(0, 8))
        self.history_list.bind("<<ListboxSelect>>", self._reuse_history)

        HoverButton(
            card,
            hover=DANGER_HOVER,
            text="Clear history",
            bg=DANGER,
            fg=DANGER_FG,
            font=self.font_small,
            command=self._clear_history,
        ).grid(row=3, column=0, sticky="ew", padx=12, pady=(0, 14))

    def _build_main(self, parent):
        main = tk.Frame(parent, bg=BG)
        main.grid(row=0, column=1, sticky="nsew")
        main.columnconfigure(0, weight=1)
        main.rowconfigure(1, weight=1)

        self._build_display(main)
        self._build_keys(main)

    def _build_display(self, parent):
        display = tk.Frame(parent, bg=DISPLAY, highlightbackground=LINE, highlightthickness=1)
        display.grid(row=0, column=0, sticky="ew", pady=(0, 14))
        display.columnconfigure(0, weight=1)

        top = tk.Frame(display, bg=DISPLAY)
        top.grid(row=0, column=0, sticky="ew", padx=18, pady=(14, 0))

        tk.Label(top, text="Yash's Calculator", bg=DISPLAY, fg=ACCENT, font=self.font_title).pack(side="left")

        self.mode_label = tk.Label(top, text="DEG", bg=DISPLAY, fg=MUTED, font=self.font_small)
        self.mode_label.pack(side="right")
        self.flag_label = tk.Label(top, text="", bg=DISPLAY, fg=EQ, font=self.font_small)
        self.flag_label.pack(side="right", padx=(0, 12))

        self.expr_var = tk.StringVar(value="")
        self.result_var = tk.StringVar(value="0")

        tk.Label(
            display,
            textvariable=self.expr_var,
            bg=DISPLAY,
            fg=MUTED,
            font=self.font_expr,
            anchor="e",
        ).grid(row=1, column=0, sticky="ew", padx=18, pady=(18, 0))
        tk.Label(
            display,
            textvariable=self.result_var,
            bg=DISPLAY,
            fg=TEXT,
            font=self.font_result,
            anchor="e",
        ).grid(row=2, column=0, sticky="ew", padx=18, pady=(4, 18))

    def _build_keys(self, parent):
        pad = tk.Frame(parent, bg=BG)
        pad.grid(row=1, column=0, sticky="nsew")
        for i in range(8):
            pad.rowconfigure(i, weight=1)
        for i in range(6):
            pad.columnconfigure(i, weight=1)

        self.fn_buttons: dict[str, HoverButton] = {}

        layout = [
            [
                ("deg", "DEG", self._toggle_deg, FN, FN_HOVER, FN_FG),
                ("2nd", "2nd", self._toggle_second, FN, FN_HOVER, FN_FG),
                ("hyp", "HYP", self._toggle_hyp, FN, FN_HOVER, FN_FG),
                ("(", "(", lambda: self._insert("("), FN, FN_HOVER, FN_FG),
                (")", ")", lambda: self._insert(")"), FN, FN_HOVER, FN_FG),
                ("ac", "AC", self._clear, DANGER, DANGER_HOVER, DANGER_FG),
            ],
            [
                ("sin", "sin", lambda: self._insert_fn("sin"), FN, FN_HOVER, FN_FG),
                ("cos", "cos", lambda: self._insert_fn("cos"), FN, FN_HOVER, FN_FG),
                ("tan", "tan", lambda: self._insert_fn("tan"), FN, FN_HOVER, FN_FG),
                ("log", "log", lambda: self._insert_fn("log"), FN, FN_HOVER, FN_FG),
                ("ln", "ln", lambda: self._insert_fn("ln"), FN, FN_HOVER, FN_FG),
                ("bk", "⌫", self._backspace, OP, OP_HOVER, OP_FG),
            ],
            [
                ("sqrt", "√", lambda: self._insert_fn("sqrt"), FN, FN_HOVER, FN_FG),
                ("sq", "x²", lambda: self._insert("**2"), FN, FN_HOVER, FN_FG),
                ("pow", "xʸ", lambda: self._insert("**"), FN, FN_HOVER, FN_FG),
                ("fact", "n!", lambda: self._insert_fn("fact"), FN, FN_HOVER, FN_FG),
                ("pi", "π", lambda: self._insert("pi"), FN, FN_HOVER, FN_FG),
                ("e", "e", lambda: self._insert("e"), FN, FN_HOVER, FN_FG),
            ],
            [
                ("7", "7", lambda: self._insert("7"), NUM, NUM_HOVER, NUM_FG),
                ("8", "8", lambda: self._insert("8"), NUM, NUM_HOVER, NUM_FG),
                ("9", "9", lambda: self._insert("9"), NUM, NUM_HOVER, NUM_FG),
                ("div", "÷", lambda: self._insert("/"), OP, OP_HOVER, OP_FG),
                ("mod", "mod", lambda: self._insert("%"), OP, OP_HOVER, OP_FG),
                ("pct", "%", self._percent, OP, OP_HOVER, OP_FG),
            ],
            [
                ("4", "4", lambda: self._insert("4"), NUM, NUM_HOVER, NUM_FG),
                ("5", "5", lambda: self._insert("5"), NUM, NUM_HOVER, NUM_FG),
                ("6", "6", lambda: self._insert("6"), NUM, NUM_HOVER, NUM_FG),
                ("mul", "×", lambda: self._insert("*"), OP, OP_HOVER, OP_FG),
                ("floordiv", "//", lambda: self._insert("//"), OP, OP_HOVER, OP_FG),
                ("inv", "1/x", lambda: self._wrap("1/("), FN, FN_HOVER, FN_FG),
            ],
            [
                ("1", "1", lambda: self._insert("1"), NUM, NUM_HOVER, NUM_FG),
                ("2", "2", lambda: self._insert("2"), NUM, NUM_HOVER, NUM_FG),
                ("3", "3", lambda: self._insert("3"), NUM, NUM_HOVER, NUM_FG),
                ("sub", "−", lambda: self._insert("-"), OP, OP_HOVER, OP_FG),
                ("comb", "nCr", lambda: self._insert_fn("comb"), FN, FN_HOVER, FN_FG),
                ("perm", "nPr", lambda: self._insert_fn("perm"), FN, FN_HOVER, FN_FG),
            ],
            [
                ("0", "0", lambda: self._insert("0"), NUM, NUM_HOVER, NUM_FG),
                ("dot", ".", lambda: self._insert("."), NUM, NUM_HOVER, NUM_FG),
                ("pm", "±", self._plus_minus, NUM, NUM_HOVER, NUM_FG),
                ("add", "+", lambda: self._insert("+"), OP, OP_HOVER, OP_FG),
                ("gcd", "gcd", lambda: self._insert_fn("gcd"), FN, FN_HOVER, FN_FG),
                ("lcm", "lcm", lambda: self._insert_fn("lcm"), FN, FN_HOVER, FN_FG),
            ],
            [
                ("abs", "|x|", lambda: self._insert_fn("abs"), FN, FN_HOVER, FN_FG),
                ("floor", "⌊x⌋", lambda: self._insert_fn("floor"), FN, FN_HOVER, FN_FG),
                ("ceil", "⌈x⌉", lambda: self._insert_fn("ceil"), FN, FN_HOVER, FN_FG),
                ("ans", "Ans", lambda: self._insert("ans"), FN, FN_HOVER, FN_FG),
                ("log2", "log₂", lambda: self._insert_fn("log2"), FN, FN_HOVER, FN_FG),
                ("eq", "=", self._equals, EQ, EQ_HOVER, EQ_FG),
            ],
        ]

        for r, row in enumerate(layout):
            for c, (key, label, cmd, bg, hover, fg) in enumerate(row):
                rim = tk.Frame(pad, bg=KEY_EDGE, padx=1, pady=1)
                rim.grid(row=r, column=c, sticky="nsew", padx=3, pady=3)
                rim.rowconfigure(0, weight=1)
                rim.columnconfigure(0, weight=1)
                btn = HoverButton(
                    rim,
                    hover=hover,
                    text=label,
                    bg=bg,
                    fg=fg,
                    font=self.font_btn,
                    command=cmd,
                )
                btn.grid(row=0, column=0, sticky="nsew")
                if key in {"sin", "cos", "tan", "log", "ln", "sqrt", "sq", "2nd", "hyp", "deg"}:
                    self.fn_buttons[key] = btn

    def _bind_keys(self):
        self.bind("<Return>", lambda _e: self._equals())
        self.bind("<KP_Enter>", lambda _e: self._equals())
        self.bind("<BackSpace>", lambda _e: self._backspace())
        self.bind("<Escape>", lambda _e: self._clear())
        self.bind("^", lambda _e: self._insert("**"))
        for ch in "0123456789.+-*/%()":
            self.bind(ch, lambda e, c=ch: self._insert(c))

    def _sync_expr(self):
        self.expr_var.set(self.expression)

    def _start_new_if_needed(self, incoming: str):
        if self.just_evaluated:
            if incoming[:1].isdigit() or incoming[:1] == "." or incoming in {"pi", "e", "ans"} or incoming.endswith("("):
                self.expression = ""
            self.just_evaluated = False

    def _insert(self, text: str):
        self._start_new_if_needed(text)
        self.expression += text
        self._sync_expr()

    def _insert_fn(self, name: str):
        mapping = self._active_fn_map()
        real = mapping.get(name, name)
        self._insert(f"{real}(")

    def _wrap(self, prefix: str):
        self._start_new_if_needed(prefix)
        if self.expression:
            self.expression = f"{prefix}{self.expression})"
        else:
            self.expression = prefix
        self._sync_expr()

    def _percent(self):
        self._insert("/100")

    def _plus_minus(self):
        if not self.expression:
            self.expression = "-"
        elif self.expression.startswith("-(") and self.expression.endswith(")"):
            self.expression = self.expression[2:-1]
        else:
            self.expression = f"-({self.expression})"
        self.just_evaluated = False
        self._sync_expr()

    def _backspace(self):
        if self.just_evaluated:
            self._clear()
            return
        self.expression = self.expression[:-1]
        self._sync_expr()
        if not self.expression:
            self.result_var.set("0")

    def _clear(self):
        self.expression = ""
        self.just_evaluated = False
        self.expr_var.set("")
        self.result_var.set("0")

    def _equals(self):
        if not self.expression.strip():
            return
        try:
            value = SafeEvaluator(self.angle_mode, self.ans).evaluate(self.expression)
            shown = format_result(value)
            self.ans = float(value)
            self.result_var.set(shown)
            self._add_history(self.expression, shown)
            self.just_evaluated = True
        except Exception:
            self.result_var.set("Error")
            self.just_evaluated = False

    def _add_history(self, expr: str, result: str):
        line = f"{expr}  =  {result}"
        self.history.append((expr, result))
        self.history_list.insert(0, line)

    def _reuse_history(self, _event=None):
        selection = self.history_list.curselection()
        if not selection:
            return
        index = selection[0]
        expr, result = self.history[-(index + 1)]
        self.expression = expr
        self.expr_var.set(expr)
        self.result_var.set(result)
        self.just_evaluated = True

    def _clear_history(self):
        self.history.clear()
        self.history_list.delete(0, "end")

    def _toggle_deg(self):
        self.angle_mode = "RAD" if self.angle_mode == "DEG" else "DEG"
        self._refresh_fn_labels()

    def _toggle_second(self):
        self.second = not self.second
        self._refresh_fn_labels()

    def _toggle_hyp(self):
        self.hyp = not self.hyp
        self._refresh_fn_labels()

    def _active_fn_map(self):
        if self.hyp and self.second:
            return {"sin": "asinh", "cos": "acosh", "tan": "atanh", "log": "pow10", "ln": "exp", "sqrt": "cbrt"}
        if self.hyp:
            return {"sin": "sinh", "cos": "cosh", "tan": "tanh", "log": "log2", "ln": "ln", "sqrt": "sqrt"}
        if self.second:
            return {"sin": "asin", "cos": "acos", "tan": "atan", "log": "pow10", "ln": "exp", "sqrt": "cbrt"}
        return {"sin": "sin", "cos": "cos", "tan": "tan", "log": "log", "ln": "ln", "sqrt": "sqrt"}

    def _refresh_fn_labels(self):
        labels = self._active_fn_map()
        pretty = {
            "sin": "sin",
            "cos": "cos",
            "tan": "tan",
            "asin": "sin⁻¹",
            "acos": "cos⁻¹",
            "atan": "tan⁻¹",
            "sinh": "sinh",
            "cosh": "cosh",
            "tanh": "tanh",
            "asinh": "sinh⁻¹",
            "acosh": "cosh⁻¹",
            "atanh": "tanh⁻¹",
            "log": "log",
            "ln": "ln",
            "log2": "log₂",
            "exp": "eˣ" if self.second else "log",
            "pow10": "10ˣ",
            "sqrt": "√",
            "cbrt": "∛",
        }
        for key in ("sin", "cos", "tan", "log", "ln", "sqrt"):
            name = labels.get(key, key)
            if key == "log" and self.second and not self.hyp:
                self.fn_buttons[key].configure(text="10ˣ")
                continue
            if key == "ln" and self.second:
                self.fn_buttons[key].configure(text="eˣ")
                continue
            self.fn_buttons[key].configure(text=pretty.get(name, name))

        self.fn_buttons["sq"].configure(text="x³" if self.second else "x²")
        self.fn_buttons["sq"]._command = (lambda: self._insert("**3")) if self.second else (lambda: self._insert("**2"))
        self.fn_buttons["deg"].configure(text=self.angle_mode)
        self.fn_buttons["2nd"].configure(fg=ACTIVE_FG if self.second else FN_FG)
        self.fn_buttons["hyp"].configure(fg=ACTIVE_FG if self.hyp else FN_FG)
        flags = []
        if self.second:
            flags.append("2nd")
        if self.hyp:
            flags.append("HYP")
        self.flag_label.configure(text="  ".join(flags))
        self.mode_label.configure(text=self.angle_mode)


def open_calculator():
    app = CalculatorApp()
    app.mainloop()


if __name__ == "__main__":
    open_calculator()
