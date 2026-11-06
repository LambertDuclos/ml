# 00 · tensors and derivatives

No lecture: the prerequisite the course assumes. Write `tensors.py` here with plain Python and
`math`, no numpy inside it; the tests judge you against numpy and torch. Scratch cells go in
`explore.py` (molten: `<leader>mi` to start the `ml` kernel, `<leader>mvip` to run a paragraph).

**Assumes:** Python functions, loops, lists and tuples; high-school algebra (powers, and what tanh,
exp and log are as functions). Nothing else: this lesson is the floor. If one of these is not
there, say "gap" before sitting 1 (`CLAUDE.md`, "Gaps").

| Sitting | Tests | Before writing |
|---|---|---|
| 1 | `test_broadcast_shape`, `test_matmul_by_hand` | numpy's broadcasting rules, read once: https://numpy.org/doc/stable/user/basics.broadcasting.html. 3Blue1Brown, *Essence of Linear Algebra*, ch. 4 (matrix multiplication as composition). |
| 2 | `test_numerical_derivative`, `test_chain_rule` | 3Blue1Brown, *Essence of Calculus*, ch. 2 to 4 (derivative, chain rule). MML §5.1 and 5.2. Do the chain rule on `tanh(x·eˣ)` on paper first. |
| 3 | `test_softmax_cross_entropy` | Derive d(cross-entropy)/d(logits) on paper before coding: you should land on softmax minus one-hot. Then ask yourself why `exp(1000)` is a problem and what subtracting the max does. |

Run: `uv run pytest courses/zero-to-hero/00-tensors-and-derivatives -q`

Done when all five tests are green. Then `notes.md`: the broadcasting rule in one sentence, what a
derivative measures, the chain rule on `tanh(x·eˣ)` written out in LaTeX, and why subtracting the
max leaves softmax unchanged. Glossary lines: shape, broadcasting, derivative, chain rule, logit,
softmax, cross-entropy.
