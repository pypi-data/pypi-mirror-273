# belief-state-superposition
[![Github Actions](https://github.com/dtch1997/belief-state-superposition/actions/workflows/tests.yaml/badge.svg)]
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![pdm-managed](https://img.shields.io/badge/pdm-managed-blueviolet)](https://pdm-project.org)
[![Checked with pyright](https://microsoft.github.io/pyright/img/pyright_badge.svg)](https://microsoft.github.io/pyright/)

# Quickstart


## Install
```bash
pip install belief-state-superposition
```

## Usage

Generate and inspect data from a Hidden Markov Model

```python
from belief_state_superposition.hmm import sample_sequence

data = sample_sequence(16)
beliefs, states, emissions, next_beliefs, next_states = zip(*data)
print(beliefs)
print(states)
print(emissions)
```

Train a model on belief states

```python
import torch 
from torch.utils.data import DataLoader
from belief_state_superposition.model import init_model
from belief_state_superposition.data import get_dataset
from belief_state_superposition.train import train_model

device = "cuda" if torch.cuda.is_available() else "cpu"
train_dataset = get_dataset(1000)
train_data_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
model = init_model().to(device)
train_model(model, train_data_loader, n_epochs=10, show_progress_bar=True, device = device)
```


# Development

Refer to [Setup](docs/setup.md) for how to set up development environment.
