# Rebuilds

First sitting of each month. The tutor proposes the earlier lesson whose glossary dates are oldest;
I create `rebuilds/<lesson>-<YYYY-MM>/`, copy only its `test_*.py` in, and rebuild the
implementation from memory in thirty minutes, notes and original closed. Then:

    uv run pytest rebuilds/<folder> -q

What failed goes in the journal and, if it is a concept, back to the top of the glossary's review
list. The folder stays: the diff against the original is the honest measure. These folders are
excluded from the default `uv run pytest` because they reuse the lessons' test file names.
