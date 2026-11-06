"""Lesson 1, micrograd. This file is the assignment.

Write `micrograd.py` in this folder with Karpathy's API, so the video and this file speak the same
language: `Value(data)` with `.data`, `.grad`, `.backward()`; `Neuron(nin)`, `Layer(nin, nout)`,
`MLP(nin, nouts)` with `.parameters()`; a `Layer` with one neuron returns a single `Value`, not a
list. Plus `train(model, xs, ys, steps, lr)`, yours: returns the list of losses, one per step, where
the loss is the sum of squared errors, as in the video, and one step is: zero every grad, backward,
`p.data -= lr * p.grad`. Five sittings:

  1. test_forward                  Value with + - * / ** neg, tanh, exp
  2. test_backward_neuron          the grads of one neuron, the video's numbers
  3. test_backward_matches_torch   backward() over any graph, torch agrees
  4. test_gradient_accumulation    the bug when a node is used twice
  5. test_mlp_learns               Neuron, Layer, MLP, and your training loop

Run:  uv run pytest courses/zero-to-hero/01-micrograd -q
"""

import math
import random

import pytest
import torch


def test_forward():
    """`Value` holds a float and remembers how it was made. Arithmetic with another Value or with a
    plain number, on either side. `grad` starts at 0."""
    from micrograd import Value

    a, b = Value(2.0), Value(-3.0)
    assert (a + b).data == -1.0
    assert (a * b).data == -6.0
    assert (a - b).data == 5.0
    assert (a / b).data == pytest.approx(-2 / 3)
    assert (a**3).data == 8.0
    assert (-a).data == -2.0
    assert (2 + a).data == 4.0
    assert (2 * a).data == 4.0
    assert (1 - a).data == -1.0
    assert (1 / a).data == 0.5
    assert a.tanh().data == pytest.approx(math.tanh(2.0))
    assert a.exp().data == pytest.approx(math.exp(2.0))
    assert a.grad == 0.0
    c = a * b + a
    assert c.data == -4.0


def test_backward_neuron():
    """The neuron from the video: o = tanh(x1*w1 + x2*w2 + b). After o.backward(), each grad is
    d o / d that value. Do it on paper first; the numbers below are the ones Karpathy gets."""
    from micrograd import Value

    x1, x2 = Value(2.0), Value(0.0)
    w1, w2 = Value(-3.0), Value(1.0)
    b = Value(6.8813735870195432)
    n = x1 * w1 + x2 * w2 + b
    o = n.tanh()
    o.backward()
    assert o.data == pytest.approx(0.7071, abs=1e-4)
    assert o.grad == 1.0
    assert n.grad == pytest.approx(0.5, abs=1e-4)
    assert x1.grad == pytest.approx(-1.5, abs=1e-4)
    assert w1.grad == pytest.approx(1.0, abs=1e-4)
    assert x2.grad == pytest.approx(0.5, abs=1e-4)
    assert w2.grad == pytest.approx(0.0, abs=1e-4)


def test_backward_matches_torch():
    """The same expression built with your Values and with torch tensors must give the same value
    and the same gradients. torch is the judge, to 1e-6."""
    from micrograd import Value

    def graph(a, b, c, d):
        return ((a * b + c) ** 2 / (d.exp() + 1)).tanh() - a / b

    inputs = (0.7, -1.3, 2.0, 0.4)
    vals = [Value(v) for v in inputs]
    out = graph(*vals)
    out.backward()

    ts = [torch.tensor(v, dtype=torch.float64, requires_grad=True) for v in inputs]
    tout = graph(*ts)
    tout.backward()

    assert out.data == pytest.approx(tout.item(), abs=1e-6)
    for v, t in zip(vals, ts):
        assert v.grad == pytest.approx(t.grad.item(), abs=1e-6)


def test_gradient_accumulation():
    """A node used twice receives gradient from both uses. Karpathy's bug, and his numbers:
    f = (a*b) * (a+b) with a=-2, b=3 gives df/da = -3 and df/db = -8."""
    from micrograd import Value

    a = Value(3.0)
    (a + a).backward()
    assert a.grad == 2.0

    a = Value(3.0)
    (a * a).backward()
    assert a.grad == 6.0

    a, b = Value(-2.0), Value(3.0)
    f = (a * b) * (a + b)
    f.backward()
    assert f.data == -6.0
    assert a.grad == pytest.approx(-3.0)
    assert b.grad == pytest.approx(-8.0)


def test_mlp_learns():
    """MLP(3, [4, 4, 1]) on the video's four examples. 41 parameters; your `train` brings the
    sum-of-squares loss under 0.05 in 100 steps at lr 0.05, and the signs of the predictions match
    the targets. The seed makes the initial weights reproducible."""
    from micrograd import MLP, train

    random.seed(1337)
    model = MLP(3, [4, 4, 1])
    assert len(model.parameters()) == 41

    xs = [[2.0, 3.0, -1.0], [3.0, -1.0, 0.5], [0.5, 1.0, 1.0], [1.0, 1.0, -1.0]]
    ys = [1.0, -1.0, -1.0, 1.0]
    losses = train(model, xs, ys, steps=100, lr=0.05)

    assert len(losses) == 100
    assert losses[-1] < losses[0]
    assert losses[-1] < 0.05
    for x, y in zip(xs, ys):
        assert (model(x).data > 0) == (y > 0)
