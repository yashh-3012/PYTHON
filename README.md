# 🐍 PYTHON — My Python Learning Journey

> My first repository: a collection of programs I write while learning Python, built up from Class 12 revision to college-level concepts.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)
![Status](https://img.shields.io/badge/status-learning%20in%20progress-orange)
![Type](https://img.shields.io/badge/type-practice%20projects-green)

---

## 📑 Table of Contents

1. [About](#-about)
2. [Repository Structure](#-repository-structure)
3. [Requirements](#-requirements)
4. [Getting Started](#-getting-started)
5. [Menu-Driven Program](#-menu-driven-program)
6. [Scientific Calculator](#-scientific-calculator)
7. [Python Concepts Covered](#-python-concepts-covered)
8. [Data Persistence](#-data-persistence)
9. [Roadmap](#-roadmap)
10. [Author](#-author)

---

## 📖 About

This repository holds the code for the Python skills I am learning. It started as revision of my 12th-grade concepts and keeps growing as I learn more in my B.Tech CSE course.

The two main projects are:

| Project | File | What it is |
|---|---|---|
| Menu-driven program | `Menu_driven_prog.py` | 27 mini programs (games, utilities, algorithms) behind one console menu |
| Scientific calculator | `calculator.py` | A dark-themed, clickable calculator built with Tkinter |

---

## 📂 Repository Structure

```
PYTHON/
├── Menu_driven_prog.py   # Main console program with 27 options
├── calculator.py         # Scientific calculator (Tkinter GUI)
├── yash.py               # Small module used to demo importing
├── scores.json           # Auto-created on first game played (leaderboard data)
└── README.md             # You are here
```

---

## ⚙️ Requirements

- **Python 3.10 or newer** (the code uses `match`–`case`)
- **Tkinter** (only for the calculator; it ships with most Python installers)
- No third-party packages needed. Only the standard library is used: `random`, `json`, `time`, `math`, `ast`, `functools`, `tkinter`

---

## 🚀 Getting Started

**1. Clone the repository**

```bash
git clone https://github.com/yashh-3012/PYTHON.git
cd PYTHON
```

**2. Run the menu-driven program**

```bash
python3 Menu_driven_prog.py
```

**3. Run the calculator on its own**

```bash
python3 calculator.py
```

> On Windows, use `python` instead of `python3`.

---

## 🎮 Menu-Driven Program

Run `Menu_driven_prog.py` and enter the number of the option you want. The menu repeats until you choose **28 (Exit)**.

### 🕹️ Games

| # | Option | Description |
|---|---|---|
| 1 | Finger Cricket | Bat against the computer; you are out when the numbers match |
| 2 | Odd / Even | Pick odd or even, then add your number to the computer's |
| 3 | Number Guessing | Guess a number from 1 to 100 in 5 attempts |
| 4 | Rock Paper Scissors | Classic game against the computer |
| 13 | KBC | Six-level quiz with prize money |
| 18 | Word Guessing | Guess the hidden word letter by letter, with hints |

### 🔧 Utilities

| # | Option | Description |
|---|---|---|
| 5 | Time | Shows the current time and a matching greeting |
| 6 | Reverse Number | Reverses the digits of a number |
| 7 | Check Palindrome | Works for both numbers and strings |
| 8 | Voting System | Simple vote using `match`–`case` |
| 9 | Do-While | Emulates a do-while loop in Python |
| 12 | List of Cubes | Cubes over a range using a list comprehension |
| 19 | String Code / Decode | Scrambles and recovers words |
| 21 | Multiplication Table | Built with a `lambda` function |
| 22 | Leaderboard | Shows saved scores for all games |
| 23 | Calculator | Opens the scientific calculator window |

### 🧮 Concept Demos

| # | Option | Concept |
|---|---|---|
| 10 | Addition | `*args` (variable-length arguments) |
| 11 | Check AP | `**kwargs` (keyword arguments) |
| 14 | Fibonacci Series | Recursion and docstrings |
| 15 | Set Methods | Union, intersection, difference, and more |
| 16 | Square Root | `try` / `except` / `finally` |
| 17 | Square Function | Raising errors with `raise` |
| 20 | Import Module | Importing a function from `yash.py` |
| 27 | Map, Filter, Reduce | Higher-order functions |

### 📊 Sorting Algorithms

| # | Algorithm | Shows each pass? |
|---|---|---|
| 24 | Bubble Sort | ✅ |
| 25 | Selection Sort | ✅ |
| 26 | Insertion Sort | ✅ |

---

## 🧮 Scientific Calculator

A clickable scientific calculator with a dark theme, built using **Tkinter**.

**Features**

- Basic operations: `+ − × ÷`, modulus, floor division, percent, powers
- Trigonometric functions with **DEG / RAD** mode
- **2nd** and **HYP** keys for inverse and hyperbolic functions
- Logarithms (`log`, `ln`, `log₂`), square root, cube root, factorial
- `nCr`, `nPr`, `gcd`, `lcm`, `abs`, `floor`, `ceil`
- Constants `π` and `e`, plus an `Ans` key for the last result
- **History panel**: click any past line to reuse it
- Keyboard support: digits, operators, `Enter`, `Backspace`, `Esc`

**Safe evaluation:** expressions are parsed with Python's `ast` module and only whitelisted operators and functions are allowed, so `eval()` is never used on calculator input.

---

## 💡 Python Concepts Covered

- Variables, data types, input and output
- Conditionals (`if` / `elif` / `else`) and `match`–`case`
- Loops (`for`, `while`, do-while pattern)
- Functions, default and variable-length arguments (`*args`, `**kwargs`)
- Recursion and docstrings
- Lists, sets, dictionaries, tuples, list comprehensions
- Lambda, `map`, `filter`, `reduce`
- Exception handling (`try`, `except`, `finally`, `raise`)
- Modules and imports
- File handling and JSON
- Sorting algorithms
- Object-oriented programming and GUI building (Tkinter)
- Abstract syntax trees (`ast`) for safe expression evaluation

---

## 💾 Data Persistence

Game scores are saved in a `scores.json` file so they survive after the program is closed. If the file does not exist, it is created automatically with default values.

Tracked stats:

| Game | Saved data |
|---|---|
| Finger Cricket | Best score, games played |
| Odd / Even | Wins, losses |
| Number Guessing | Wins, fewest attempts |
| Rock Paper Scissors | Wins, losses, ties |
| KBC | Best prize, games played |

---

## 🗺️ Roadmap

- [ ] Replace `eval()` in menu options 10 and 11 with safer input parsing
- [ ] Add input validation for all numeric prompts
- [ ] Split the menu program into smaller modules
- [ ] Add more data-structure and algorithm programs (stacks, queues, searching)
- [ ] Add OOP-based projects
- [ ] Add unit tests

---

## 👤 Author

**Yash**
B.Tech CSE, VIT Vellore

GitHub: [@yashh-3012](https://github.com/yashh-3012)

---

⭐ If you are also learning Python, feel free to explore the code and star the repo!