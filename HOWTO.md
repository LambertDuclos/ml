# How to work in this repo

Every command, in one place. The method (who writes what, the ladder, the session protocol) is in
`CLAUDE.md`; this file is the hands-on manual.

## 1. One-time setup

Done on the iMac on 6 November 2026. For another machine:

```sh
brew install graphviz imagemagick            # expression graphs; inline images in neovim
git clone https://github.com/LambertDuclos/ml.git ~/ml && cd ~/ml
uv sync                                       # Python 3.14 + torch, numpy, matplotlib, sympy, pytest, ipykernel, debugpy, ruff
uv run python -m ipykernel install --user --name ml --display-name "ml (uv, torch)"   # the kernel molten and Jupyter use
uv run pytest                                 # everything red except tests/ (the guard): expected before any lesson is done
```

Neovim side (molten needs its own Python host, separate from the project):

```sh
uv venv ~/.virtualenvs/neovim --python 3.12
uv pip install --python ~/.virtualenvs/neovim/bin/python pynvim jupyter_client
nvim --headless "+Lazy load molten-nvim" "+UpdateRemotePlugins" "+qa"
```

GitHub, personal account, without touching the work account that stays active in `gh`:

```sh
gh auth login                                                   # once, the LambertDuclos account
gh auth switch -u lambertBiteSize                               # work account back to active
git config user.name "Lambert Duclos-de Guise"                  # in ~/ml
git config user.email "lambertddg@gmail.com"
git config --local --replace-all credential.helper ''
git config --local --add credential.helper '!f() { echo "username=LambertDuclos"; echo "password=$(gh auth token -u LambertDuclos)"; }; f'
```

Optional, to type `ml session` from anywhere (fish): `fish_add_path ~/ml/bin`. Otherwise `bin/ml` from the repo.

## 2. Every sitting: three tmux panes, started from the lesson folder

```sh
cd ~/ml/courses/zero-to-hero/00-tensors-and-derivatives     # the current lesson

# pane 1
nvim test_tensors.py tensors.py explore.py
# pane 2
uv run pytest . -q
# pane 3
~/ml/bin/ml session
```

Starting from the lesson folder matters: `uv` still finds the project, pytest runs only that
lesson, and imports in `explore.py` resolve.

## 3. The sitting, tool by tool

1. **Pane 3.** The tutor reads the journal, runs the lesson's tests, names today's test, asks the
   review question. Answer it in two sentences, notes closed.
2. **Pane 1.** Read today's test and its docstring in `test_*.py`: it is the spec, the function
   name, the arguments, what must hold.
3. **Watch the segment** listed in the lesson's `README.md`. Type along in `explore.py` with molten
   (section 5), one paragraph per cell. Poke at numbers, print shapes, plot.
4. **Close the video. Write the implementation file** (`tensors.py`, `micrograd.py`…) in neovim,
   plain editing, no copy-paste. That file is the only code that counts.
5. **Pane 2.** Rerun pytest. Red says what to fix; green is the sitting done.
6. **Stuck?** Pane 3, one of the four words below.
7. **Done or tired?** Say "stop". The tutor writes "Resume here" in the journal, updates the README
   and the glossary, formats, commits and pushes. You do nothing mechanical.

### The four words

| Word | Means |
|---|---|
| `gap` | I don't know something the lesson assumes. Costs nothing on the ladder; explained on the spot or turned into a detour. |
| `rung` | Next rung of the ladder on the lesson's mechanism: question → concept → pseudocode. |
| `solution` | Rung 4: a reference in `ref/`, never in my file. Logged. Next sitting opens by rebuilding it blind. |
| `stop` | End the sitting. |

## 4. Tests

```sh
uv run pytest                                              # whole repo (from the root)
uv run pytest courses/zero-to-hero/01-micrograd -q         # one lesson
uv run pytest . -q                                         # the lesson I am in
uv run pytest . -q -k test_backward_neuron                 # one test
uv run pytest . -q -x                                      # stop at the first red
bin/ml tests [args]                                        # same as uv run pytest, from anywhere in the repo
```

A new lesson's tests are proven by the tutor against a throwaway reference before I see them
(`CLAUDE.md`, "Gates"). Red with `ModuleNotFoundError: No module named 'tensors'` means I have not
created the file yet: normal at the start of a lesson.

## 5. Molten (scratch cells inside neovim)

Cells are paragraphs separated by a blank line, in `explore.py`.

