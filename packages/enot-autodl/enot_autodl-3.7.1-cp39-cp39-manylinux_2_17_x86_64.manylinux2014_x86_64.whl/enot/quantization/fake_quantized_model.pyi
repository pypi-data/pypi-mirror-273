from enot.graph.transform_patterns.base import SubgraphTransformPattern
from enot.quantization.utils.common import QuantizationType
from torch import nn
from torch.fx import GraphModule
from typing import Any, Iterator

__all__ = ['FakeQuantizedModel']

class FakeQuantizedModel(nn.Module):
    """
    Base FakeQuantized model class.

    Inserts fake quantization nodes into the model and provides interface for calibration
    and quantization aware training.

    """
    def __init__(self, model: nn.Module, args: tuple, kwargs: dict[str, Any], transform_patterns: list[list[SubgraphTransformPattern]], activations_quantization_type: QuantizationType, leaf_modules: list[type[nn.Module] | nn.Module] | None = None, inplace: bool = False, **options) -> None:
        """
        Parameters
        ----------
        model : torch.nn.Module
            Model from which :class:`FakeQuantizedModel` will be constructed.
        args : Tuple
            Positional arguments for model.
        kwargs : Dict[str, Any]
            Keyword arguments for model.
        transform_patterns : Sequence[Tuple[SubgraphTransformPattern, ...]]
            Sequence of group of transformations patterns. Each group will be applied separately.
        activations_quantization_type : QuantizationType
            Type of activations quantization.
            Activations quantization supports only layerwise (scalar) and QuantizationStrategy
            and any QuantizationStrategy.
        leaf_modules : list with types of modules or instances of torch.nn.Module, optional
            Types of modules or module instances that must be interpreted as leaf modules while tracing.
        inplace : bool
            Enables inplace modification of input model (reduces memory consumption).
        kwargs : kwargs
            Additional options.

        """
    @property
    def fake_quantized_model(self) -> GraphModule:
        """
        Returns parsed quantized model graph module.

        Returns
        -------
        torch.fx.GraphModule
            Parsed model.

        """
    @property
    def is_full_calibration_enabled(self) -> bool:
        """Whether all quantized layers in the model are in calibration mode or not."""
    @property
    def is_full_fake_quantization_enabled(self) -> bool:
        """Whether fake quantization is enabled in all quantized layers in the model or not."""
    def quantization_parameters(self) -> Iterator[nn.Parameter]:
        """
        Returns an iterator over model quantization parameters (quantization thresholds).

        Returns
        -------
        iterator over torch.nn.Parameter
            An iterator over model quantization parameters.

        Notes
        -----
        Weights of quantized modules (like convolution weight tensor or linear layer weight matrix) are not quantization
        parameters.

        """
    def scale_factors(self) -> Iterator[nn.Parameter]:
        """
        Returns an iterator over scale factors.

        Notes
        -----
        Scale factors are not the same as scale/zero_point in quantization parameters.
        They have their own meaning and help improve quantization results.

        """
    def regular_parameters(self) -> Iterator[nn.Parameter]:
        """
        Returns an iterator over model parameters excluding quantization parameters.

        Returns
        -------
        iterator over torch.nn.Parameter
            An iterator over regular model parameters.

        """
    def enable_calibration_mode(self, mode: bool = True) -> FakeQuantizedModel:
        """
        Enables or disables calibration mode.

        In the calibration mode quantized model collects input data statistics which will be used for quantization
        parameter initialization.

        Parameters
        ----------
        mode : bool, optional
            Whether to enable calibration mode. Default value is True.

        Returns
        -------
        FakeQuantizedModel
            self

        """
    def enable_quantization_mode(self, mode: bool = True) -> FakeQuantizedModel:
        """
        Enables or disables fake quantization.

        Fake quantization mode is enabled for all quantized layers. In this regime these layers are using fake
        quantization nodes to produce quantized weights and activations during forward pass.

        Parameters
        ----------
        mode : bool, optional
            Whether to use fake quantization. Default value is True.

        Returns
        -------
        FakeQuantizedModel
            self

        """
    def forward(self, *args, **kwargs) -> Any: ...
