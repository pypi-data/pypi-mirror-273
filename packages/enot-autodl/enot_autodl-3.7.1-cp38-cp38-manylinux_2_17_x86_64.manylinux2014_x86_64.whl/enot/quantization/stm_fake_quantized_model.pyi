from _typeshed import Incomplete
from enot.graph.transform_patterns.base import SubgraphTransformPattern
from enot.quantization.fake_quantized_model import FakeQuantizedModel
from torch import nn
from typing import Any

__all__ = ['STMFakeQuantizedModel']

class STMFakeQuantizedModel(FakeQuantizedModel):
    """
    Fake quantization model for STM devices.

    ONNXSim and ONNXRuntime (basic level) optimizations MUST be applied to exported ONNX.
    Scale factors are disabled by default.

    Examples
    --------
    >>> import onnx
    >>> import onnxruntime as rt
    >>> import onnxsim
    >>>
    >>> fq_model = STMFakeQuantizedModel(...)
    >>> ...
    >>> torch.onnx.export(...)
    >>>
    >>> model, _ = onnxsim.simplify(model=ONNX_NAME)
    >>> onnx.save(model, ONNX_NAME)
    >>>
    >>> sess_options = rt.SessionOptions()
    >>> sess_options.graph_optimization_level = rt.GraphOptimizationLevel.ORT_ENABLE_BASIC
    >>> sess_options.optimized_model_filepath = ONNX_NAME
    >>> session = rt.InferenceSession(ONNX_NAME, sess_options)

    """
    def __init__(self, model: nn.Module, args: tuple = (), kwargs: dict[str, Any] | None = None, leaf_modules: list[type[nn.Module] | nn.Module] | None = None, use_weight_scale_factors: bool = False, use_bias_scale_factors: bool = False, inplace: bool = False, **options) -> None:
        """
        Parameters
        ----------
        model : nn.Module
            Model for quantization.
        args : Tuple
            Positional arguments for model.
        kwargs : Dict[str, Any]
            Keyword arguments for model.
        leaf_modules : list with types of modules or instances of torch.nn.Module, optional
            Types of modules or module instances that must be interpreted as leaf modules while tracing.
        use_weight_scale_factors : bool
            Whether to use scale factors for weights tuning. Since additional memory consumption (x2
            times compared to off-mode) be careful to use. False by default.
        use_bias_scale_factors : bool
            Whether to use scale factors to train biases. False by default.
        inplace : bool
            Enables inplace modification of input model (reduces memory consumption). False by default.

        """

class _STMQuantizationPatternsBuilder:
    w_qtype: Incomplete
    act_qtype: Incomplete
    def __init__(self, use_weight_scale_factors: bool, use_bias_scale_factors: bool) -> None: ...
    def build(self) -> list[list[SubgraphTransformPattern]]: ...
