from _typeshed import Incomplete
from enot.graph.transform_patterns.base import SubgraphTransformPattern
from enot.quantization.fake_quantized_model import FakeQuantizedModel
from torch import nn
from typing import Any

__all__ = ['OpenVINOFakeQuantizedModel']

class OpenVINOFakeQuantizedModel(FakeQuantizedModel):
    """
    Quantized OpenVINO model class, which uses INT8 `convolutions`_ and `fully-connected layers`_.

    This class is used for quantization aware training.

    .. _convolutions: https://pytorch.org/docs/stable/generated/torch.nn.Conv2d.html
    .. _fully-connected layers: https://pytorch.org/docs/stable/generated/torch.nn.Linear.html
    .. _ONNX: https://github.com/onnx/onnx

    """
    def __init__(self, model: nn.Module, args: tuple = (), kwargs: dict[str, Any] | None = None, leaf_modules: list[type[nn.Module] | nn.Module] | None = None, apply_avx2_fix: bool = False, use_weight_scale_factors: bool = False, use_bias_scale_factors: bool = True, inplace: bool = False, **options) -> None:
        """
        Parameters
        ----------
        model : nn.Module
            Model from which :class:`OpenVINOFakeQuantizedModel` will be constructed.
        args : Tuple
            Positional arguments for model.
        kwargs : Dict[str, Any]
            Keyword arguments for model.
        leaf_modules : list with types of modules or instances of torch.nn.Module, optional
            Types of modules or module instances that must be interpreted as leaf modules while tracing.
        apply_avx2_fix : bool
            Whether to fix quantization parameters for AVX-2 kernels, or do not apply fix and maximize
            metric for AVX-512 kernels. Without fix we cannot guarantee stable result, because OpenVINO
            can mix kernels (AVX-512, AVX-2) on host with AVX-512 instructions. False by default. Please do
            not change this option, if you do not know what you are doing.
        use_weight_scale_factors : bool
            Whether to use scale factors for weights tuning. Since additional memory consumption (x2
            times compared to off-mode) be careful to use. False by default.
        use_bias_scale_factors : bool
            Whether to use scale factors to train biases. True by default.
        inplace : bool
            Enables inplace modification of input model (reduces memory consumption). False by default.

        """

class _OpenVINOQuantizationPatternsBuilder:
    w_qtype: Incomplete
    act_qtype: Incomplete
    def __init__(self, apply_avx2_fix: bool, use_weight_scale_factors: bool, use_bias_scale_factors: bool) -> None: ...
    def build(self) -> list[list[SubgraphTransformPattern]]: ...
