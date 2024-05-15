from enot.graph.ir.ir import IR as IR
from enot.rescaling.transforms.rescaler import RescaleTransformPattern as RescaleTransformPattern
from enot.rescaling.transforms.stats_collector import InsertStatsCollectorTransformPattern as InsertStatsCollectorTransformPattern
from torch import nn as nn
from torch.fx import GraphModule as GraphModule
from typing import Any

class RescalingCalibrator:
    """
    Is a simple tool to improve accuracy when using quantization.

    Examples
    --------
    >>> from enot.rescaling import RescalingCalibrator
    >>> rescaling_calibrator = RescalingCalibrator(model)
    >>> # calibration (collecting activation statistics):
    >>> for sample, _ in dataloader:
    >>>     rescaling_calibrator(sample)  # pass model args/kwargs as usual
    >>> # rescaling (activations and weights):
    >>> model = rescaling_calibrator.rescale(alpha=0.5)

    """
    def __init__(self, model: nn.Module, *, args: tuple = (), kwargs: dict[str, Any] | None = None, excluded_modules: list[type[nn.Module] | nn.Module] | None = None, inplace: bool = False) -> None:
        """
        Parameters
        ----------
        model : torch.nn.Module
            Model for rescaling.
        args : Tuple
            Model positional arguments. Optional.
        kwargs : Optional[Dict[str, Any]]
            Model keyword arguments. Optional.
        excluded_modules : Optional[List[Union[Type[torch.nn.Module], torch.nn.Module]]]
            Modules or types of modules that should not be recaled.
        inplace : bool
            Rescaling not only inserts new submodules to the model, but also changes the weights of some submodules.
            In the case ``inplace=True`` calibrator copies the model and original model will not be changed.
            In the case ``inplace=False`` the weights of the original model will be changed.
            Default value is False.

        """
    def rescale(self, *, alpha: float = 0.5) -> GraphModule:
        """
        Rescale model using the statistics collected during the calibration process.

        Parameters
        ----------
        alpha : float
            Migration strength coefficient.
            Controls how much difficulty migrates from activation to weights.
            0.5 is a well-balanced point to evenly split the quantization difficulty.
            Choose a larger alpha to migrate more quantization difficulty to weights (like 0.75).
            Should be in the range [0, 1].
            Default value is 0.5.

        Returns
        -------
        torch.fx.GraphModule
            Rescaled model.
            Note, in case of ``inplace=True``, the model passed to :class:`RescalingCalibrator`
            will be completely broken, only use the model returned by this method.

        """
    def __call__(self, *args, **kwargs) -> Any: ...
