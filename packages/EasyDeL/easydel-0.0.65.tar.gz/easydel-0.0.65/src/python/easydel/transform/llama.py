import gc
from pathlib import Path

from jax import numpy as jnp
import jax
import torch
from transformers import LlamaForCausalLM
from ..modules.llama import LlamaConfig
from fjformer import load_and_convert_checkpoint_to_torch


def inverse_permute(w, num_attention_heads, in_dim, out_dim):
    reshaped_w = w.reshape(num_attention_heads, 2, in_dim // num_attention_heads // 2, out_dim)
    transposed_w = reshaped_w.transpose(0, 2, 1, 3)
    inverted_w = transposed_w.reshape(in_dim, out_dim)
    return inverted_w


def match_keywords(string, ts, ns):
    for t in ts:
        if t not in string:
            return False
    for n in ns:
        if n in string:
            return False
    return True


def llama_convert_hf_to_flax_load(checkpoints_dir, config: LlamaConfig,
                                  device):
    ckpt_paths = sorted(Path(checkpoints_dir).glob("*.bin"))
    state_dict = {}
    with jax.default_device(device):
        for i, checkpoint_path in enumerate(ckpt_paths):
            checkpoint = torch.load(checkpoint_path, map_location="cpu")
            for k, v in checkpoint.items():
                state_dict[k] = v

        jax_weights = llama_convert_hf_to_flax(state_dict, config, device)

        return jax_weights


def llama_convert_hf_to_flax(state_dict, config: LlamaConfig,
                             device):
    with jax.default_device(device):
        jax_weights = {
            "model": {
                "embed_tokens": {"embedding": state_dict["model.embed_tokens.weight"].cpu().numpy()},
                "norm": {"kernel": state_dict["model.norm.weight"].cpu().numpy()},
                "layers": {
                    f"{layer}": {
                        "self_attn": {
                            "q_proj": {
                                "kernel": state_dict[
                                    f"model.layers.{layer}.self_attn.q_proj.weight"].cpu().numpy().transpose()
                            },
                            "k_proj": {
                                "kernel": state_dict[
                                    f"model.layers.{layer}.self_attn.k_proj.weight"].cpu().numpy().transpose()
                            },
                            "v_proj": {
                                "kernel": state_dict[
                                    f"model.layers.{layer}.self_attn.v_proj.weight"].cpu().numpy().transpose()
                            },
                            "o_proj": {
                                "kernel": state_dict[
                                    f"model.layers.{layer}.self_attn.o_proj.weight"].cpu().numpy().transpose()
                            },
                        },
                        "mlp": {
                            "gate_proj": {
                                "kernel": state_dict[f"model.layers.{layer}.mlp.gate_proj.weight"]
                                .cpu().numpy()
                                .transpose()
                            },
                            "down_proj": {
                                "kernel": state_dict[f"model.layers.{layer}.mlp.down_proj.weight"]
                                .cpu().numpy()
                                .transpose()
                            },
                            "up_proj": {
                                "kernel": state_dict[f"model.layers.{layer}.mlp.up_proj.weight"]
                                .cpu().numpy()
                                .transpose()
                            },
                        },
                        "input_layernorm": {
                            "kernel": state_dict[f"model.layers.{layer}.input_layernorm.weight"].cpu().numpy()
                        },
                        "post_attention_layernorm": {
                            "kernel": state_dict[
                                f"model.layers.{layer}.post_attention_layernorm.weight"
                            ].cpu().numpy()
                        },
                    }
                    for layer in range(config.num_hidden_layers)
                },
            },
            "lm_head": {"kernel": state_dict["lm_head.weight"].cpu().numpy().transpose()},
        }

        return jax_weights


def llama_convert_flax_to_pt(flax_params, config: LlamaConfig, dtype=jnp.float16):
    torch_params = {}
    for key, tensor in flax_params.items():
        if match_keywords(key, ['kernel'], ['none']):
            tensor = tensor.T
        torch_params[key] = torch.from_numpy(tensor.astype(dtype=dtype))

    state_dict = {}
    inv_freq = 1.0 / (10000.0 ** (torch.arange(0, config.hidden_size // config.num_attention_heads, 2).float() / (
            config.hidden_size // config.num_attention_heads)))
    for layer_i in range(config.num_hidden_layers):
        state_dict.update({
            f"model.layers.{layer_i}.self_attn.q_proj.weight": torch_params[
                f"model.layers.{layer_i}.self_attn.q_proj.kernel"],
            f"model.layers.{layer_i}.self_attn.k_proj.weight": torch_params[
                f"model.layers.{layer_i}.self_attn.k_proj.kernel"],
            f"model.layers.{layer_i}.self_attn.v_proj.weight": torch_params[
                f"model.layers.{layer_i}.self_attn.v_proj.kernel"],
            f"model.layers.{layer_i}.self_attn.o_proj.weight": torch_params[
                f"model.layers.{layer_i}.self_attn.o_proj.kernel"],

            f"model.layers.{layer_i}.mlp.gate_proj.weight": torch_params[
                f"model.layers.{layer_i}.mlp.gate_proj.kernel"],
            f"model.layers.{layer_i}.mlp.down_proj.weight": torch_params[
                f"model.layers.{layer_i}.mlp.down_proj.kernel"],
            f"model.layers.{layer_i}.mlp.up_proj.weight": torch_params[
                f"model.layers.{layer_i}.mlp.up_proj.kernel"],

            f"model.layers.{layer_i}.input_layernorm.weight": torch_params[
                f"model.layers.{layer_i}.input_layernorm.kernel"],
            f"model.layers.{layer_i}.post_attention_layernorm.weight": torch_params[
                f"model.layers.{layer_i}.post_attention_layernorm.kernel"],
            f"model.layers.{layer_i}.self_attn.rotary_emb.inv_freq": inv_freq

        })

    state_dict.update({
        "model.embed_tokens.weight": torch_params["model.embed_tokens.embedding"],
        "model.norm.weight": torch_params["model.norm.kernel"],
        "lm_head.weight": torch_params["lm_head.kernel"],
    })
    return state_dict


def llama_easydel_to_hf(path, config: LlamaConfig):
    """
        Takes path to easydel saved ckpt and return the model in pytorch (Transformers Huggingface)
    """
    torch_params = load_and_convert_checkpoint_to_torch(path)
    edited_params = {}
    for k, v in torch_params.items():
        edited_params[k.replace('.kernel', '.weight').replace('.embedding', '.weight')] = v
    model = LlamaForCausalLM(config=config)
    model.load_state_dict(edited_params)
    return model


def llama_from_pretrained(model_id, device):
    """
    return: Weight or Params for easydel Model , Config
    """
    config = LlamaConfig.from_pretrained(model_id)
    model = LlamaForCausalLM.from_pretrained(model_id)
    easydel_wights = llama_convert_hf_to_flax(
        state_dict=model.state_dict(),
        config=config,
        device=device
    )
    config.add_jax_args()

    del model
    gc.collect()
    return easydel_wights, config
