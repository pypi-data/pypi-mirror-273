import torch
from _typeshed import Incomplete
from dataclasses import dataclass
from enum import Enum
from torch import _C as torch_C
from typing import Any, Callable, NamedTuple, Sequence

class TensorInfo(NamedTuple):
    shape: Sequence[int]
    channel_axis: int

class QuantizationGranularity(Enum):
    """Quantization granularity: layerwise or channelwise."""
    LAYERWISE: str
    CHANNELWISE: str

class QuantizationStrategy(Enum):
    """Quantization strategy: symmetric or assymetric."""
    SYMMETRIC: str
    ASYMMETRIC: str

class CalibrationMethod(Enum):
    """Calibration method: how-to calculate calibration thresholds."""
    MIN_MAX: str

class _DifferentiableRoundHalfToEven(torch.autograd.Function):
    @staticmethod
    def forward(ctx: Any, *args: Any, **kwargs: Any) -> Any: ...
    @staticmethod
    def backward(ctx: Any, *grad_outputs: Any) -> Any: ...

differentiable_round_half_to_even: Incomplete

class _DifferentiableRoundHalfUp(torch.autograd.Function):
    @staticmethod
    def forward(ctx: Any, *args: Any, **kwargs: Any) -> Any: ...
    @staticmethod
    def backward(ctx: Any, *grad_outputs: Any) -> Any: ...

differentiable_round_half_up: Incomplete

class RoundingFunction(Enum):
    """Function is used to round values in quantization/dequantization transformations."""
    HALF_TO_EVEN: Incomplete
    HALF_UP: Incomplete

@dataclass(frozen=True)
class QuantizationType:
    """Defines the type of quantization."""
    granularity: QuantizationGranularity
    strategy: QuantizationStrategy
    calibration_method: CalibrationMethod
    rounding_function: RoundingFunction
    bitness: int = ...
    calibration_options: dict[str, Any] | None = ...
    use_weight_scale_factors: bool = ...
    use_bias_scale_factors: bool = ...
    quantize_bias: bool = ...
    def __init__(self, granularity: QuantizationGranularity, strategy: QuantizationStrategy, calibration_method: CalibrationMethod = ..., rounding_function: RoundingFunction = ..., bitness: int = 8, calibration_options: dict[str, Any] | None = None, use_weight_scale_factors: bool = False, use_bias_scale_factors: bool = True, quantize_bias: bool = False) -> None:
        """
        Parameters
        ----------
        granularity : QuantizationGranularity
            Quantization granularity: layerwise or channelwise.
        strategy : QuantizationStrategy
            QuantizationStrategy: symmetric or asymmetric.
        calibration_method : CalibrationMethod
            The method that is used to calculate thresholds.
        rounding_function : RoundingFunction
            The function that is used to round values in quantization procedure.
        bitness : int
            Bitness of quantization.
        use_weight_scale_factors : bool
            Whether to use scale factors for weights tuning. Since additional memory consumption (x2
            times compared to off-mode) be careful to use. False by default.
        use_bias_scale_factors : bool
            Whether to use scale factors to train biases. True by default.
        quantize_bias : bool
            Quantize bias or not, related to WeightQuantizationModule only. Default is False.

        """

def float_model_from_quantized_model(quantized_model: Any) -> Any:
    """Creates a copy of quantized model with the disabled fake quantization."""

class CustomOnnxExport(torch.autograd.Function):
    """
    Replaces standard Torch symbolic tracing.

    Can be used to customize Torch-to-ONNX export.

    """
    @classmethod
    def set_forward_and_apply(cls, forward_function: Callable, *args, **kwargs) -> Any: ...
    @staticmethod
    def forward(ctx: Any, *args: Any, **kwargs: Any) -> Any: ...
    @staticmethod
    def backward(ctx: Any, *grad_outputs: Any) -> Any: ...
    @staticmethod
    def symbolic(graph: torch_C.Graph, *values) -> torch_C.Value: ...

def optimal_quantization_scheme() -> str:
    """Returns optimal quantization scheme for locally installed GPU."""
