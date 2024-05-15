import random
from typing import Literal

State = Literal["S0", "S1", "SR"]
Emission = Literal["0", "1"]
Belief = Literal["nS", "n0", "n1", "n00", "n10", "n11", "n101"]

belief2idx: dict[Belief, int] = {
    "nS": 0,
    "n0": 1,
    "n1": 2,
    "n00": 3,
    "n10": 4,
    "n11": 5,
    "n101": 6,
}
idx2belief: dict[int, Belief] = {v: k for k, v in belief2idx.items()}

state2idx: dict[State, int] = {
    "S0": 0,
    "S1": 1,
    "SR": 2,
}
idx2state: dict[int, State] = {v: k for k, v in state2idx.items()}


def sample_sequence(length: int) -> list[tuple[Belief, State, Emission, Belief, State]]:
    """
    Returns a tuple of: (states, emissions, beliefs, next_states)
    """

    belief: Belief = "nS"
    state: State = random.choice(["S0", "S1", "SR"])

    data = []
    for _ in range(length):
        emission, next_belief, next_state = sample_next_hmm_data(belief, state)
        data.append((belief, state, emission, next_belief, next_state))
        state = next_state
        belief = next_belief
    return data


def tokenize(
    belief: Belief,
    state: State,
    emission: Emission,
    next_belief: Belief,
    next_state: State,
) -> tuple[int, int, int, int, int]:
    return (
        belief2idx[belief],
        state2idx[state],
        int(emission),
        belief2idx[next_belief],
        state2idx[next_state],
    )


def detokenize(
    belief: int, state: int, emission: int, next_belief: int, next_state: int
) -> tuple[Belief, State, Emission, Belief, State]:
    return (
        idx2belief[belief],
        idx2state[state],
        str(emission),  # type: ignore
        idx2belief[next_belief],
        idx2state[next_state],
    )


def sample_next_hmm_data(prev_belief: Belief, prev_state: State):
    """
    Input:
    - Belief state at time T-1 (after seeing emission)
    - State at time T

    Output:
    - Emission at time T
    - Belief state at time T
    - State at time T+1
    """

    # Randomly sample an emission
    next_emission = sample_next_emission(prev_state)
    # Compute the belief state
    next_belief = get_next_belief(prev_belief, next_emission)
    # Compute the next state
    next_state = get_next_state(prev_state, next_emission)

    return (next_emission, next_belief, next_state)


def sample_next_emission(state: State) -> Emission:
    if state == "S0":
        return "0"
    elif state == "S1":
        return "1"
    elif state == "SR":
        return "0" if random.random() < 0.5 else "1"
    raise RuntimeError("Should not reach here")


def get_next_state(prev_state: State, emission: Emission) -> State:
    # NOTE: it turns out that for this HMM, we don't need the emission.
    del emission
    if prev_state == "S0":
        return "S1"
    elif prev_state == "S1":
        return "SR"
    elif prev_state == "SR":
        return "S0"
    raise RuntimeError("Should not reach here")


def get_next_belief(prev_belief: Belief, emission: Emission) -> Belief:
    # Base case: first state
    if prev_belief == "nS":
        if emission == "0":
            return "n0"
        elif emission == "1":
            return "n1"
        else:
            raise ValueError(emission)
    # Base case: second state
    elif prev_belief == "n0":
        if emission == "0":
            return "n00"
        elif emission == "1":
            return "n101"
        else:
            raise ValueError(emission)
    elif prev_belief == "n1":
        if emission == "0":
            return "n10"
        elif emission == "1":
            return "n11"
        else:
            raise ValueError(emission)
    elif prev_belief == "n10":
        if emission == "0":
            return "n00"
        elif emission == "1":
            return "n101"
        else:
            raise ValueError(emission)
    # Inductive case
    elif prev_belief == "n00":
        return "n101"
    elif prev_belief == "n11":
        return "n00"
    elif prev_belief == "n101":
        return "n11"
    raise RuntimeError("Should not reach here")
