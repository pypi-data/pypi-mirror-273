from _typeshed import Incomplete
from enot.graph.transform_patterns.base import SubgraphTransformPattern
from enot.quantization.fake_quantized_model import FakeQuantizedModel
from torch import nn
from typing import Any

__all__ = ['TensorRTFakeQuantizedModel']

class TensorRTFakeQuantizedModel(FakeQuantizedModel):
    """
    Quantized TensorRT model class, which uses INT8 `convolutions`_ and `fully-connected layers`_.

    This class is used for quantization aware training.

    .. _convolutions: https://pytorch.org/docs/stable/generated/torch.nn.Conv2d.html
    .. _fully-connected layers: https://pytorch.org/docs/stable/generated/torch.nn.Linear.html
    .. _ONNX: https://github.com/onnx/onnx

    """
    def __init__(self, model: nn.Module, args: tuple = (), kwargs: dict[str, Any] | None = None, leaf_modules: list[type[nn.Module] | nn.Module] | None = None, quantization_scheme: str = 'default', use_weight_scale_factors: bool = False, use_bias_scale_factors: bool = True, quantize_add: bool = True, inplace: bool = False, **options) -> None:
        """
        Parameters
        ----------
        model : nn.Module
            Model from which :class:`TensorRTFakeQuantizedModel` will be constructed.
        args : Tuple
            Positional arguments for model.
        kwargs : Dict[str, Any]
            Keyword arguments for model.
        leaf_modules : list with types of modules or instances of torch.nn.Module, optional
            Types of modules or module instances that must be interpreted as leaf modules while tracing.
        quantization_scheme : str
            Specifies GPU architecture for which quantization will be optimized.
            Pass *pascal* to optimize for Pascal GPU architecture.
            Pass *default* to optimize for newer then Pascal GPU architecture.
            Also, try to use :func:`~enot.quantization.utils.optimal_quantization_scheme`
            to automatically select optimal quantization scheme.
        use_weight_scale_factors : bool
            Whether to use scale factors for weights tuning. Since additional memory consumption (x2
            times compared to off-mode) be careful to use. False by default.
        use_bias_scale_factors : bool
            Whether to use scale factors to train biases. True by default.
        quantize_add : bool
            Quantize add (+) or not. Default value is True.
        inplace : bool
            Enables inplace modification of input model (reduces memory consumption). False by default.

        """

class _TensorRTQuantizationPatternsBuilder:
    w_qtype: Incomplete
    act_qtype: Incomplete
    def __init__(self, use_weight_scale_factors: bool, use_bias_scale_factors: bool, quantization_scheme: str, quantize_add: bool) -> None: ...
    def build(self) -> list[list[SubgraphTransformPattern]]: ...
