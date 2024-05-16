llama_configs = {
    "3b": {
        "vocab_size": 32000,
        "hidden_size": 3200,
        "intermediate_size": 8640,
        "num_hidden_layers": 26,
        "num_attention_heads": 32,
        "num_key_value_heads": None,
        "max_position_embeddings": 2048,
        "initializer_range": 0.02,
        "rms_norm_eps": 1e-6,
        "use_cache": True,
        "tie_word_embeddings": False,
        "rope_scaling": None
    },
    "7b": {
        "vocab_size": 32000,
        "hidden_size": 4096,
        "intermediate_size": 11008,
        "num_hidden_layers": 32,
        "num_attention_heads": 32,
        "num_key_value_heads": None,
        "max_position_embeddings": 2048,
        "initializer_range": 0.02,
        "rms_norm_eps": 1e-6,
        "use_cache": True,
        "tie_word_embeddings": False,
        "rope_scaling": None
    },
    "13b": {
        "vocab_size": 32000,
        "hidden_size": 5120,
        "intermediate_size": 13824,
        "num_hidden_layers": 40,
        "num_attention_heads": 40,
        "num_key_value_heads": None,
        "max_position_embeddings": 2048,
        "initializer_range": 0.02,
        "rms_norm_eps": 1e-6,
        "use_cache": True,
        "tie_word_embeddings": False,
        "rope_scaling": None
    },
    "30b": {
        "vocab_size": 32000,
        "hidden_size": 6656,
        "intermediate_size": 17920,
        "num_hidden_layers": 60,
        "num_attention_heads": 52,
        "num_key_value_heads": None,
        "max_position_embeddings": 2048,
        "initializer_range": 0.02,
        "rms_norm_eps": 1e-6,
        "use_cache": True,
        "tie_word_embeddings": False,
        "rope_scaling": None
    },
    "65b": {
        "vocab_size": 32000,
        "hidden_size": 8192,
        "intermediate_size": 22016,
        "num_hidden_layers": 80,
        "num_attention_heads": 64,
        "num_key_value_heads": None,
        "max_position_embeddings": 2048,
        "initializer_range": 0.02,
        "rms_norm_eps": 1e-5,
        "use_cache": True,
        "tie_word_embeddings": False,
        "rope_scaling": None
    }
}

llama_2_configs = {

    "7b": {
        "vocab_size": 32000,
        "hidden_size": 4096,
        "intermediate_size": 11008,
        "num_hidden_layers": 32,
        "num_attention_heads": 32,
        "num_key_value_heads": None,
        "max_position_embeddings": 2048,
        "initializer_range": 0.02,
        "rms_norm_eps": 1e-5,
        "use_cache": True,
        "tie_word_embeddings": False,
        "rope_scaling": None
    },
    "13b": {
        "bos_token_id": 1,
        "eos_token_id": 2,
        "hidden_act": "silu",
        "hidden_size": 5120,
        "initializer_range": 0.02,
        "intermediate_size": 13824,
        "max_position_embeddings": 4096,
        "model_type": "llama",
        "num_attention_heads": 40,
        "num_hidden_layers": 40,
        "num_key_value_heads": None,
        "pretraining_tp": 1,
        "rms_norm_eps": 1e-05,
        "rope_scaling": None,
        "tie_word_embeddings": False,
        "use_cache": True,
        "vocab_size": 32000
    },
    "70b": {
        "bos_token_id": 1,
        "eos_token_id": 2,
        "hidden_act": "silu",
        "hidden_size": 8192,
        "initializer_range": 0.02,
        "intermediate_size": 28672,
        "max_position_embeddings": 4096,
        "num_attention_heads": 64,
        "num_hidden_layers": 80,
        "num_key_value_heads": 8,
        "pretraining_tp": 1,
        "rms_norm_eps": 1e-05,
        "rope_scaling": None,
        "tie_word_embeddings": False,
        "use_cache": True,
        "vocab_size": 32000
    }
}

