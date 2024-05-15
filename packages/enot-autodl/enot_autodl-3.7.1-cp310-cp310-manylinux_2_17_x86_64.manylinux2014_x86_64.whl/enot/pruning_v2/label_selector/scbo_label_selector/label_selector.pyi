import torch
from _typeshed import Incomplete
from enot.graph.ir.snapshot import Snapshot as Snapshot
from enot.pruning.label_selector.channel_selector_constraint import ChannelsSelectorConstraint as ChannelsSelectorConstraint, DefaultChannelsSelectorConstraint as DefaultChannelsSelectorConstraint
from enot.pruning_v2.criteria.label_groups import label_groups as label_groups
from enot.pruning_v2.ir import PruningIR as PruningIR
from enot.pruning_v2.label import Label as Label
from enot.pruning_v2.label_selector.base import LabelSelector as LabelSelector, LatencyMeasurementError as LatencyMeasurementError, TargetLatencyMixin as TargetLatencyMixin, maybe_select_by_latency_bounds as maybe_select_by_latency_bounds
from enot.pruning_v2.label_selector.scbo_label_selector.scbo import SCBO as SCBO
from enot.pruning_v2.label_selector.scbo_label_selector.scbo_state import SCBOState as SCBOState
from enot.pruning_v2.label_selector.starting_points_generator import StartingPointsGenerator as StartingPointsGenerator
from torch import nn as nn
from typing import Any, Callable

class SCBOLabelSelector(LabelSelector, TargetLatencyMixin):
    """Label selector based on SCBO algorithm."""
    target_latency: Incomplete
    def __init__(self, target_latency: float, latency_calculation_function: Callable[[nn.Module], float], n_search_steps: int | None, n_starting_points: int | None = None, batch_size: int = 4, constraint: ChannelsSelectorConstraint | None = None, additional_starting_points_generator: StartingPointsGenerator | None = None, device: str | torch.device | None = None, dtype: torch.dtype = ..., verbose: bool = True, handle_ctrl_c: bool = False, seed: int | None = None, scbo_kwargs: dict[str, Any] | None = None) -> None:
        '''
        Parameters
        ----------
        target_latency : float
            Target model latency.
            This argument should have the same units as output of ``latency_calculation_function``.
        latency_calculation_function : Callable[[torch.nn.Module], float]
            Function that calculates model latency.
            It should take model (torch.nn.Module) and measure the "speed" (float) of its execution.
            It could be a number of FLOPs, MACs, inference time on CPU/GPU or other "speed" criteria.
            If latency measurement cannot be performed for a particular model configuration due to technical reasons
            (e.g., problems with measurements on a server), then ``latency_calculation_function`` should raise
            :class:`~enot.pruning_v2.label_selector.LatencyMeasurementError`.
        n_search_steps : Optional[int]
            Number of configurations (samples) for pruning to find optimal architecture.
            If None, then search loop will stop when SCBO converges.
        n_starting_points : Optional[int]
            Number of sampled configurations used for startup step.
            If None, then ``n_starting_points`` calculates as
            ``min(total_number_of_groups_in_model * 2, n_search_steps - 1)``.
            None by default.
        batch_size : int
            Batch size for SCBO algorithm. 4 by default.
        constraint : Optional[ChannelsSelectorConstraint]
            Optional :class:`~enot.pruning.ChannelsSelectorConstraint` instance,
            that calculates low, high and step for the constraint for total number of labels in group.
            If None, then :class:`~enot.pruning.DefaultChannelsSelectorConstraint` will be used.
            None by default.
        additional_starting_points_generator : Optional[StartingPointsGenerator]
            User defined generator of additional starting points for SCBO algorithm. None by default.
        device : Optional[Union[str, torch.device]]
            The desired device for SCBO algorithm.
            None by default (cuda if possible).
        dtype : torch.dtype
            The desired dtype of SCBO algorithm. `torch.double` by default.
        verbose : bool
            Whether to show progress bar or not. True by default.
        handle_ctrl_c : bool
            Whether to allow early stop by **Ctrl+c** or not. False by default.
        seed : Optional[int]
            Optional seed for SCBO algorithm. Default value is None.
        scbo_kwargs : Optional[Dict[str, Any]]
            Additional keyword arguments for SCBO (developers only).

        '''
    @property
    def batch_size(self) -> int:
        """SCBO batch size."""
    @batch_size.setter
    def batch_size(self, value: int) -> None: ...
    @property
    def n_search_steps(self) -> int | None:
        """Number of search steps."""
    @n_search_steps.setter
    def n_search_steps(self, value: int | None) -> None: ...
    @property
    def n_starting_points(self) -> int | None:
        """Number of starting points."""
    @n_starting_points.setter
    def n_starting_points(self, value: int | None) -> None: ...
    @property
    def verbose(self) -> bool:
        """Whether to show progress bar or not."""
    @verbose.setter
    def verbose(self, value: bool) -> None: ...
    def set_search_step_cb(self, search_step_cb: Callable[[list[Label], int, float, float], bool] | None) -> None:
        """
        Set search step callback. This callback will be called every time a pair (score, latency) improvement occurs
        during the search procedure.

        Parameters
        ----------
        search_step_cb : Callable[[List[Label], int, float, float], bool]
        Callback function. This function should take list of labels (which were selected by SCBO) as first argument,
        number of the best step as second argument, new best score of pruned model as third argument and new
        latency of pruned model as the last argument. If callback returns ``True``, the search is terminated.

        """
    def select(self, snapshot: Snapshot) -> list[Label]: ...
