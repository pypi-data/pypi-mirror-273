from contextlib import ContextDecorator
from enot.distillation._distill_model import DistillModel as DistillModel
from enot.distillation.mapping import Mapping as Mapping
from torch import nn as nn
from torch.fx.graph_module import GraphModule as GraphModule

class distill(ContextDecorator):
    """
    Context manager that glues teacher and student model into one distillation model.

    Examples
    --------
    >>> from enot.distillation import Mapping
    >>> from enot.distillation import distill

    Create mapping between teacher and student models,
    also we additionaly added criterion for each mapping pair as payload.

    >>> mapping = Mapping(student, teacher)  # GraphModule - GraphModule mapping.
    >>> mapping.add('features_18_0', 'features_18_0', payload=nn.MSELoss())
    >>> mapping.add('features_2_conv_1_0', 'features_2_conv_1_0', payload=nn.CrossEntropyLoss())
    >>> mapping.add('features_5_conv_0_2', 'features_5_conv_0_2', payload=nn.MSELoss())

    Prepare optimizer, scheduler, dataloaders, etc as usual.

    >>> optimizer = RAdam(params=student.parameters())

    Use distill context to distill teacher knowledge to student.

    >>> with distill(student=student, teacher=teacher, mapping=mapping) as distill_model:
    >>>     inputs = torch.ones(1, 3, 224, 224)
    >>>     optimizer.zero_grad()
    >>>     output = distill_model(inputs)
    >>>     loss: torch.Tensor = torch.zeros(1)
    >>>     for student_output, teacher_output criterion in output:
    >>>         loss += criterion(student_output, teacher_output)
    >>>     loss.backward()
    >>>     optimizer.step()

    """
    def __init__(self, student: nn.Module | GraphModule, teacher: nn.Module | GraphModule, *, mapping: Mapping | None = None, nograd_teacher: bool = True) -> None:
        """
        Parameters
        ----------
        student : Union[nn.Module, GraphModule]
            Student; knowledge will be transferred to this model from teacher model.
        teacher : Union[nn.Module, GraphModule]
            Teacher; knowledge will be transferred from this model to student model.
        mapping : Optional[Mapping]
            Mapping specifies modules from where and where to distill.
        nograd_teacher : bool
            Use no_grad decorator for teacher or not. Default value is True.

        """
    def __enter__(self) -> nn.Module: ...
    def __exit__(self, exc_type: type[BaseException] | None, exc_value: BaseException | None, exc_traceback: types.TracebackType | None) -> None: ...
