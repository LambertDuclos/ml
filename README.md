# ml

Deep learning from the ground up, built by hand and checked against PyTorch.

This is a learning repository, kept public on purpose. I am working through Andrej Karpathy's
*Neural Networks: Zero to Hero*, the mathematics behind it, and then papers, towards graduate
research in foundation models. Every mechanism here (backpropagation, the MLP, batch norm,
attention, the tokenizer) is written by me from scratch. The tests that judge it, and the plumbing
around it, are written by Claude Code acting as a tutor that never writes the lesson's code.

## The method

One loop per lesson:

1. The tutor writes the test file first. The test is the assignment and the only judge: my
   implementation must match `torch.autograd` or numpy numerically.
2. I watch the lecture segment, then close the video and build the thing from the test, with no
   copy-paste. Writing it twice is where it sticks.
3. When stuck, help comes one rung at a time: a question, then the concept (a picture, tiny
   numbers, then the formula), then pseudocode, and only on the explicit word "solution" a
   reference in `ref/`, which I then rebuild blind the next day.
4. Green tests, then exercises (predict, break, modify, extend), then `notes.md` in my own words,
   read by a critic that sees only the notes and reports what is false, vague or missing.
5. Daily: re-explain the concept I have not touched for longest. Monthly: rebuild an earlier lesson
   blind in thirty minutes.

The tutor's contract and the session protocol are in `CLAUDE.md`.

## Map

- `courses/zero-to-hero/` — Karpathy's course, one folder per lecture: `README.md` (segments and
  sittings), `test_*.py` (the assignment), my implementation, `explore.py` (scratch cells),
  `notes.md`, `exercises.md`.
- `courses/maths/` — linear algebra, calculus, probability, optimisation, from *Mathematics for
  Machine Learning* (Deisenroth, Faisal, Ong), with numerical tests.
- `core/` — my own small library, promoted lesson after lesson (Linear, BatchNorm, attention…).
- `papers/` — one folder per paper: notes (claim, method, what is new, what is weak), a
  reproduction of one number, and the questions I would ask the authors.
- `rebuilds/` — the monthly blind rebuilds.
- `glossary.md`, `questions.md` — concepts in my words with review dates; questions I cannot
  answer yet.

## Where I am

| Track | Lesson | Tests green | Since |
|---|---|---|---|
| Zero to Hero | 00 tensors and derivatives | 0/5 | 2026-11-06 |
| Maths | 01 linear algebra | 0/4 | 2026-11-06 |

## Setup

```sh
brew install graphviz imagemagick   # expression graphs; inline plots in neovim
uv sync                             # Python 3.14, torch, numpy, matplotlib, sympy, pytest
uv run pytest                       # everything, including the tutor's own guard
bin/ml session                      # open a sitting with the tutor (Claude Code)
```

Apple M4, PyTorch on MPS. Lessons 0 to 8 run locally; the GPT-2 reproduction needs a rented GPU.

## Acknowledgements

Andrej Karpathy for the course; Deisenroth, Faisal and Ong for the book; 3Blue1Brown for the
pictures. MIT license.
