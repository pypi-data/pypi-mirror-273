import torch
import pytest
from smol_sae.base import Config
from smol_sae.rainbow import RainbowSAE
from smol_sae.utils import get_splits
from transformer_lens import HookedTransformer


@pytest.fixture
def device():
    # if torch.cuda.is_available():
    #     return "cuda"
    # elif torch.backends.mps.is_available():
    #     return "mps"
    # else:
    return "cpu"


@pytest.fixture
def model(device):
    return HookedTransformer.from_pretrained("gelu-1l").to(device)


@pytest.fixture
def config(device):
    return Config(
        n_buffers=2,
        expansion=2,
        in_batch=32,
        out_batch=32,
        buffer_size=2**8,
        sparsities=(0.1, 1.0),
        device=device,
    )


@pytest.fixture()
def sae(config, model):
    return RainbowSAE(config, model)


def test_vanilla_sae_forward(model, device, sae: RainbowSAE):
    n_batch = 2
    # test forward
    input = torch.randn(n_batch, sae.n_instances, model.cfg.d_model).to(device)
    output = sae(input)
    assert output.shape == input.shape


def test_vanilla_sae_patch_loss(model, device, sae: RainbowSAE):
    _, validation = get_splits()
    print(validation.shape)
    sae.patch_loss(model, validation)