| Key | Does |
|---|---|
| `<leader>mi` | start a kernel: pick `ml (uv, torch)` |
| `<leader>mvip` | run the paragraph under the cursor |
| `<leader>me` | run the current line, or the visual selection |
| `<leader>mo` / `<leader>mh` | enter the output window / hide it |
| `<leader>mr` | rerun the cell under the cursor |
| `<leader>mR` | restart the kernel |

Matplotlib figures appear inline under the cell (image.nvim, kitty graphics protocol, Ghostty).
Imports like `from micrograd import Value` work because neovim was started in the lesson folder.

## 6. Debugging

Put `breakpoint()` inside the function, run the test with capture off:

```sh
uv run pytest . -q -s -k test_backward_neuron
```

In pdb: `n` next line, `s` step into, `p x1.grad` print, `l` where am I, `c` continue, `q` quit.
`uv run pytest . -q --pdb` drops into pdb at the first failure instead. The editor way,
`nvim-dap-python` with `debugpy` from the project, works too.

## 7. Git and GitHub

The tutor commits after each green test and pushes, with the personal identity and the credential
helper from section 1. By hand, if ever needed:

```sh
git status
git log --oneline
git add -A && git commit -m "01-micrograd: backward on a single neuron (2/5)"
git push
```

Remote: `https://github.com/LambertDuclos/ml.git`, branch `main`, public. Pushes authenticate as
LambertDuclos whatever account `gh` has active (`gh auth status` shows them).

## 8. Where things live

| What | Where |
|---|---|
| The contract and the session protocol | `CLAUDE.md` |
| This manual | `HOWTO.md` |
| Lessons | `courses/zero-to-hero/<nn-lesson>/`, `courses/maths/`, later `courses/vision/`, detours in `courses/detours/` |
| My library | `core/` |
| Papers | `papers/<year>-<name>/` |
| Monthly blind rebuilds | `rebuilds/<lesson>-<YYYY-MM>/` |
| Concepts, questions | `glossary.md`, `questions.md` |
| Journal, critic reports | `~/notes/projets/ml/` (outside the repo) |
| Datasets | `data/` (ignored by git, downloaded by each lesson's `data.py`) |
| Tutor, examiner, critic | `.claude/agents/` |
| The guard and its tests | `.claude/hooks/guard.py`, `tests/test_guard.py` |

## 9. The monthly blind rebuild

First sitting of the month. The tutor names the lesson.

```sh
mkdir -p ~/ml/rebuilds/01-micrograd-2026-12
cp ~/ml/courses/zero-to-hero/01-micrograd/test_micrograd.py ~/ml/rebuilds/01-micrograd-2026-12/
cd ~/ml/rebuilds/01-micrograd-2026-12 && nvim micrograd.py      # thirty minutes, notes and original closed
uv run pytest . -q
```

## 10. Changing the method

Rules live in `CLAUDE.md`, the agents and the guard. During a sitting (`bin/ml session`) they are
closed to the tutor on purpose. To change one, open a plain session in the repo and ask:

```sh
cd ~/ml && claude
```

A new dependency enters the same way: `uv add <package>` (or `uv add --dev`), plus a line in
`CLAUDE.md`, "Writing code".

## 11. Troubleshooting

| Symptom | Do |
|---|---|
| `ml: command not found` | `bin/ml …` from the repo, or `fish_add_path ~/ml/bin` |
| Molten: no `ml` kernel in the list | rerun the `ipykernel install` line of section 1 |
| Molten: `<leader>mi` does nothing or errors about the host | section 1, neovim side: the host venv and `UpdateRemotePlugins`; then `:checkhealth provider` |
| Molten: text works, images do not | `tmux show -g allow-passthrough` must say `all`; Ghostty or kitty as terminal; `image.nvim` backend `kitty`. Fallback: `uv add --dev jupyterlab` in a plain session, then `uv run jupyter lab` in the browser with the same `ml` kernel |
| "ml guard: … belongs to Lambert" in the tutor's output | the guard refused Claude a write on my file: expected, that file is mine to write |
| "ml guard: … is the method, closed during a session" | a rule change was attempted during a sitting: do it in a plain `claude` session (section 10) |
| `git push` asks for a password | `gh auth status`; if LambertDuclos is missing, `gh auth login`, then `gh auth switch -u lambertBiteSize` |
| Tests import the wrong module after a rebuild | run pytest from inside the folder you mean; rebuilds are excluded from the root run on purpose |