mpt_configs = {
    "1b": {
        "alibi": True,
        "alibi_bias_max": 8,
        "attn_clip_qkv": None,
        "attn_impl": "torch",
        "attn_pdrop": 0,
        "attn_qk_ln": True,
        "attn_uses_sequence_id": False,
        "d_model": 2048,
        "emb_init_std": None,
        "emb_init_uniform_lim": None,
        "emb_pdrop": 0,
        "embedding_fraction": 1.0,
        "fan_mode": "fan_in",
        "init_device": "cpu",
        "init_div_is_residual": True,
        "init_gain": 0,
        "init_nonlinearity": "relu",
        "init_std": 0.02,
        "logit_scale": None,
        "low_precision_layernorm": True,
        "max_seq_len": 2048,
        "mlp_ratio": 4,
        "model_type": "mosaic_gpt",
        "n_heads": 16,
        "n_layers": 24,
        "no_bias": True,
        "param_init_fn": "kaiming_normal_",
        "prefix_lm": False,
        "resid_pdrop": 0,
        "softmax_scale": None,
        "tokenizer_name": "EleutherAI/gpt-neox-20b",
        "torch_dtype": "float16",
        "use_cache": False,
        "verbose": 0,
        "vocab_size": 50432
    },
    "7b": {
        "act_fn": "gelu",
        "alibi": True,
        "d_model": 4096,
        "emb_prob_drop": 0.0,
        "embedding_fraction": 1.0,
        "expansion_ratio": 4,
        "learned_pos_emb": True,
        "logit_scale": None,
        "max_seq_len": 2048,
        "model_type": "mpt",
        "n_heads": 32,
        "n_layers": 32,
        "no_bias": True,
        "qk_ln": False,
        "resid_prob_drop": 0.0,
        "use_bias": False,
        "use_cache": False,
        "use_lm_head": False,
        "use_norm_bias": False,
        "verbose": 0,
        "vocab_size": 50432
    },
    "30b": {
        "act_fn": "gelu",
        "alibi": True,
        "d_model": 7168,
        "emb_prob_drop": 0.0,
        "embedding_fraction": 1.0,
        "expansion_ratio": 4,
        "learned_pos_emb": True,
        "logit_scale": None,
        "max_seq_len": 8192,
        "model_type": "mpt",
        "n_heads": 64,
        "n_layers": 48,
        "no_bias": True,
        "qk_ln": False,
        "resid_prob_drop": 0.0,
        "use_bias": False,
        "use_cache": False,
        "use_lm_head": False,
        "use_norm_bias": False,
        "verbose": 0,
        "vocab_size": 50432
    }
}

gptj_configs = {
    "6b": {
        "vocab_size": 50400,
        "n_positions": 2048,
        "n_embd": 4096,
        "n_layer": 28,
        "n_head": 16,
        "rotary_dim": 64,
        "n_inner": None,
        "activation_function": "gelu_new",
        "layer_norm_epsilon": 1e-5,
        "initializer_range": 0.02,
        "scale_attn_weights": True,
        "use_cache": True,
        "bos_token_id": 50256,
        "eos_token_id": 50256,
        "tie_word_embeddings": False,
        "n_real_tokens": 50257,
    }
}

falcon_configs = {
    "7b": {
        "alibi": False,
        "apply_residual_connection_post_layernorm": False,
        "attention_dropout": 0.0,
        "bias": False,
        "bos_token_id": 11,
        "eos_token_id": 11,
        "hidden_dropout": 0.0,
        "hidden_size": 4544,
        "initializer_range": 0.02,
        "layer_norm_epsilon": 1e-05,
        "max_seq_len": 2048,
        "model_type": "falcon",
        "multi_query": True,
        "n_head": 71,
        "n_layer": 32,
        "parallel_attn": True,
        "use_cache": False,
        "vocab_size": 65024
    },
    "40b": {
        "bias": False,
        "bos_token_id": 11,
        "eos_token_id": 11,
        "hidden_dropout": 0.0,
        "hidden_size": 8192,
        "initializer_range": 0.02,
        "layer_norm_epsilon": 1e-05,
        "model_type": "RefinedWeb",
        "n_head": 128,
        "n_head_kv": 8,
        "n_layer": 60,
        "parallel_attn": True,
        "torch_dtype": "bfloat16",
        "use_cache": True,
        "vocab_size": 65024
    }
}

