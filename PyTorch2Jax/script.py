import torch 
import numpy as np
import jax
import jax.numpy as jnp
from typing import Tuple

# No need to test this, assume it is correct
# Just a helper function for the apply_rotary_emb_torch function
def reshape_for_broadcast(freqs_cis: torch.Tensor, x: torch.Tensor):
    ndim = x.ndim
    assert 0 <= 1 < ndim
    assert freqs_cis.shape == (x.shape[1], x.shape[-1])
    shape = [d if i == 1 or i == ndim - 1 else 1 for i, d in enumerate(x.shape)]
    return freqs_cis.view(*shape)


"""
This file contains two functions: apply_rotary_emb_torch and apply_rotary_emb_jax.
The functions should be functionally equivalent.
"""


# This should be equivalent to the below function (apply_rotary_emb_jax)
def apply_rotary_emb_torch(
    xq: torch.Tensor,
    xk: torch.Tensor,
    freqs_cis: torch.Tensor,
) -> Tuple[torch.Tensor, torch.Tensor]:
    xq_ = torch.view_as_complex(xq.float().reshape(*xq.shape[:-1], -1, 2))
    xk_ = torch.view_as_complex(xk.float().reshape(*xk.shape[:-1], -1, 2))
    freqs_cis = reshape_for_broadcast(freqs_cis, xq_)
    xq_out = torch.view_as_real(xq_ * freqs_cis).flatten(3)
    xk_out = torch.view_as_real(xk_ * freqs_cis).flatten(3)
    return xq_out.type_as(xq), xk_out.type_as(xk)


# This should be equivalent to the above function (apply_rotary_emb_torch)
def apply_rotary_emb_jax(
    xq: jnp.ndarray,
    xk: jnp.ndarray,
    freqs_cis: jnp.ndarray,
    dtype: jnp.dtype=jnp.float32, # This is the return type. Generally we will use jnp.float32.
) -> Tuple[jnp.ndarray, jnp.ndarray]:
    reshape_xq = xq.astype(jnp.float32).reshape(*xq.shape[:-1], -1, 2)
    reshape_xk = xk.astype(jnp.float32).reshape(*xk.shape[:-1], -1, 2)

    xq_ = jax.lax.complex(reshape_xq[..., 0], reshape_xq[..., 1])
    xk_ = jax.lax.complex(reshape_xk[..., 0], reshape_xk[..., 1])

    # add head dim
    freqs_cis = jnp.reshape(freqs_cis, (*freqs_cis.shape[:2], 1, *freqs_cis.shape[2:]))

    xq_out = xq_ * freqs_cis
    xq_out = jnp.stack((jnp.real(xq_out), jnp.imag(xq_out)), axis=-1).reshape(*xq_out.shape[:-1], -1)

    xk_out = xk_ * freqs_cis
    xk_out = jnp.stack((jnp.real(xk_out), jnp.imag(xk_out)), axis=-1).reshape(*xk_out.shape[:-1], -1)

    return xq_out.astype(dtype), xk_out.astype(dtype)

"""
---- HELPER FUNCTIONS ----

The following helper functions are meant to help with test writing.
Note that you can use torch.from_numpy(ndarray) → Tensor to get a torch
tensor from a numpy array.
"""
def jnp_ndarray_to_torch(x: jnp.ndarray) -> torch.Tensor:
    return torch.from_numpy(x.astype(np.float32))


def torch_tensor_to_jnp(x: torch.Tensor) -> jnp.ndarray:
    return x.cpu().numpy().astype(np.float32)


