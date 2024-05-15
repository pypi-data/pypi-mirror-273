from _typeshed import Incomplete
from enot.quantization.calibration.function_builder import AsymmetricMinMaxFunctionBuilder as AsymmetricMinMaxFunctionBuilder, SymmetricMinMaxFunctionBuilder as SymmetricMinMaxFunctionBuilder
from enot.quantization.calibration.functions import AsymmetricCalibrationFunction as AsymmetricCalibrationFunction, SymmetricCalibrationFunction as SymmetricCalibrationFunction
from enot.quantization.utils.common import CalibrationMethod as CalibrationMethod, QuantizationStrategy as QuantizationStrategy, QuantizationType as QuantizationType, TensorInfo as TensorInfo
from typing import Callable

class CalibrationFunctionFactory:
    """Constructs calibration functions by QuantizationType."""
    def __init__(self) -> None: ...
    def register_builder(self, key: tuple[QuantizationStrategy, CalibrationMethod], builder: Callable) -> None:
        """
        Registers builder for particular QuantizationStrategy and CalibrationMethod.

        Parameters
        ----------
        key : Tuple[QuantizationStrategy, CalibrationMethod]
            A key that identifies the builder.
        builder : Callable
            Callable object that will be built calibration function
            by quantization description and tensor description.

        """
    def create(self, quantization_type: QuantizationType, tensor_info: TensorInfo | None) -> SymmetricCalibrationFunction | AsymmetricCalibrationFunction:
        """
        Creates calibration function by quantization description and tensor description.

        Parameters
        ----------
        quantization_type : QuantizationType
            Quantization description.
        tensor_info : Optional[TensorInfo]
            Description of the target tensor. Can be None in case of layerwise quantization.

        Returns
        -------
        Union[SymmetricCalibrationFunction, AsymmetricCalibrationFunction]
            Calibration function.

        """

CALIBRATION_FUNCTION_FACTORY: Incomplete
