from enum import Enum

class DistillationLayerSelectionStrategy(Enum):
    """
    Layer selection strategy for quantization distillation procedure.

    This strategy tells which layers will be used for distillation process during quantization.

    Layer selection for distillation has been proven to be important, with some strategies being more robust in general
    while the others can provide better results in specific cases. For example, it is not a good idea to make
    distillation over detection network outputs as it produces unstable gradients. However, distillation over
    classification network outputs is widely used and provides good results in multiple scenarios.

    The four available regimes are the following:

    #. **DISTILL_LAST_QUANT_LAYERS**

        * Finds last quantized layers and distill over their outputs. Default option, robust to different scenarios
          including classification, segmentation, detection.

    #. **DISTILL_OUTPUTS**

        * Finds all ``PyTorch`` tensors in user model's outputs and distill over them. Useful for classification
          problems with cross entropy loss (:class:`torch.nn.CrossEntropyLoss`).

    #. **DISTILL_ALL_QUANT_LAYERS**

        * Finds all quantized layers and distill over their outputs. This is generally more robust to overfitting, but
          in practice converges worse for small number of distillation epochs.

    #. **DISTILL_USER_DEFINED_LAYERS**

        * Distillation over user-defined tensors in the model. User should wrap such tensors with
          :class:`.QuantDistillationModule` module call. For more information, see it's documentation.

    """
    DISTILL_LAST_QUANT_LAYERS: int
    DISTILL_OUTPUTS: int
    DISTILL_ALL_QUANT_LAYERS: int
    DISTILL_USER_DEFINED_LAYERS: int
