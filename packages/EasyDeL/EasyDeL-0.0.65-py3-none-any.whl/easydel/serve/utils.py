import chex
import fjformer.linen
import jax
from fjformer import make_shard_and_gather_fns, match_partition_rules, with_sharding_constraint
from typing import Optional, List, Callable, Any
from flax.core import freeze
from flax.traverse_util import unflatten_dict
from jax import numpy as jnp
from jax.experimental import mesh_utils
from pydantic import BaseModel
from fjformer.checkpoint import get_dtype
from gradio.themes.base import Base
from gradio.themes.utils import colors, fonts, sizes
from typing import Union

from transformers import GenerationConfig, LogitsProcessor

from ..modules.easydel_modelling_utils import EasyDeLFlaxPretrainedModel
from jax.sharding import PartitionSpec
from jax.experimental.pjit import pjit


class InstructRequest(BaseModel):
    instruction: str
    system: Optional[str] = None
    temperature: Optional[float] = None
    greedy: Optional[bool] = False


class ChatRequest(BaseModel):
    prompt: str
    system: Optional[str] = None
    history: Union[List[str], None] = None
    temperature: Optional[float] = None
    greedy: Optional[bool] = False


class Seafoam(Base):
    def __init__(
            self,
            *,
            primary_hue: Union[colors.Color, str] = colors.emerald,
            secondary_hue: Union[colors.Color, str] = colors.blue,
            neutral_hue: Union[colors.Color, str] = colors.gray,
            spacing_size: Union[sizes.Size, str] = sizes.spacing_md,
            radius_size: Union[sizes.Size, str] = sizes.radius_md,
            text_size: Union[sizes.Size, str] = sizes.text_lg,
            font: Union[fonts.Font, str]
            = (
                    fonts.GoogleFont("Quicksand"),
                    "ui-sans-serif",
                    "sans-serif",
            ),
            font_mono: Union[fonts.Font, str]
            = (
                    fonts.GoogleFont("IBM Plex Mono"),
                    "ui-monospace",
                    "monospace",
            ),
    ):
        """
        The __init__ function is called when the class is instantiated.
        It sets up the object with all of its instance variables and other things it needs to function properly.


        :param self: Represent the instance of the object
        :param *: Unpack the list of parameters into a tuple
        :param primary_hue: Union[colors.Color,str]: Set the primary color of the theme
        :param secondary_hue: Union[colors.Color,str]: Set the secondary color of the theme
        :param neutral_hue: Union[colors.Color,str]: Set the neutral color of the theme
        :param spacing_size: Union[sizes.Size,str]: Set the spacing size of the theme
        :param radius_size: Union[sizes.Size,str]: Set the radius of the buttons and other elements
        :param text_size: Union[sizes.Size,str]: Set the size of the text in the app

        :return: The class object

        """

        super().__init__(
            primary_hue=primary_hue,
            secondary_hue=secondary_hue,
            neutral_hue=neutral_hue,
            spacing_size=spacing_size,
            radius_size=radius_size,
            text_size=text_size,
            font=font,
            font_mono=font_mono,

        )
        super().set(
            body_background_fill="linear-gradient(90deg, *secondary_800, *neutral_900)",
            body_background_fill_dark="linear-gradient(90deg, *secondary_800, *neutral_900)",
            button_primary_background_fill="linear-gradient(90deg, *primary_300, *secondary_400)",
            button_primary_background_fill_hover="linear-gradient(90deg, *primary_200, *secondary_300)",
            button_primary_text_color="white",
            button_primary_background_fill_dark="linear-gradient(90deg, *primary_600, *secondary_800)",
            slider_color="*secondary_300",
            slider_color_dark="*secondary_400",
            block_title_text_weight="600",
            block_border_width="0px",
            block_shadow="*shadow_drop_lg",
            button_shadow="*shadow_drop_lg",
            button_large_padding="4px",
            border_color_primary="linear-gradient(90deg, *primary_600, *secondary_800)",
            border_color_primary_dark="linear-gradient(90deg, *primary_600, *secondary_800)",
            table_border_color="linear-gradient(90deg, *primary_600, *secondary_800)",
            table_border_color_dark="linear-gradient(90deg, *primary_600, *secondary_800)",
            button_primary_border_color="linear-gradient(90deg, *primary_600, *secondary_800)",
            button_primary_border_color_dark="linear-gradient(90deg, *primary_600, *secondary_800)",
            panel_border_color="linear-gradient(90deg, *primary_600, *secondary_800)",
            panel_border_color_dark="linear-gradient(90deg, *primary_600, *secondary_800)",
            block_border_color="linear-gradient(90deg, *primary_600, *secondary_800)",
            block_border_color_dark="linear-gradient(90deg, *primary_600, *secondary_800)"
        )


