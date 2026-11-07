"""Lesson 0, tensors and derivatives. This file is the assignment.

Write `tensors.py` in this folder with plain Python and `math`: you implement, numpy and torch
judge. Three sittings:

  1. test_broadcast_shape, test_matmul_by_hand    shapes: what broadcasting and matmul really do
  2. test_numerical_derivative, test_chain_rule   what a derivative is, numerically, then by rule
  3. test_softmax_cross_entropy                   the loss every classifier in this course uses

Run:  uv run pytest courses/zero-to-hero/00-tensors-and-derivatives -q
"""

import math
import random

import numpy as np
import pytest
import torch


def test_broadcast_shape():
    """`broadcast_shape(a, b)` takes two shapes (tuples of ints) and returns the broadcast shape, a
    tuple too (a list never equals a tuple in Python), by numpy's rule: align from the right; each
    pair of sizes must be equal, or one of them must be 1, and the result takes the larger. Raise
    ValueError when they cannot broadcast."""
    from tensors import broadcast_shape

    cases = [
        ((3, 1), (1, 4)),
        ((5,), (2, 5)),
        ((2, 3, 1), (3, 4)),
        ((1,), (3,)),
        ((), (2,)),
        ((4, 1, 6), (1, 5, 1)),
    ]
    for a, b in cases:
        assert broadcast_shape(a, b) == np.broadcast_shapes(a, b), (a, b)
        assert broadcast_shape(b, a) == np.broadcast_shapes(b, a), (b, a)
    with pytest.raises(ValueError):
        broadcast_shape((3,), (4,))
    with pytest.raises(ValueError):
        broadcast_shape((2, 3), (3, 2))


def test_matmul_by_hand():
    """`matmul(A, B)` on nested lists of floats (rows), with explicit loops, returns nested lists.
    Raise ValueError when the inner dimensions differ. Write down the three loops and what each
    index means before typing them."""
    from tensors import matmul

    rng = random.Random(0)
    A = [[rng.uniform(-1, 1) for _ in range(4)] for _ in range(3)]  # (3, 4)
    B = [[rng.uniform(-1, 1) for _ in range(2)] for _ in range(4)]  # (4, 2)
    C = matmul(A, B)  # (3, 2)
    assert len(C) == 3 and all(len(row) == 2 for row in C)
    np.testing.assert_allclose(np.array(C), np.array(A) @ np.array(B), atol=1e-12)
    with pytest.raises(ValueError):
        matmul(A, A)


def test_numerical_derivative():
    """`numerical_derivative(f, x, h=1e-5)` is the central difference (f(x+h) - f(x-h)) / (2h).
    Then four derivatives you write by hand as functions of x: `d_square`, `d_tanh`, `d_exp`,
    `d_log`. The numerical one is the judge."""
    from tensors import d_exp, d_log, d_square, d_tanh, numerical_derivative

    for x in (-2.0, -0.5, 0.0, 0.3, 1.7):
        assert numerical_derivative(lambda t: t**2, x) == pytest.approx(2 * x, abs=1e-6)
        assert d_square(x) == pytest.approx(numerical_derivative(lambda t: t**2, x), abs=1e-6)
        assert d_tanh(x) == pytest.approx(numerical_derivative(math.tanh, x), abs=1e-6)
        assert d_exp(x) == pytest.approx(numerical_derivative(math.exp, x), abs=1e-6)
    for x in (0.1, 0.5, 2.0, 10.0):
        assert d_log(x) == pytest.approx(numerical_derivative(math.log, x), abs=1e-6)


def test_chain_rule():
    """`composite(x) = tanh(x * exp(x))` and `d_composite(x)`, its derivative written by the chain
    rule on paper first (name each rule you use in notes.md: product rule inside, chain rule
    outside). Judged twice: numerically, and by torch.autograd, which is what the rest of the
    course automates."""
    from tensors import composite, d_composite, numerical_derivative

    for x in (-1.5, -0.3, 0.0, 0.4, 0.9):
        assert composite(x) == pytest.approx(math.tanh(x * math.exp(x)))
        assert d_composite(x) == pytest.approx(numerical_derivative(composite, x), abs=1e-6)
        t = torch.tensor(x, dtype=torch.float64, requires_grad=True)
        torch.tanh(t * torch.exp(t)).backward()
        assert d_composite(x) == pytest.approx(t.grad.item(), abs=1e-9)


def test_softmax_cross_entropy():
    """`softmax(logits)` on a list of floats; `cross_entropy(logits, target)` = -log(softmax[target]);
    `d_cross_entropy(logits, target)`, its gradient with respect to the logits, derived by hand (it
    comes out as softmax minus one-hot: check it, then believe it). Judged against torch.
    The last two cases have huge logits: a naive exp overflows, so subtract the max first, and
    explain in notes.md why that changes nothing."""
    from tensors import cross_entropy, d_cross_entropy, softmax

    cases = [
        ([2.0, 1.0, 0.1], 0),
        ([-1.0, 0.0, 1.0, 2.0], 3),
        ([0.0, 0.0], 1),
        ([1000.0, 1000.0, 1000.0], 2),
        ([500.0, -500.0, 0.0], 1),
    ]
    for logits, target in cases:
        t = torch.tensor(logits, dtype=torch.float64, requires_grad=True)
        p = softmax(logits)
        assert sum(p) == pytest.approx(1.0)
        np.testing.assert_allclose(p, torch.softmax(t, dim=0).detach().numpy(), atol=1e-9)
        loss = torch.nn.functional.cross_entropy(t, torch.tensor(target))
        assert cross_entropy(logits, target) == pytest.approx(loss.item(), abs=1e-9)
        loss.backward()
        np.testing.assert_allclose(d_cross_entropy(logits, target), t.grad.numpy(), atol=1e-9)
