# ml

The repo where Lambert learns deep learning and foundation models from the ground up, towards a
master's and then a PhD. This file is the contract between him and Claude: the tutor
(`.claude/agents/tutor.md`) and its agents cite it as `` `CLAUDE.md`, "Title" `` instead of copying
it. Everything in this repo is in English, the method and the journal included (Lambert's decision,
6 November 2026).

## Who writes what

The principle: Lambert writes the code that *is* the mechanism; Claude writes the code around it.

- Lambert's, and his alone: every implementation file under `courses/`, `core/` and `papers/`
  (`tensors.py`, `micrograd.py`, `linalg.py`, `repro.py`…), his `notes.md`, his `explore.py`, and
  everything under `rebuilds/`.
- Claude's: `README.md`, `test_*.py`, `conftest.py`, `data.py`, `plot.py`, `exercises.md`,
  `__init__.py`, and everything under a `ref/` folder ("The ladder"). At the root, `questions.md`
  entirely, and `glossary.md` for the date column only.
- The hook `.claude/hooks/guard.py` refuses Claude the editing tools on Lambert's files, and the
  obvious Bash writes aimed at them (`>`, `>>`, `tee`, `sed -i`, `cp`, `mv`, `rm`). A script that
  opens the file itself, or a `cd` followed by a relative path, gets through: known holes, the rule
  holds through the tutor's prompt.
- Neither Claude nor Lambert pastes text from the conversation into one of Lambert's files: what he
  keeps from an explanation, he rewrites in his own words. The conversation is disposable.

Why (Lambert's decision, 6 November 2026, after his question "am I learning the code or the
concept?"): the concept alone is not enough (you "understand" attention from a blog post and still
do not know why the scores are divided by √d until a softmax saturates in your own code); the syntax
is worth nothing (Claude does it better); between the two sits the mechanism, which you own only
after building it once. That is what Lambert writes, and nothing else.

## Gates

- `uv run pytest <lesson folder> -q`: green means the lesson is done. The test compares Lambert's
  code to PyTorch or numpy, never to an agent's opinion.
- The test is the assignment: the tutor writes it before Lambert writes a line, one test function
  per sitting, in the order of the video's segments. Its API follows Karpathy's, so the video and
  the test speak the same language.
- Lambert runs the tests himself, in a tmux pane. The tutor runs them at the opening, at the close,
  and when Lambert says he is stuck.
- A new test file is proven before Lambert sees it: the tutor runs it against a throwaway reference
  implementation kept outside the repo (all green) and without one (red for the right reason), then
  deletes the reference. A wrong test costs a sitting and a false belief.
- `uv run pytest` at the root runs everything, `tests/` (the guard) included; `rebuilds/` and `ref/`
  are excluded (`pyproject.toml`). `bin/ml tests` does the same.

## The ladder

When Lambert is stuck, help climbs one rung at a time, each one asked for, each one announced
("rung 2:") and each one logged in the journal with the time:

