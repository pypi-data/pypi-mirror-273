import abc
from abc import ABC, abstractmethod
from enot.graph.ir.snapshot import Snapshot as Snapshot
from enot.pruning.label_selector.channel_selector_constraint import ChannelsSelectorConstraint as ChannelsSelectorConstraint, DummyChannelsSelectorConstraint as DummyChannelsSelectorConstraint
from enot.pruning_v2.criteria.label_groups import label_groups as label_groups
from enot.pruning_v2.ir import PruningIR as PruningIR
from enot.pruning_v2.label import Label as Label
from torch import nn as nn
from typing import Callable

class LabelSelector(ABC, metaclass=abc.ABCMeta):
    """
    Base class for all pruning label selectors.

    This class defines an abstract method :meth:`PruningLabelSelector.select` that should return labels to prune.

    """
    @abstractmethod
    def select(self, snapshot: Snapshot) -> list[Label]:
        """
        Method that chooses which labels should be pruned based on current label selector policy.

        .. warning::
            Depending on label selector implementation, this function may have significant execution time.

        Parameters
        ----------
        snapshot : Snapshot
            Target snapshot.

        Returns
        -------
        list of Label
            List of labels which should be pruned.

        """

class LatencyMeasurementError(Exception):
    """Must be raised by a latency measurement function if the measurement
    cannot be performed for a particular model configuration."""

class TargetLatencyMixin:
    """Adds a target_latency property to the class."""
    @property
    def target_latency(self) -> float:
        """Desired latency of the pruned model."""
    @target_latency.setter
    def target_latency(self, value: float) -> None: ...

def maybe_select_by_latency_bounds(snapshot: Snapshot, latency_calculation_function: Callable[[nn.Module], float], target_latency: float, constraint: ChannelsSelectorConstraint | None = None) -> list[Label] | None:
    '''
    Checks that `target_latency` is within acceptable values. If target_latency is less than the minimum possible
    latency for this model, it returns a list of labels to prune to the minimum model. If `target_latency` is greater
    than the latency of the model, it returns an empty list of labels for pruning. In all other cases it returns `None`.

    Parameters
    ----------
    snapshot : Snapshot
        Target snapshot.
    target_latency : float
        Target model latency.
        This argument should have the same units as output of ``latency_calculation_function``.
    latency_calculation_function : Callable[[torch.nn.Module], float]
        Function that calculates model latency.
        It should take model (torch.nn.Module) and measure the "speed" (float) of its execution.
        It could be a number of FLOPs, MACs, inference time on CPU/GPU or other "speed" criteria.
    constraint : Optional[ChannelsSelectorConstraint]
        Optional :class:`~enot.pruning.ChannelsSelectorConstraint` instance,
        that calculates low, high and step for the constraint for total number of labels in group.
        If None, then :class:`~enot.pruning.DefaultChannelsSelectorConstraint` will be used.
        None by default.

    Returns
    -------
    Optional[List[Label]]
        List of labels for pruning or None.

    '''
