import torch
from torch.utils.data import Dataset, TensorDataset
from belief_state_superposition.hmm import sample_sequence, tokenize, detokenize


def get_dataset(
    n_samples: int,
    seq_len: int = 16,
) -> Dataset:
    """Return a dataset of HMM data"""

    beliefss = []
    statess = []
    emissionss = []
    next_beliefss = []
    next_statess = []

    for _ in range(n_samples):
        data = sample_sequence(seq_len)
        # Tokenizer
        tokenized_data = [tokenize(*d) for d in data]
        beliefs, states, emissions, next_beliefs, next_states = zip(*tokenized_data)

        beliefss.append(beliefs)
        statess.append(states)
        emissionss.append(emissions)
        next_beliefss.append(next_beliefs)
        next_statess.append(next_states)

    return TensorDataset(
        torch.tensor(beliefss),
        torch.tensor(statess),
        torch.tensor(emissionss),
        torch.tensor(next_beliefss),
        torch.tensor(next_statess),
    )


if __name__ == "__main__":
    dataset = get_dataset(10)
    print(len(dataset))  # type: ignore
    print(dataset[0])
    print(dataset[0][0].shape)
    print(dataset[0][1].shape)
    print(dataset[0][2].shape)
    print(dataset[0][3].shape)
    print(dataset[0][4].shape)

    for b, s, e, nb, ns in dataset:
        for i in range(16):
            print(
                detokenize(
                    b[i].item(), s[i].item(), e[i].item(), nb[i].item(), ns[i].item()
                )
            )
        break
