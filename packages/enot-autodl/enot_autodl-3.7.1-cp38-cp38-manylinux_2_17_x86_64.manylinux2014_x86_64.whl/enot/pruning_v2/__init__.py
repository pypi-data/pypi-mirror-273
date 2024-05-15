# pylint: disable=useless-import-alias
"""
The ``enot.pruning_v2`` module contains functional for automatic pruning of user-models.

This module features pre-defined or custom pruning procedures for removing least important filters or neurons.
It currently supports structured pruning procedure.
User can define pruning ratio manually or use any of the pre-defined strategies.

The module exports the following names:
- ``PruningIR``
- ``LossAwareCriterion``
- ``UniformLabelSelector``, ``GlobalScoreLabelSelector``, ``KnapsackLabelSelector``, ``LatencyLabelSelector``,
``SCBOLabelSelector``

For details see documentation: https://enot-autodl.rtd.enot.ai

Examples
--------
>>> from enot.pruning_v2 import PruningIR
>>> from enot.pruning_v2 import LossAwareCriterion
>>> from enot.pruning_v2 import UniformLabelSelector
>>>
>>> ir = PruningIR(model)
>>> with LossAwareCriterion(ir) as score_collector:
>>>     for sample in train_loader:
>>>         model_output = score_collector(sample)
>>>         loss = loss_function(model_output, sample)
>>>         loss.backward()
>>>
>>> label_selector = UniformLabelSelector(pruning_ratio=0.5)
>>> labels_for_pruning = label_selector.select(ir.snapshot())
>>> ir = ir.prune(labels=labels_for_pruning)
>>> pruned_model = ir.model

"""
from enot.pruning_v2.criteria import LossAwareCriterion as LossAwareCriterion
from enot.pruning_v2.ir import PruningIR as PruningIR
from enot.pruning_v2.label_selector import GlobalScoreLabelSelector as GlobalScoreLabelSelector
from enot.pruning_v2.label_selector import KnapsackLabelSelector as KnapsackLabelSelector
from enot.pruning_v2.label_selector import LatencyLabelSelector as LatencyLabelSelector
from enot.pruning_v2.label_selector import SCBOLabelSelector as SCBOLabelSelector
from enot.pruning_v2.label_selector import UniformLabelSelector as UniformLabelSelector
