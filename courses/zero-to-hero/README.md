# Zero to Hero

Andrej Karpathy, *Neural Networks: Zero to Hero*: https://karpathy.ai/zero-to-hero.html (the
YouTube playlist is linked there). One folder per lecture. A folder appears when I reach it: the
tutor writes its `README.md`, its `test_*.py` and its plumbing at the end of the previous lesson.

| # | Folder | Lecture | What I build |
|---|---|---|---|
| 00 | `00-tensors-and-derivatives` | prerequisite, no lecture | broadcasting, matmul, numerical derivatives, the chain rule, softmax and cross-entropy |
| 01 | `01-micrograd` | The spelled-out intro to neural networks and backpropagation: building micrograd | a scalar autograd engine and an MLP trained with it |
| 02 | `02-makemore-bigram` | The spelled-out intro to language modeling: building makemore | a bigram character model, by counting, then as a one-layer net |
| 03 | `03-makemore-mlp` | Building makemore Part 2: MLP | Bengio et al. 2003: embeddings and a hidden layer (first entry in `papers/`) |
| 04 | `04-activations-batchnorm` | Part 3: Activations & Gradients, BatchNorm | initialisation, saturation, batch norm, the diagnostic plots |
| 05 | `05-backprop-ninja` | Part 4: Becoming a Backprop Ninja | the whole backward pass by hand through the MLP and batch norm |
| 06 | `06-wavenet` | Part 5: Building a WaveNet | hierarchical (dilated) layers; torch.nn-like modules promoted to `core/` |
| 07 | `07-gpt` | Let's build GPT: from scratch, in code, spelled out | self-attention, the transformer block, a character-level GPT |
| 08 | `08-tokenizer` | Let's build the GPT Tokenizer | byte-pair encoding, compared with tiktoken |
| 09 | `09-gpt2-124m` | Let's reproduce GPT-2 (124M) | the full training run; needs a rented GPU |

Each folder: `README.md` (segments, sittings, what to write), `test_<lesson>.py` (the assignment),
`<lesson>.py` (mine), `explore.py` (my scratch cells, run with molten), `notes.md` (mine, at the
end), `exercises.md` (the examiner's), `ref/` (only if I asked for a solution).
