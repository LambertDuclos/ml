# 01 · linear algebra

MML chapters 2 (linear algebra), 3 (analytic geometry), 4 (matrix decompositions); pictures from
3Blue1Brown, *Essence of Linear Algebra*. Write `linalg.py` here; numpy is allowed for the primitives
(`@`, `np.linalg.svd`, `np.linalg.solve`): the point is the construction, not reimplementing LAPACK.

**Assumes:** vectors and the dot product, matrix multiplication (lesson 0), numpy indexing basics.
Eigenvectors and the SVD are what you learn here, not what you need coming in.

| Sitting | Tests | Read first |
|---|---|---|
| 1 | `test_projection`, `test_power_iteration` | MML §3.8 (projections), §4.2 (eigenvalues and eigenvectors); 3Blue1Brown ch. 14. Derive the projection from "the residual is orthogonal to u". |
| 2 | `test_low_rank_approximation`, `test_least_squares` | MML §4.5 and 4.6 (SVD, Eckart–Young), §9.2 (least squares as a projection). |

Run: `uv run pytest courses/maths/01-linear-algebra -q`

`notes.md`: each result derived in LaTeX, and one sentence on where it shows up in deep learning
(projection: attention scores; eigenvalues: why training can blow up; low rank: LoRA; least
squares: the simplest "learning").