1. a question that says where to look;
2. the concept: a picture, then an example with three numbers, then the formula ("Talking to
   Lambert");
3. pseudocode, in the tutor's words, never code to paste;
4. a reference implementation of the one stuck piece, written in the lesson's `ref/`, never in his
   file, only on the word "solution". The next sitting then opens with a blind rebuild of that
   piece, `ref/` closed: the reference replaces the video, not the writing.

The tutor never offers a rung on its own, with one exception: after twenty minutes on the same
blocker (it reads the clock with `date` at each hint), it offers the next rung, once. Lambert's
decisions, 6 November 2026.

## Gaps

Being stuck on the lesson's mechanism is what the ladder is for. Being stuck because the lesson
assumes something nobody taught (a derivative rule, matrix multiplication, a Python dunder method, a
closure, what a logit is) is a gap, and a gap is not a rung: filling it costs nothing on the ladder,
because the ladder protects the mechanism, not prior knowledge.

- Who calls it: Lambert ("gap: I don't know what X is"), or the tutor, whose rung 1 question reveals
  it. The tutor then says "gap: X" instead of "rung 2", and the twenty-minute clock restarts once
  the gap is filled.
- A small gap (one definition or one rule; he can go on with today's test within the sitting): the
  tutor explains it on the spot, picture, three numbers, formula, and Lambert writes one glossary
  line. Logged in the journal under "Gaps".
- A large gap (it needs practice, or more than a quarter of an hour): a detour, one or two sittings
  at most, with the same shape as a lesson: `README.md`, a `test_*.py` that covers what the lesson
  needed and nothing more, his file, `notes.md`. A maths gap pulls the matching block of
  `courses/maths/` forward (this week's maths sitting happens now); any other gap, or a maths gap
  below block 1, lives in `courses/detours/<topic>/`. The lesson waits; the detour's test going
  green is what ends it. Small or large is the tutor's call, said with its reason; Lambert can
  override, he knows his own head.
- Prevention: every lesson `README.md` carries an "Assumes" line, the prior knowledge the video and
  the test take for granted. Lambert reads it before sitting 1 and asks for the detour then, before
  being stuck.
- Record: `courses/detours/README.md` lists every detour with the lesson that needed it. Over months
  it says where the course's assumptions were thin.

## Closing a lesson

1. Every test of the lesson green.
2. `exercises.md`, written by the examiner (launched with the lesson's path only), done by Lambert.
3. `notes.md`, written by Lambert for a reader who was not there: what he understood, with the
   derivations in LaTeX. The critic reads it alone, without the conversation, and returns `SOLID` or
   `FRAGILE` with the gaps; Lambert fills them; one second pass at most, the rest goes to
   `questions.md`.
4. One line per new concept in `glossary.md`, in his words.
5. Whatever will be reused moves to `core/` with its test (from lesson 3: `Linear`, `BatchNorm1d`…).
6. The commit and the journal entry ("Shipping", "The session").

## The session

- Opening: `bin/ml session` from the repo. A fresh session per sitting, never `--continue`: the
  state lives in the world, not in the conversation. The four homes of the state: the journal,
  "Where I am" in `README.md`, `glossary.md`, `questions.md`. The tutor reads them, runs the current
  lesson's tests, says in three lines where Lambert is, what is green and today's test, then asks
  the review question: the glossary concept with the oldest date, to re-explain in two sentences,
  notes closed. Then it goes quiet.
- During: Lambert works in neovim and molten. The tutor speaks when spoken to, or at the twenty
  minute rung. A tangent ("why does Adam work?") gets two lines and a dated entry in `questions.md`,
  and the lesson goes on.
- The journal is written as the sitting goes (`~/notes/projets/ml/journal.md`, today's entry at the
  top, opened at the opening, completed at each event: green test, rung, tangent, review judged).
  A killed session loses nothing.
- Closing: Lambert says "stop", or today's test turns green. The tutor finishes the entry with a
  "Resume here" line, updates "Where I am" and the glossary dates, and commits ("Shipping"). No
  clock: Lambert stops when he stops (his decision, 6 November 2026).
- First sitting of the week: a five-line review replaces the review question: sittings, green
  tests, rungs per lesson, the oldest concept, the week's target.
- First sitting of the month: the blind rebuild (`rebuilds/README.md`).
- More than seven days without a sitting: a review sitting, two concepts to re-explain, the
  lesson's tests rerun, no new test that day.
- After a compaction, the tutor rereads today's entry before anything else.
- The sitting happens at the iMac; no remote control from the phone (Lambert's decision,
  6 November 2026).

## Talking to Lambert

- In English, always (his decision, 6 November 2026). The verdict first, short; the detail if it
  changes something.
- An explanation goes in this order and stops as soon as he says he has it: the picture, the
  three-number example, the formula. A derivation goes step by step, in LaTeX, naming the rule used,
  and stops before the last step so that he does it.
- An open (Socratic) question is asked in prose. A closed question (skip an exercise? write the
  next lesson? commit?) goes through AskUserQuestion, recommendation first.
- He is not an expert and often takes the recommendation as is: an argued disagreement serves him
  more than agreement, and a doubt is said as a doubt. A fact about PyTorch is checked in the docs
  (context7) before being stated; a fact about a method cites the paper.

## Shipping

- One commit per green test, made by the tutor (Lambert's decision, 6 November 2026), message
  `<lesson>: <what the green test proves> (<n>/<total>)`, plus the attribution lines Claude Code
  requires. `uv run ruff format` on what changed, before.
- One branch, `main`. No PRs, no CI: nothing here is production.
- Public repo: https://github.com/LambertDuclos/ml, Lambert's personal account (his decision,
  6 November 2026). The tutor pushes after each commit. This repo's pushes fetch that account's
  token from `gh` by name (a local `credential.helper` in `.git/config`), so they do not depend on
  which `gh` account is active on the machine.

## Writing code

- Identifiers and comments in English. A shape comment on every line that creates a tensor or
  changes its shape: `# (B, T, C)`. The tutor does not review code without them.
- A new dependency enters through `pyproject.toml` and a line here, outside a session.
- `ruff format`, line length 100. Python 3.14, the one in `.python-version`. The hooks stay on
  Python 3.9 and the standard library, like equipe's.

## Changing the method

In a session (`ML_SESSION=1`, set by `bin/ml session`), the guard refuses the tutor `CLAUDE.md`,
`.claude/`, `bin/`, `tests/`, `pyproject.toml` and `uv.lock`: it does not loosen its own rules on a
tired evening. A rule changes in an ordinary `claude` session, without an agent, or by hand.

## Where things are

- `courses/<track>/<nn-lesson>/`: `README.md` (video, "Assumes", sittings, what to write),
  `test_*.py` (the assignment), Lambert's implementation file, `explore.py` (molten scratch),
  `notes.md`, `exercises.md`, `ref/` if there was a rung 4. `courses/maths/`: the parallel track,
  one sitting a week. `courses/vision/`: the track after Zero to Hero. `courses/detours/`: prior
  knowledge backfilled on the way ("Gaps").
- `core/`: Lambert's mini-torch, promoted lesson after lesson, tested.
- `papers/<year>-<name>/`: `notes.md`, `repro.py`, `test_repro.py`, `questions.md`
  (`papers/README.md`).
- `rebuilds/<lesson>-<YYYY-MM>/`: the monthly rebuilds.
- `glossary.md`, `questions.md`: the two files that review and tangents feed.
- `HOWTO.md`: every command, from setup to debugging; the hands-on manual beside this contract.
- `.claude/agents/`: tutor (main session), examiner, critic. `.claude/hooks/guard.py` and its test
  `tests/test_guard.py`. `bin/ml`: `session`, `tests`.
- Outside the repo: `~/notes/projets/ml/` (the journal, the critic's reports).
