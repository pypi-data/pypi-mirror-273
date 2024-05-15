from enot.quantization.calibration.functions import AsymmetricCalibrationFunction as AsymmetricCalibrationFunction, AsymmetricMinMaxCalibration as AsymmetricMinMaxCalibration, SymmetricCalibrationFunction as SymmetricCalibrationFunction, SymmetricMinMaxCalibration as SymmetricMinMaxCalibration
from enot.quantization.utils.common import TensorInfo as TensorInfo

class SymmetricMinMaxFunctionBuilder:
    def __call__(self, tensor_info: TensorInfo) -> SymmetricCalibrationFunction: ...

class AsymmetricMinMaxFunctionBuilder:
    def __call__(self, tensor_info: TensorInfo) -> AsymmetricCalibrationFunction: ...
