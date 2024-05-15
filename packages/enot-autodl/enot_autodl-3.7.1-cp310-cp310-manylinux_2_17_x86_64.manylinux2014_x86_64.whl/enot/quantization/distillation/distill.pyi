from _typeshed import Incomplete
from contextlib import ContextDecorator
from enot.quantization.distillation.layer_search import find_all_quant_nodes as find_all_quant_nodes, find_distillation_nodes as find_distillation_nodes, find_last_quant_nodes as find_last_quant_nodes, find_node_references_in_output_node as find_node_references_in_output_node
from enot.quantization.distillation.strategy import DistillationLayerSelectionStrategy as DistillationLayerSelectionStrategy
from enot.quantization.fake_quantized_model import FakeQuantizedModel as FakeQuantizedModel
from enot.quantization.utils.context import disable_quantization_mode as disable_quantization_mode
from enot.utils.common import eval_mode as eval_mode
from torch import nn
from torch.fx.graph_module import GraphModule as GraphModule
from torch.fx.node import Node as Node

class distill(ContextDecorator):
    """
    Context manager for distillation of :class:`~enot.quantization.FakeQuantizedModel`.

    Returns a pair consisting of a special module and parameters for backpropagation.
    The module accepts data and returns pairs: ``(student_output, teacher_output)``,
    which need to be passed to the loss function for distillation.

    Examples
    --------
    >>> from enot.quantization import distill
    >>> from enot.quantization import RMSELoss
    >>>
    >>> with distill(fq_model=fq_model, tune_weight_scale_factors=True) as (qdistill_model, params):
    >>>     optimizer = RAdam(params=params, lr=0.005, betas=(0.9, 0.95))
    >>>     scheduler = CosineAnnealingLR(optimizer=optimizer, T_max=len(dataloader) * n_epochs)
    >>>     criterion = RMSELoss()
    >>>
    >>>     for _ in range(n_epochs):
    >>>         for batch in dataloader:
    >>>             batch = batch[0]
    >>>
    >>>             optimizer.zero_grad()
    >>>             loss: torch.Tensor = torch.tensor(0.0)
    >>>             for student_output, teacher_output in qdistill_model(batch):
    >>>                 loss += criterion(student_output, teacher_output)
    >>>
    >>>             loss.backward()
    >>>             optimizer.step()
    >>>             scheduler.step()

    """
    def __init__(self, fq_model: FakeQuantizedModel, model: nn.Module | GraphModule | None = None, strategy: DistillationLayerSelectionStrategy = ..., tune_weight_scale_factors: bool = False) -> None:
        """
        Parameters
        ----------
        fq_model : FakeQuantizedModel
            Fake-quantized model.
        model : Optional[Union[nn.Module, GraphModule]]
            Optional teacher model for distillation.
            If value is None, float ``fq_model`` will be used as a teacher model.
            Default value is None.
        strategy : DistillationLayerSelectionStrategy
            Distillation layer selection strategy.
            Default value is ``DISTILL_LAST_QUANT_LAYERS``.
        tune_weight_scale_factors : bool
            Whether to tune weight scale factors or not. False by default.
            Note: turning on weight scale factors in fake quantized model
            leads to additional memory consumption - x2 compared to disabled mode.

        """
    def __enter__(self) -> tuple[nn.Module, list[nn.Parameter]]: ...
    def __exit__(self, exc_type: type[BaseException] | None, exc_value: BaseException | None, exc_traceback: types.TracebackType | None) -> None: ...

class _QDistillModel(nn.Module):
    teacher: Incomplete
    student: Incomplete
    def __init__(self, teacher: FakeQuantizedModel | nn.Module | GraphModule, student: FakeQuantizedModel) -> None: ...
    def forward(self, *args, **kwargs) -> list: ...
