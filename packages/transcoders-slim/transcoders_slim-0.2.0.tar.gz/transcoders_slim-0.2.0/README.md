# transcoders-slim
![Github Actions](https://github.com/dtch1997/transcoders-slim/actions/workflows/tests.yaml/badge.svg)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![pdm-managed](https://img.shields.io/badge/pdm-managed-blueviolet)](https://pdm-project.org)
[![Checked with pyright](https://microsoft.github.io/pyright/img/pyright_badge.svg)](https://microsoft.github.io/pyright/)

# Quickstart


## Installation
```bash
pip install transcoders-slim
```
## Usage

Load pre-trained transcoders from Jacob Dunefsky's repository: https://github.com/jacobdunefsky/transcoder_circuits
```python
from transcoders.transcoder import Transcoder
from transcoders_slim.load_pretrained import load_pretrained
transcoders: dict[str, Transcoder] = load_pretrained()
for name, transcoder in transcoders.items():
    print(name, transcoder)
```

Run a transcoder: 
```
d_in = transcoder.d_in
d_tr = transcoder.d_sae
seq_len = 32
tr_in = torch.zeros(1, seq_len, d_in).to(transcoder.device)
tr_out, tr_hid = transcoder(tr_in)[:2]
```


# Development

Refer to [Setup](docs/setup.md) for how to set up development environment.
