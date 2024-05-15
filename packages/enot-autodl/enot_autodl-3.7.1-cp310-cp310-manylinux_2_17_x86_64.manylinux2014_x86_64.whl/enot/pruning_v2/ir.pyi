from enot.graph.ir.ir import DEFAULT_SNAPSHOT_NAME as DEFAULT_SNAPSHOT_NAME, IR as IR
from enot.graph.ir.tracer import FxIRTracer as FxIRTracer, IRTracer as IRTracer
from enot.pruning_v2.label import Label as Label
from enot.pruning_v2.label_inference.inference import infer_labels as infer_labels, registered_modules as registered_modules
from enot.pruning_v2.marker.mark import mark as mark
from enot.pruning_v2.pruner import pruner as pruner
from enot.pruning_v2.snapshot import PruningSnapshot as PruningSnapshot
from enot.pruning_v2.snapshot_tracer import PruningSnapshotTracer as PruningSnapshotTracer
from torch import nn as nn
from typing import Any
from typing_extensions import Self

class PruningIR(IR):
    """
    The main class containing internal pruning data and providing a high-level interface
    for pruning user-defined models.

    Notes
    -----
    It should only be serialized/deserialized using the ``dill`` module:

    >>> torch.save(ir, 'ir.pt', pickle_module=dill)
    >>> torch.load('ir.pt', pickle_module=dill)

    """
    def __init__(self, model: nn.Module, *, leaf_modules: list[type[nn.Module] | nn.Module] | None = None, registered_modules_as_leaf_modules: bool = True, soft_tracing: bool = True) -> None:
        """
        Parameters
        ----------
        model : torch.nn.Module
            Model for pruning.
        leaf_modules : list of Type[torch.nn.Module] or torch.nn.Module, Optional
            Types of modules or module instances that must be interpreted as leaf modules. Leaf modules are the atomic
            units that appear in the IR.
        registered_modules_as_leaf_modules : bool
            Whether ``torch.nn.Module``-modules registered in the label inference registry should be treated as leaf
            modules or not. Default value is True.
        soft_tracing : bool
            If True then untraceable modules will be interpreted as leaf modules. True by default.

        """
    def create_snapshot(self, name: str = ..., *, args: tuple = (), kwargs: dict[str, Any] | None = None, tracer: IRTracer | None = None) -> Self: ...
    def infer_labels(self, name: str = ..., *, args: tuple = (), kwargs: dict[str, Any] | None = None) -> Self:
        """
        Run label inference for snapshot.

        Parameters
        ----------
        name : str
            Snapshot name for label inference.
        args : Tuple
            Positional arguments for label inference.
        kwargs : Optional[Dict[str, Any]]
            Keyword arguments for label inference.

        """
    def prune(self, name: str = ..., *, labels: list[Label], inplace: bool = False, skip_label_checking: bool = False) -> Self:
        """
        Run pruning procedure.

        Parameters
        ----------
        name : str
            Name of the snapshot for pruning. In most cases this parameter can be ommited.
        labels : List[Label]
            List of labels that should be pruned.
        inplace : bool
            Enables inplace modification of input model (reduces memory consumption). False by default.
        skip_label_checking : bool
            If True, labels flags consistency checks will be skipped. Default value is False.

        Returns
        -------
        PruningIR
            Reference to the pruned intermediate representation.

        Notes
        -----
        If labels is empty and inplace is False, a copy of the current intermediate representation will be returned.

        """
    def set_force_thunk_update(self, force: bool) -> Self:
        """
        Force updates to arguments that are ``thunks`` (nodes with ``op != get_attr``).

        It can completely break the original model (``torch.nn.Module``).

        """