opt_configs = {
    "1.3b": {

        "activation_dropout": 0.0,
        "activation_function": "relu",
        "attention_dropout": 0.0,
        "bos_token_id": 2,
        "do_layer_norm_before": True,
        "dropout": 0.1,
        "eos_token_id": 2,
        "ffn_dim": 8192,
        "hidden_size": 2048,
        "init_std": 0.02,
        "layerdrop": 0.0,
        "max_position_embeddings": 2048,
        "model_type": "opt",
        "num_attention_heads": 32,
        "num_hidden_layers": 24,
        "pad_token_id": 1,
        "prefix": "</s>",
        "use_cache": True,
        "vocab_size": 50272,
        "word_embed_proj_dim": 2048

    },
    "6.7b": {
        "_remove_final_layer_norm": False,
        "activation_dropout": 0.0,
        "activation_function": "relu",
        "attention_dropout": 0.0,
        "bos_token_id": 2,
        "do_layer_norm_before": True,
        "dropout": 0.1,
        "eos_token_id": 2,
        "ffn_dim": 16384,
        "hidden_size": 4096,
        "init_std": 0.02,
        "layerdrop": 0.0,
        "max_position_embeddings": 2048,
        "model_type": "opt",
        "num_attention_heads": 32,
        "num_hidden_layers": 32,
        "pad_token_id": 1,
        "prefix": "</s>",
        "use_cache": True,
        "vocab_size": 50272,
        "word_embed_proj_dim": 4096
    },
    "66b": {
        "_remove_final_layer_norm": False,
        "activation_dropout": 0.0,
        "activation_function": "relu",
        "attention_dropout": 0.0,
        "bos_token_id": 2,
        "do_layer_norm_before": True,
        "dropout": 0.1,
        "eos_token_id": 2,
        "ffn_dim": 36864,
        "hidden_size": 9216,
        "init_std": 0.02,
        "layerdrop": 0.0,
        "max_position_embeddings": 2048,
        "model_type": "opt",
        "num_attention_heads": 72,
        "num_hidden_layers": 64,
        "pad_token_id": 1,
        "prefix": "</s>",
        "use_cache": True,
        "vocab_size": 50272,
        "word_embed_proj_dim": 9216
    },
    "13b": {
        "_name_or_path": "facebook/opt-13b",
        "_remove_final_layer_norm": False,
        "activation_dropout": 0.0,
        "activation_function": "relu",
        "attention_dropout": 0.0,
        "bos_token_id": 2,
        "do_layer_norm_before": True,
        "dropout": 0.1,
        "eos_token_id": 2,
        "ffn_dim": 20480,
        "hidden_size": 5120,
        "init_std": 0.02,
        "layerdrop": 0.0,
        "max_position_embeddings": 2048,
        "model_type": "opt",
        "num_attention_heads": 40,
        "num_hidden_layers": 40,
        "output_projection": True,
        "pad_token_id": 1,
        "prefix": "</s>",
        "use_cache": True,
        "vocab_size": 50272,
        "word_embed_proj_dim": 5120
    },
    "350m": {
        "activation_dropout": 0.0,
        "activation_function": "relu",
        "attention_dropout": 0.0,
        "bos_token_id": 2,
        "do_layer_norm_before": False,
        "dropout": 0.1,
        "eos_token_id": 2,
        "ffn_dim": 4096,
        "hidden_size": 1024,
        "init_std": 0.02,
        "layerdrop": 0.0,
        "max_position_embeddings": 2048,
        "model_type": "opt",
        "num_attention_heads": 16,
        "num_hidden_layers": 24,
        "pad_token_id": 1,
        "prefix": "</s>",
        "use_cache": True,
        "vocab_size": 50272,
        "word_embed_proj_dim": 512

    }
}


def get_config(model_type: str, struct: str):
    """
    The get_config function takes in a model_type and struct, and returns the corresponding config.

    :param model_type: str: Determine which model to use
    :param struct: str: Specify the structure of the model
    :return: A dictionary of hyperparameters
    
    """
    if model_type == "llama":
        return llama_configs[struct]
    elif model_type == "llama2":
        return llama_2_configs[struct]
    elif model_type == "opt":
        return opt_configs[struct]
    elif model_type == "gptj":
        return gptj_configs[struct]
    elif model_type == "falcon":
        return falcon_configs[struct]
    elif model_type == "mpt":
        return mpt_configs[struct]
    else:
        raise ValueError(f"Unknown ModelType : {model_type}")
