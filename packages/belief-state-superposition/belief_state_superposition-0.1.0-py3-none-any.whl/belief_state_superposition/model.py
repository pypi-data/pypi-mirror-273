import transformer_lens as tl


def init_model(
    n_layers: int = 2,
    seed: int = 0,
    d_model: int = 512,
    n_heads: int = 8,
):
    model_config = tl.HookedTransformerConfig(
        n_layers=n_layers,
        d_model=d_model,
        d_head=d_model // n_heads,
        n_heads=n_heads,
        d_mlp=256,
        d_vocab=2,
        n_ctx=16,
        normalization_type="LN",
        act_fn="relu",
        # attn_only=True,
        init_weights=True,
        device="cuda",
        # positional_embedding_type='rotary',
        seed=seed,
    )
    model = tl.HookedTransformer(model_config)
    return model
