from contextlib import ContextDecorator
from enot.quantization.fake_quantized_model import FakeQuantizedModel as FakeQuantizedModel
from enot.quantization.qnn.fake_quantization.fake_quantization import FakeQuantization as FakeQuantization
from enot.utils.common import iterate_by_submodules as iterate_by_submodules

class calibrate(ContextDecorator):
    """
    Context manager which enables and disables quantization threshold calibration procedure.

    Within this context manager, calibration procedure is enabled in all
    :class:`~enot.quantization.FakeQuantizedModel` objects. Exiting this context
    manager resets calibration and quantization flags in all layers to their initial values.

    Examples
    --------
    >>> from enot.quantization import calibrate
    >>>
    >>> with torch.no_grad(), calibrate(fq_model):
    >>>     for batch in itertools.islice(dataloader, 10):  # 10 batches for calibration
    >>>         batch = batch[0].cuda()
    >>>         fq_model(batch)

    """
    def __init__(self, fq_model: FakeQuantizedModel) -> None:
        """
        Parameters
        ----------
        fq_model : FakeQuantizedModel
            Fake-quantized model instance to calibrate.

        """
    def __enter__(self) -> None: ...
    def __exit__(self, exc_type: type[BaseException] | None, exc_value: BaseException | None, exc_tb: types.TracebackType | None) -> None: ...
