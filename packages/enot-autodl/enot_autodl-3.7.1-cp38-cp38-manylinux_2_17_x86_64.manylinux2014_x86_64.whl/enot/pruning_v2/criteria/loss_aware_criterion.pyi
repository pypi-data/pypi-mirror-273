from enot.graph.common import insert_node_after_node as insert_node_after_node, remove_node as remove_node
from enot.graph.ir.ir import DEFAULT_SNAPSHOT_NAME as DEFAULT_SNAPSHOT_NAME
from enot.graph.ir.node import Node as Node, output_type as output_type
from enot.graph.ir.snapshot import Snapshot as Snapshot
from enot.pruning_v2.criteria.base import PruningCriterion as PruningCriterion
from enot.pruning_v2.criteria.gate import NodeOutputGate as NodeOutputGate
from enot.pruning_v2.criteria.label_groups import label_groups as label_groups
from enot.pruning_v2.criteria.manual_gate import manual_gate_labels as manual_gate_labels
from enot.pruning_v2.ir import PruningIR as PruningIR
from enot.pruning_v2.label import Label as Label, has_tensor_labels as has_tensor_labels
from enot.pruning_v2.label_inference.node_handlers.binary_elementwise import AGGREGATE_BINARY_OPS as AGGREGATE_BINARY_OPS, binary_node_inputs as binary_node_inputs

class LossAwareCriterion(PruningCriterion):
    """Default ENOT pruning Criterion."""
    def __init__(self, ir: PruningIR, snapshot_name: str = ...) -> None: ...
