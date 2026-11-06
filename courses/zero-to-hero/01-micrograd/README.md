# 01 · micrograd

Lecture: *The spelled-out intro to neural networks and backpropagation: building micrograd*
(2 h 25), the first video at https://karpathy.ai/zero-to-hero.html. Timestamps below are
approximate chapter marks.

Write `micrograd.py` here with Karpathy's names (`Value`, `_prev`, `_op`, `_backward`, `backward`,
`Neuron`, `Layer`, `MLP`) so that the video and `test_micrograd.py` speak the same language, plus a
`train` function of your own. Scratch cells go in `explore.py` (molten). `plot.py` is the tutor's:
`from plot import draw_dot` draws the expression graph as in the video.

**Assumes:** lesson 0 (derivatives, the chain rule); Python classes and operator overloading
(`__add__`, `__mul__`, and the reflected `__radd__`, `__rmul__` that make `2 * a` work); a function
defined inside another that remembers the variables around it (a closure, which is what each
`_backward` is); recursion (the topological sort); Python sets. Ask for a detour on any of these
before sitting 1 (`CLAUDE.md`, "Gaps").

| Sitting | Test | Watch first | Then build, video closed |
|---|---|---|---|
| 1 | `test_forward` | 0:00 → 0:40 (derivatives by hand, the `Value` object, the graph) | `Value` with `+ - * / **`, `neg`, `tanh`, `exp`, and the right-hand forms (`2 * a`, `1 - a`) |
| 2 | `test_backward_neuron` | 0:40 → 1:09 (manual backprop, twice) | the neuron on paper first, then `_backward` per op and `backward()` |
| 3 | `test_backward_matches_torch` | 1:09 → 1:43 (backward over a whole graph; the same in PyTorch) | every op has its `_backward`; torch agrees to 1e-6 |
| 4 | `test_gradient_accumulation` | 1:22 → 1:27 (the bug when a node is used twice) | find the bug yourself before watching the fix |
| 5 | `test_mlp_learns` | 1:43 → 2:14 (`Neuron`, `Layer`, `MLP`, loss, gradient descent) | the net and your own `train` loop |

Run: `uv run pytest courses/zero-to-hero/01-micrograd -q`

Done when all five are green. Then `exercises.md` (the examiner), `notes.md` (you, for a reader
who was not there: what backpropagation is, the chain rule written out for one `*` node, the
topological order and why `+=`), and one glossary line per concept: computational graph, local
derivative, chain rule, topological order, gradient accumulation, neuron, MLP, loss, gradient
descent, learning rate.
