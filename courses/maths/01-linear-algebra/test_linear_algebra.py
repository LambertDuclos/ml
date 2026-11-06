"""Maths 01, linear algebra. This file is the assignment: write `linalg.py` next to it.

  1. test_projection, test_power_iteration             (sitting 1)
  2. test_low_rank_approximation, test_least_squares   (sitting 2)

Run:  uv run pytest courses/maths/01-linear-algebra -q
"""

import numpy as np
import pytest


def test_projection():
    """`project(v, u)`: the orthogonal projection of vector v onto the line spanned by u, which is
    (v·u / u·u) u. Derive it from "the residual v - p is orthogonal to u" before coding it."""
    from linalg import project

    rng = np.random.default_rng(0)
    for _ in range(5):
        v, u = rng.normal(size=4), rng.normal(size=4)  # (4,), (4,)
        p = project(v, u)
        np.testing.assert_allclose(p, (v @ u) / (u @ u) * u, atol=1e-12)
        assert abs((v - p) @ u) < 1e-10  # residual orthogonal to u
        assert np.linalg.matrix_rank(np.stack([p, u])) == 1  # p lies on the line of u


def test_power_iteration():
    """`top_eigenvector(A, iters=1000)`: the unit eigenvector of the largest eigenvalue of a
    symmetric matrix, by repeated multiplication and normalisation. Compared with np.linalg.eigh up
    to sign; and the Rayleigh quotient v·Av must be the top eigenvalue."""
    from linalg import top_eigenvector

    rng = np.random.default_rng(1)
    M = rng.normal(size=(6, 6))
    A = M @ M.T  # (6, 6), symmetric positive semi-definite
    v = top_eigenvector(A, iters=1000)
    assert v.shape == (6,)
    assert abs(np.linalg.norm(v) - 1) < 1e-9
    w, V = np.linalg.eigh(A)  # eigenvalues ascending, eigenvectors in columns
    assert abs(abs(v @ V[:, -1]) - 1) < 1e-6
    assert v @ A @ v == pytest.approx(w[-1], rel=1e-6)


def test_low_rank_approximation():
    """`low_rank(A, k)`: the best rank-k approximation of A, by truncating its SVD. Eckart–Young
    says the error in spectral norm is exactly the (k+1)-th singular value: check that, it is the
    whole point."""
    from linalg import low_rank

    rng = np.random.default_rng(2)
    A = rng.normal(size=(8, 5))  # (8, 5)
    s = np.linalg.svd(A, compute_uv=False)  # singular values, descending
    for k in (1, 2, 4):
        Ak = low_rank(A, k)
        assert Ak.shape == A.shape
        assert np.linalg.matrix_rank(Ak) == k
        assert np.linalg.norm(A - Ak, ord=2) == pytest.approx(s[k], rel=1e-9)
    np.testing.assert_allclose(low_rank(A, 5), A, atol=1e-10)


def test_least_squares():
    """`least_squares(X, y)`: the w minimising ||Xw - y||², through the normal equations
    (XᵀX) w = Xᵀy. Compared with np.linalg.lstsq; and the residual must be orthogonal to every
    column of X, because least squares is a projection."""
    from linalg import least_squares

    rng = np.random.default_rng(3)
    X = rng.normal(size=(20, 3))  # (20, 3)
    w_true = np.array([1.0, -2.0, 0.5])
    y = X @ w_true + 0.1 * rng.normal(size=20)  # (20,)
    w = least_squares(X, y)
    np.testing.assert_allclose(w, np.linalg.lstsq(X, y, rcond=None)[0], atol=1e-9)
    assert np.abs(X.T @ (y - X @ w)).max() < 1e-9
