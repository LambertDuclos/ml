"""Plumbing for lesson 1, written by the tutor: draw the expression graph as in the video.

Needs the `graphviz` package (in pyproject) and the `dot` binary (`brew install graphviz`).
In explore.py:   from plot import draw_dot; draw_dot(o).render("graph", view=True)
Your Value must expose `data`, `grad`, `_prev` (its children) and `_op` (a str, '' for a leaf);
a `label` attribute is used when present.
"""

from graphviz import Digraph


def trace(root):
    """All nodes and edges reachable from root, walking children."""
    nodes, edges = set(), set()

    def build(v):
        if v not in nodes:
            nodes.add(v)
            for child in getattr(v, "_prev", ()):
                edges.add((child, v))
                build(child)

    build(root)
    return nodes, edges


def draw_dot(root, fmt="svg", rankdir="LR"):
    """A graphviz Digraph of the expression ending at root: one record per Value, one small node
    per operation."""
    dot = Digraph(format=fmt, graph_attr={"rankdir": rankdir})
    nodes, edges = trace(root)
    for n in nodes:
        uid = str(id(n))
        label = getattr(n, "label", "")
        dot.node(
            name=uid,
            label=f"{{ {label} | data {n.data:.4f} | grad {n.grad:.4f} }}",
            shape="record",
        )
        if n._op:
            dot.node(name=uid + n._op, label=n._op)
            dot.edge(uid + n._op, uid)
    for n1, n2 in edges:
        dot.edge(str(id(n1)), str(id(n2)) + n2._op)
    return dot
