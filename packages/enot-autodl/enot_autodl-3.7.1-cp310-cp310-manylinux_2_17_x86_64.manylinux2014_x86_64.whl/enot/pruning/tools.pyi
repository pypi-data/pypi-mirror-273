import torch
from enot.pruning.gate import ChannelGate as ChannelGate
from enot.pruning.graph_parsing.parser_state.parser_state import DimensionLabels as DimensionLabels
from enot.pruning.graph_parsing.utils import pretty_str_labels as pretty_str_labels
from enot.pruning.labels import Label as Label, LabelGroup as LabelGroup
from enot.pruning.pruning_info import ModelPruningInfo as ModelPruningInfo
from enot.tensor_trace import Node as Node, OpNode as OpNode, ParameterNode as ParameterNode
from enot.tensor_trace.tensor_link_utils import get_tensor_by_link_in_model as get_tensor_by_link_in_model
from enot.tensor_trace.tools import get_module_name_by_tracing_node as get_module_name_by_tracing_node, get_tracing_node_by_module_name as get_tracing_node_by_module_name
from enot.utils.common import getattr_complex as getattr_complex
from enot.utils.weights_manipulation.weight_mapping import apply_nd_mapping as apply_nd_mapping
from pathlib import Path
from torch import nn as nn
from typing import NamedTuple

class LabelFilterInfo(NamedTuple):
    """General information of label filter."""
    tensor_name: str
    shape: tuple[int, ...]
    mapping: list[list[tuple[int, int]] | None]
    tensor: torch.Tensor | None = ...

def tabulate_module_dependencies(module_name: str, pruning_info: ModelPruningInfo, model: nn.Module | None = None, show_op_with_weights_only: bool = True, show_parameter_nodes: bool = False, show_all_nodes: bool = False) -> str:
    '''
    Return a string containing all of the tracing/pruning information
    for the node corresponding to the module with the given name.

    Parameters
    ----------
    module_name : str
        Name of the module in torch model, for example: "features.5.conv.1.0".
    pruning_info : ModelPruningInfo
        Pruning state, can be obtained from calibrator.
    model : Optional[nn.Module]
        PyTorch model used for calibration.
    show_op_with_weights_only : bool
        Include nodes with weights (modules) only. Default value is True.
    show_parameter_nodes : bool
        Include or not Parameter nodes. Default value is False.
    show_all_nodes : bool
        Include or not all types of nodes. Default value is False.

    Returns
    -------
    str
        Tracing/pruning information for the node corresponding to the module wit the given name.

    '''
def tabulate_label_dependencies(label: Label | int, pruning_info: ModelPruningInfo, model: nn.Module | None = None, show_op_with_weights_only: bool = True, show_parameter_nodes: bool = False, show_all_nodes: bool = False) -> str:
    """
    Return a string containing all of the tracing/pruning information
    for the label.

    Parameters
    ----------
    label : Union[Label, int]
        Label for which information is to be printed.
    pruning_info : ModelPruningInfo
        Pruning state, can be obtained from calibrator.
    model : Optional[nn.Module]
        PyTorch model used for calibration.
    show_op_with_weights_only : bool
        Include nodes with weights (modules) only. Default value is True.
    show_parameter_nodes : bool
        Include or not Parameter nodes. Default value is False.
    show_all_nodes : bool
        Include or not all types of nodes. Default value is False.

    Returns
    -------
    str
        Tracing/pruning information for the label.

    """
def tabulate_unprunable_groups(pruning_info: ModelPruningInfo, model: nn.Module | None = None, show_op_with_weights_only: bool = True, show_parameter_nodes: bool = False, show_all_nodes: bool = False) -> str:
    """
    Return a string containing all of the tracing/pruning information
    for all unprunable groups.

    Parameters
    ----------
    pruning_info : ModelPruningInfo
        Pruning state, can be obtained from calibrator.
    model : Optional[nn.Module]
        PyTorch model used for calibration.
    show_op_with_weights_only : bool
        Include nodes with weights (modules) only. Default value is True.
    show_parameter_nodes : bool
        Include or not Parameter nodes. Default value is False.
    show_all_nodes : bool
        Include or not all types of nodes. Default value is False.

    Returns
    -------
    str
        Tracing/pruning information for all unprunable groups.

    """
def tabulate_label_filters(label: Label | int, pruning_info: ModelPruningInfo, model: nn.Module) -> str:
    """
    Return a string containing all of the label filters information.

    Parameters
    ----------
    label : Union[Label, int]
        The label for which filters are be found.
    pruning_info : ModelPruningInfo
        Pruning state, can be obtained from calibrator.
    model : nn.Module
        PyTorch model used for calibration.

    Returns
    -------
    str
        Label filters information.

    """
def get_label_filters(label: Label | int, pruning_info: ModelPruningInfo, model: nn.Module, *, with_tensors: bool = False) -> list[LabelFilterInfo]:
    """
    Return filters that corresponding to passed label.

    Parameters
    ----------
    label : Union[Label, int]
        The label for which filters are be found.
    pruning_info : ModelPruningInfo
        Pruning state, can be obtained from calibrator.
    model : nn.Module
        PyTorch model used for calibration.
    with_tensors : bool
        Include filter values (tensors) or not. Default value is False.

    Returns
    -------
    List[LabelFilterInfo]
        List of containers with filter tensor name, shape, mapping and filter value (optionally).

    """
def save_pruning_info(pruning_info: ModelPruningInfo, path: str | Path) -> None:
    """
    Serialize ModelPruningInfo to file.

    Parameters
    ----------
    pruning_info : ModelPruningInfo
        ModelPruningInfo to serialize.
    path : Union[str, Path]
        Path to save.

    """
def load_pruning_info(path: str | Path, map_location: str = 'cuda') -> ModelPruningInfo:
    """
    Deserialize ModelPruningInfo from file.

    Parameters
    ----------
    path : Union[str, Path]
        Path to serialized ModelPruningInfo.
    map_location : str
        Location for deserialization, the same as in ``torch.load``. Default value is ``cuda``.

    Returns
    -------
    ModelPruningInfo
        Deserialized ModelPruningInfo.

    """
