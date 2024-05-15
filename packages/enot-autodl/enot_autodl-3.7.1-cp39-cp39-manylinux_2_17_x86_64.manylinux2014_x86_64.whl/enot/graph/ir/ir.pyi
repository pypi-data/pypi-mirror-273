import torch
from _typeshed import Incomplete
from enot.graph.ir.node import Node as Node
from enot.graph.ir.shape_inference import shape_inference as shape_inference
from enot.graph.ir.snapshot import Snapshot as Snapshot
from enot.graph.ir.tracer import DefaultIRTracer as DefaultIRTracer, IRTracer as IRTracer
from enot.graph.match_patterns.base import find_pattern as find_pattern
from enot.graph.transform_patterns.base import SubgraphTransformPattern as SubgraphTransformPattern
from enot.utils.common import getattr_complex as getattr_complex
from torch import fx, nn
from typing import Any, Callable, Final
from typing_extensions import Self

DEFAULT_SNAPSHOT_NAME: Final[str]

class IR(nn.Module):
    """
    Intermediate representation of source model, that manages computational graph snapshots of the concrete model state
    for concrete input arguments. It allows to create/edit/delete snapshots.

    Notes
    -----
    It is the analogous to ``torch.fx.GraphModule``, which can manage more than one ``torch.fx.Graph``.

    IR should be serialized/deserialized only with dill module:
    - `torch.save(model, 'path', pickle_module=dill)`
    - `torch.load('path', pickle_module=dill)`

    """
    model: Incomplete
    training: Incomplete
    def __init__(self, model: nn.Module, *, snapshot_tracer_factory: Callable[[IR], IRTracer] | None = None) -> None:
        """
        Parameters
        ----------
        model : nn.Module
            Source model.
        snapshot_tracer_factory : Optional[Callable[[IR], IRTracer]]
            Factory function for the IR tracer.
            If None, then ``DefaultIRTracer`` will be used.
            Default value is None.

        """
    @property
    def snapshot_names(self) -> list[str]:
        """Tuple of snapshot names."""
    @property
    def active_snapshot_name(self) -> str | None:
        """
        Name of the active (used as computational graph) snapshot.

        None if the initial model forward is used.

        """
    def create_snapshot(self, name: str = ..., *, args: tuple = (), kwargs: dict[str, Any] | None = None, tracer: IRTracer | None = None) -> Self:
        """
        Create new snapshot of the current model state.

        Parameters
        ----------
        name : str
            Name of the new snapshot.
        args : Tuple
            Positional arguments that will be used for tracing.
        kwargs : Dict[str, Any]
            Keyword arguments that will be used for tracing.
        tracer : Optional[IRTracer]
            Tracer that should be used instead of default tracer. None by default.

        Returns
        -------
        IR
            Self.

        """
    def delete_snapshot(self, name: str = ...) -> Self:
        """Delete snapshot with given name."""
    def activate_snapshot(self, name: str | None = ...) -> Self:
        """Set up snapshot with given name as computational graph of the IR."""
    def snapshot(self, name: str = ...) -> Snapshot:
        """Return snapshot by name."""
    def compiled_snapshot(self, name: str = ...) -> fx.GraphModule:
        """
        Return snapshot in the form ``torch.fx.GraphModule``.

        Can be used to run computations or export the model to ONNX.

        """
    def transform_snapshot(self, name: str = ..., *, transforms: list[SubgraphTransformPattern], excluded_modules: list[type[nn.Module] | nn.Module] | None = None) -> Self:
        """
        Transform snapshot.

        Parameters
        ----------
        name : str
            Name of the snapshot to transform.
        transforms : List[SubgraphTransformPattern]
            List of transformation patterns.
        excluded_modules : Optional[List[Union[Type[torch.nn.Module], torch.nn.Module]]]
            Types of modules or module instances that need to be excluded from pattern matching.

        Returns
        -------
        IR
            Self.

        """
    def delete_compiled_snapshots_cache(self) -> Self:
        """Clean up cache of the compiled snapshots."""
    def shape_infer_snapshot(self, name: str = ..., *, args: tuple = (), kwargs: dict[str, Any] | None = None) -> Self:
        """
        Run shape inference for snapshot.

        Parameters
        ----------
        name : str
            Snapshot name for shape inference.
        args : Tuple
            Positional arguments for shape inference.
        kwargs : Optional[Dict[str, Any]]
            Keyword arguments for shape inference.

        """
    def model_attribute(self, name: str) -> Any:
        """Return model attribute by name (search in model and in attached data)."""
    def attach_data(self, data: nn.Module | nn.Parameter | torch.Tensor, suggested_name: str) -> str:
        """
        Attach new data (module, parameter or buffer) to the model.

        Parameters
        ----------
        data : Union[nn.Module, nn.Parameter, torch.Tensor]
            Data to be added.
        suggested_name : str
            Name for that data in IR.

        Returns
        -------
        str
            Name of the added data in IR.

        """
    def delete_unused_data(self) -> Self:
        """Remove unused data that was attached using ``attach_data``."""
    def on_snapshot_update(self, name: str = ...) -> None:
        """Used as signal that the snapshot has been updated."""
    def forward(self, *args, **kwargs) -> Any: ...
