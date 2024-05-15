# ruff: noqa: F722
import torch
from tqdm import trange
from torch.optim import Adam
from torch.utils.data import DataLoader
from eindex import eindex
from jaxtyping import Float, Int

from belief_state_superposition.model import init_model
from belief_state_superposition.data import get_dataset


def loss_fn(
    logits: Float[torch.Tensor, "n_batch n_seq n_dim"],
    next_tokens: Int[torch.Tensor, "n_batch n_seq"],
) -> Float[torch.Tensor, "n_batch n_seq"]:
    """
    Calculate the negative log-likelihood loss for given logits and next-tokens.
    """
    log_probs = logits.log_softmax(dim=-1)
    correct_log_probs = eindex(log_probs, next_tokens, "batch seq [batch seq]")
    return -correct_log_probs


def train_model(
    model: torch.nn.Module,
    train_data_loader: DataLoader,
    n_epochs: int = 100,
    learning_rate: float = 1e-3,
    show_progress_bar: bool = False,
    device: str = "cpu",
) -> list[float]:
    optim = Adam(model.parameters(), lr=learning_rate, weight_decay=1e-5)
    model.train()

    losses = []
    epochs = trange(n_epochs, desc="Training", disable=not show_progress_bar)
    for epoch in epochs:
        loss = 0
        for batch in train_data_loader:
            _, _, emissions, _, _ = batch
            emissions = emissions.to(device)
            logits = model(emissions)

            # Note: handle token shift
            curr_logits = logits[:, :-1]
            next_tokens = emissions[:, 1:]
            loss = loss_fn(curr_logits, next_tokens).mean()

            # Optimize
            model.zero_grad()
            loss.backward()
            optim.step()
            losses.append(loss.item())
            loss = loss.item()

        epochs.set_description(f"train_loss: {loss:.3f}", refresh=True)
    return losses


if __name__ == "__main__":
    device = "cuda" if torch.cuda.is_available() else "cpu"
    train_dataset = get_dataset(1000)
    train_data_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
    model = init_model().to(device)
    train_model(
        model, train_data_loader, n_epochs=10, show_progress_bar=True, device=device
    )