seafoam = Seafoam()


def get_partitions(tree):
    """Retrieve sharding specifications for model parameters."""
    if not isinstance(tree, fjformer.linen.LinearBitKernel):
        return getattr(tree.sharding, "spec", PartitionSpec(None))
    else:
        kernel_sharding = getattr(tree.kernel.sharding, "spec", PartitionSpec(None))
        scale_sharding = getattr(tree.scale.sharding, "spec", PartitionSpec(None))
        return fjformer.linen.LinearBitKernel(
            kernel=kernel_sharding,  # type:ignore
            scale=scale_sharding,  # type:ignore
        )


def shard_params(
        params,
        partition_rules,
        shard_mesh_shape=(1, -1, 1, 1),
        backend='gpu',
        shard_mesh=("dp", "fsdp", "tp", "sp"), do_unf=True,
        dtype='fp16'
):
    dtype = get_dtype(dtype)
    params = unflatten_dict(params) if do_unf else params
    params = freeze(params)
    mxd = jax.device_count(backend)
    rsp = jnp.asarray([1, mxd, 1]).reshape(shard_mesh_shape)
    phs_mesh = mesh_utils.create_device_mesh(rsp.tolist(), )
    mesh = jax.sharding.Mesh(phs_mesh, shard_mesh)
    ps = match_partition_rules(
        partition_rules,
        params
    )
    with mesh:
        shard_fns, _ = make_shard_and_gather_fns(
            ps, dtype
        )
        params = jax.tree_util.tree_map(lambda fn, x: fn(x), shard_fns, params)
    return params, mesh


def create_generate_function(
        model: EasyDeLFlaxPretrainedModel,
        generation_config: GenerationConfig,
        params: Union[dict, jax.tree_util.PyTreeDef],
        generation_partition_spec: PartitionSpec = PartitionSpec(("dp", "fsdp"), "sp"),
        output_partition_spec: PartitionSpec = PartitionSpec(("dp", "fsdp"), "sp"),
        logits_processor: Optional[LogitsProcessor] = None,
        return_prediction_only: bool = True
) -> Callable[[Union[dict, jax.tree_util.PyTreeDef], chex.Array, chex.Array], chex.Array]:
    """Create a sharded function for text generation using a Flax model.

        :param model :EasyDeLFlaxPretrainedModel: The Flax model used for text generation.
        :param generation_config :GenerationConfig: Configuration for text generation.
        :param params :dict or jax.tree_util.PyTreeDef: Parameters of the model or a PyTree representing the model's
            parameters.
        :param generation_partition_spec :PartitionSpec: Sharding specification for generation inputs. Defaults to
            PartitionSpec(("dp", "fsdp"), "sp").
        :param output_partition_spec: PartitionSpec: Sharding specification for output sequences. Defaults to
            PartitionSpec(("dp", "fsdp"), "sp").
        :param logits_processor :LogitsProcessor: Processor for model logits. Defaults to None.
        :param return_prediction_only :bool: Whether to return only the generated sequences. Defaults to True.

    :return :Callable[[Any, chex.Array, chex.Array], chex.Array]: Sharded function for text generation.

    """

    def generate_fn(
            parameters: Union[dict, jax.tree_util.PyTreeDef],
            input_ids: chex.Array,
            attention_mask: chex.Array
    ) -> chex.Array:
        """Generate text sequences using the provided model and parameters.

        :param parameters:Union[dict, jax.tree_util.PyTreeDef]: Model parameters.
        :param input_ids: chex.Array: Input token IDs.
        :param attention_mask:chex.Array: Attention mask.
        :return: Generated array sequences.
        """
        input_ids = with_sharding_constraint(
            input_ids,
            generation_partition_spec
        )
        attention_mask = with_sharding_constraint(
            attention_mask,
            generation_partition_spec
        )
        predict = model.generate(
            input_ids,
            attention_mask=attention_mask,
            params=parameters,
            generation_config=generation_config,
            logits_processor=logits_processor
        )
        return predict.sequences[:, input_ids.shape[1]:] if return_prediction_only else predict.sequences

    return pjit(
        generate_fn,
        in_shardings=(
            jax.tree_util.tree_map(get_partitions, params),
            generation_partition_spec,
            generation_partition_spec
        ),
        out_shardings=output_partition_spec
    )
