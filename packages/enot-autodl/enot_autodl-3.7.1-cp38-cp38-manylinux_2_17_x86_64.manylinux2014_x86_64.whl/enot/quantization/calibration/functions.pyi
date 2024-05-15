import abc
import torch
from _typeshed import Incomplete
from abc import ABC, abstractmethod
from enot.quantization.utils.common import TensorInfo as TensorInfo
from torch import nn

class SymmetricCalibrationFunction(ABC, nn.Module, metaclass=abc.ABCMeta):
    """Interface (function signature) of symmetric calibration functions."""
    channel_axis: Incomplete
    def __init__(self, tensor_info: TensorInfo | None) -> None:
        """
        Parameters
        ----------
        tensor_info : Optional[TensorInfo]
            Description of target tensor. Can be None in case of layerwise quantization.

        """
    @abstractmethod
    def __call__(self, value: torch.Tensor, threshold: torch.Tensor) -> torch.Tensor:
        """
        Calibrates threshold.

        Parameters
        ----------
        value : torch.Tensor
            Data for calibration.
        threshold : torch.Tensor
            Current threshold.

        Returns
        -------
        torch.Tensor
            Updated (by calibration) threshold.

        """

class AsymmetricCalibrationFunction(ABC, nn.Module, metaclass=abc.ABCMeta):
    """Interface (function signature) of asymmetric calibration functions."""
    channel_axis: Incomplete
    def __init__(self, tensor_info: TensorInfo | None) -> None:
        """
        Parameters
        ----------
        tensor_info : Optional[TensorInfo]
            Description of target tensor. Can be None in case of layerwise quantization.

        """
    @abstractmethod
    def __call__(self, value: torch.Tensor, threshold_min: torch.Tensor, threshold_max: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:
        """
        Calibrates min (left) and max (right) thresholds.

        Parameters
        ----------
        value : torch.Tensor
            Data for calibration.
        threshold_min : torch.Tensor
            Current min (left) threshold.
        threshold_max : torch.Tensor
            Current max (right) threshold.

        Returns
        -------
        Tuple[torch.Tensor, torch.Tensor]
            Updated thresholds.

        """

class SymmetricMinMaxCalibration(SymmetricCalibrationFunction):
    def __call__(self, value: torch.Tensor, threshold: torch.Tensor) -> torch.Tensor:
        """
        Returns updated threshold value for scalar min-max tensor quantization.

        Threshold for tensor is calculated as a maximum absolute value of tensor over the whole calibration data.

        Parameters
        ----------
        value : torch.Tensor
            Calibration data (shape = any).
        threshold : torch.Tensor
            Current threshold value (shape = (1,)).

        Returns
        -------
        torch.Tensor
            Updated threshold (shape = (1,)).

        """

class AsymmetricMinMaxCalibration(AsymmetricCalibrationFunction):
    def __call__(self, value: torch.Tensor, threshold_min: torch.Tensor, threshold_max: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:
        """
        Returns updated threshold values for scalar asymmetric min-max tensor quantization.

        Parameters
        ----------
        value : torch.Tensor
            Calibration data.
        threshold_min : torch.Tensor
            Current min threshold value tensor.
        threshold_max : torch.Tensor
            Current max threshold value tensor.

        Returns
        -------
        Tuple[torch.Tensor, torch.Tensor]
            Updated thresholds.

        """
