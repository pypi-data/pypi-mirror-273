import torch
from smol_sae.base import Config
from smol_sae.vanilla import VanillaSAE
from transformer_lens import HookedTransformer

device = "cuda" if torch.cuda.is_available() else "cpu"
config = Config(
    n_buffers=100, expansion=4, buffer_size=2**8, sparsities=(0.1, 1.0), device=device
)

model = HookedTransformer.from_pretrained("gelu-1l").to(device)
sae = VanillaSAE(config, model)
n_batch = 32
sae_input = torch.randn(n_batch, sae.n_instances, model.cfg.d_model).to(device)
sae_output = sae(sae_input)
